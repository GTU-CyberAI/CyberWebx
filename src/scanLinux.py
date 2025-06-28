import pefile
import os
import hashlib
import array
import math
import pandas as pd
import model as ml_model
from model import MalwareModel


COLUMNS = [
    "Name", "md5", "Machine", "SizeOfOptionalHeader", "Characteristics",
    "MajorLinkerVersion", "MinorLinkerVersion", "SizeOfCode", "SizeOfInitializedData",
    "SizeOfUninitializedData", "AddressOfEntryPoint", "BaseOfCode", "BaseOfData",
    "ImageBase", "SectionAlignment", "FileAlignment", "MajorOperatingSystemVersion",
    "MinorOperatingSystemVersion", "MajorImageVersion", "MinorImageVersion",
    "MajorSubsystemVersion", "MinorSubsystemVersion", "SizeOfImage", "SizeOfHeaders",
    "CheckSum", "Subsystem", "DllCharacteristics", "SizeOfStackReserve",
    "SizeOfStackCommit", "SizeOfHeapReserve", "SizeOfHeapCommit", "LoaderFlags",
    "NumberOfRvaAndSizes", "SectionsNb", "SectionsMeanEntropy", "SectionsMinEntropy",
    "SectionsMaxEntropy", "SectionsMeanRawsize", "SectionsMinRawsize",
    "SectionMaxRawsize", "SectionsMeanVirtualsize", "SectionsMinVirtualsize",
    "SectionMaxVirtualsize", "ImportsNbDLL", "ImportsNb", "ImportsNbOrdinal",
    "ExportNb", "ResourcesNb", "ResourcesMeanEntropy", "ResourcesMinEntropy",
    "ResourcesMaxEntropy", "ResourcesMeanSize", "ResourcesMinSize",
    "ResourcesMaxSize", "LoadConfigurationSize", "VersionInformationSize"
]
# get_md5 fonksiyonu, verilen dosya yolundaki dosyayı ikili (binary) modda açar
# Dosyayı 4096 baytlık parçalar halinde okuyarak MD5 hash değerini hesaplar
# Fonksiyon, hesaplanan hash'i hexadecimal formatta döndürür
def get_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# get_entropy fonksiyonu, verilen veri (byte dizisi) üzerinde Shannon entropisini hesaplar
# Veri içerisindeki her baytın frekansı belirlenir ve bu frekanslara göre entropi değeri hesaplanır
# Fonksiyon, veri boşsa 0.0, aksi halde hesaplanan entropi değerini döndürür
def get_entropy(data):
    if len(data) == 0:
        return 0.0
    occurences = array.array('L', [0]*256)
    for x in data:
        occurences[x if isinstance(x, int) else ord(x)] += 1

    entropy = 0
    for x in occurences:
        if x:
            p_x = float(x) / len(data)
            entropy -= p_x*math.log(p_x, 2)
    return entropy

# get_resources fonksiyonu, PE dosyasındaki kaynak (resources) bilgilerini toplar
# PE dosyasının DIRECTORY_ENTRY_RESOURCE özelliği varsa, kaynak tipleri, ID'leri ve dil bazında tekrarlanan bilgiler alınır
# Her bir kaynak için, verinin baytlarını elde eder, boyutunu alır ve entropi hesaplanır
# Fonksiyon, her bir kaynağı [entropi, boyut] biçiminde bir liste olarak döndürür
def get_resources(pe):
    resources = []
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        try:
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if hasattr(resource_type, 'directory'):
                    for resource_id in resource_type.directory.entries:
                        if hasattr(resource_id, 'directory'):
                            for resource_lang in resource_id.directory.entries:
                                data = pe.get_data(
                                    resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                                size = resource_lang.data.struct.Size
                                entropy = get_entropy(data)
                                resources.append([entropy, size])
        except Exception:
            return resources
    return resources

# get_version_info fonksiyonu, PE dosyasından sürüm bilgilerini ve sabit dosya bilgilerini toplar
# FileInfo bölümündeki StringFileInfo ve VarFileInfo alt bölümlerinden metin ve değişken bilgilerini çıkarır
# Ek olarak, VS_FIXEDFILEINFO yapısı varsa, burada yer alan dosya bayrakları, işletim sistemi, dosya türü ve sürüm numaraları gibi bilgileri de ekler
# Fonksiyon, bu bilgileri anahtar-değer çiftleri şeklinde bir sözlük olarak döndürür
def get_version_info(pe):
    res = {}
    for fileinfo in pe.FileInfo:
        if fileinfo.Key == 'StringFileInfo':
            for st in fileinfo.StringTable:
                for entry in st.entries.items():
                    res[entry[0]] = entry[1]
        if fileinfo.Key == 'VarFileInfo':
            for var in fileinfo.Var:
                res[var.entry.items()[0][0]] = var.entry.items()[0][1]
    if hasattr(pe, 'VS_FIXEDFILEINFO'):
        res['flags'] = pe.VS_FIXEDFILEINFO.FileFlags
        res['os'] = pe.VS_FIXEDFILEINFO.FileOS
        res['type'] = pe.VS_FIXEDFILEINFO.FileType
        res['file_version'] = pe.VS_FIXEDFILEINFO.FileVersionLS
        res['product_version'] = pe.VS_FIXEDFILEINFO.ProductVersionLS
        res['signature'] = pe.VS_FIXEDFILEINFO.Signature
        res['struct_version'] = pe.VS_FIXEDFILEINFO.StrucVersion
    return res

# extract_infos fonksiyonu, verilen dosya yolundaki PE dosyası üzerinde çeşitli bilgileri çıkarır
# Dosya ismi ve MD5 hash değeri ilk olarak elde edilir
# PE dosyasının temel başlık (header) bilgileri, opsiyonel başlık değerleri ve section (bölüm) bilgileri toplanır
# Section'ların entropileri, raw (ham) ve virtual boyut bilgileri hesaplanır
# İçe aktarmalar (imports) ve dışa aktarımlar (exports) ile ilgili istatistikler, kaynak (resources) bilgileri de eklenir
# Ek olarak, load configuration ve version bilgileri de çıkarılır
# Fonksiyon, elde edilen tüm özellikleri belirlenen sütun sırasına uygun olarak bir liste şeklinde döndürür
def extract_infos(fpath):
    res = []
    res.append(os.path.basename(fpath))
    res.append(get_md5(fpath))
    pe = pefile.PE(fpath)
    res.append(pe.FILE_HEADER.Machine)
    res.append(pe.FILE_HEADER.SizeOfOptionalHeader)
    res.append(pe.FILE_HEADER.Characteristics)
    res.append(pe.OPTIONAL_HEADER.MajorLinkerVersion)
    res.append(pe.OPTIONAL_HEADER.MinorLinkerVersion)
    res.append(pe.OPTIONAL_HEADER.SizeOfCode)
    res.append(pe.OPTIONAL_HEADER.SizeOfInitializedData)
    res.append(pe.OPTIONAL_HEADER.SizeOfUninitializedData)
    res.append(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    res.append(pe.OPTIONAL_HEADER.BaseOfCode)
    try:
        res.append(pe.OPTIONAL_HEADER.BaseOfData)
    except AttributeError:
        res.append(0)
    res.append(pe.OPTIONAL_HEADER.ImageBase)
    res.append(pe.OPTIONAL_HEADER.SectionAlignment)
    res.append(pe.OPTIONAL_HEADER.FileAlignment)
    res.append(pe.OPTIONAL_HEADER.MajorOperatingSystemVersion)
    res.append(pe.OPTIONAL_HEADER.MinorOperatingSystemVersion)
    res.append(pe.OPTIONAL_HEADER.MajorImageVersion)
    res.append(pe.OPTIONAL_HEADER.MinorImageVersion)
    res.append(pe.OPTIONAL_HEADER.MajorSubsystemVersion)
    res.append(pe.OPTIONAL_HEADER.MinorSubsystemVersion)
    res.append(pe.OPTIONAL_HEADER.SizeOfImage)
    res.append(pe.OPTIONAL_HEADER.SizeOfHeaders)
    res.append(pe.OPTIONAL_HEADER.CheckSum)
    res.append(pe.OPTIONAL_HEADER.Subsystem)
    res.append(pe.OPTIONAL_HEADER.DllCharacteristics)
    res.append(pe.OPTIONAL_HEADER.SizeOfStackReserve)
    res.append(pe.OPTIONAL_HEADER.SizeOfStackCommit)
    res.append(pe.OPTIONAL_HEADER.SizeOfHeapReserve)
    res.append(pe.OPTIONAL_HEADER.SizeOfHeapCommit)
    res.append(pe.OPTIONAL_HEADER.LoaderFlags)
    res.append(pe.OPTIONAL_HEADER.NumberOfRvaAndSizes)
    res.append(len(pe.sections))
    entropy = list(map(lambda x: x.get_entropy(), pe.sections))
    res.append(sum(entropy)/len(entropy))
    res.append(min(entropy))
    res.append(max(entropy))
    raw_sizes = list(map(lambda x: x.SizeOfRawData, pe.sections))
    res.append(sum(raw_sizes)/float(len(raw_sizes)))
    res.append(min(raw_sizes))
    res.append(max(raw_sizes))
    virtual_sizes = list(map(lambda x: x.Misc_VirtualSize, pe.sections))
    res.append(sum(virtual_sizes)/float(len(virtual_sizes)))
    res.append(min(virtual_sizes))
    res.append(max(virtual_sizes))
    try:
        res.append(len(pe.DIRECTORY_ENTRY_IMPORT))
        imports = sum([x.imports for x in pe.DIRECTORY_ENTRY_IMPORT], [])
        res.append(len(imports))
        res.append(len(list(filter(lambda x: x.name is None, imports))))
    except AttributeError:
        res.append(0)
        res.append(0)
        res.append(0)
    try:
        res.append(len(pe.DIRECTORY_ENTRY_EXPORT.symbols))
    except AttributeError:
        res.append(0)
    resources = get_resources(pe)
    res.append(len(resources))
    if len(resources) > 0:
        entropy = list(map(lambda x: x[0], resources))
        res.append(sum(entropy)/float(len(entropy)))
        res.append(min(entropy))
        res.append(max(entropy))
        sizes = list(map(lambda x: x[1], resources))
        res.append(sum(sizes)/float(len(sizes)))
        res.append(min(sizes))
        res.append(max(sizes))
    else:
        res.extend([0]*6)
    try:
        res.append(pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.Size)
    except AttributeError:
        res.append(0)
    try:
        version_infos = get_version_info(pe)
        res.append(len(version_infos.keys()))
    except AttributeError:
        res.append(0)

    try:
        pe.close()
    except Exception:
        pass
    del pe

    return res

# scan_pe_file fonksiyonu, belirtilen dosya yolundaki PE dosyasından çıkarılan özellikler ile
# MalwareModel tipindeki modelin tahmin fonksiyonunu çağırır
# Modelin çıktısına bağlı olarak dosya ismi ve tespit sonucunu içeren bir sözlük döndürür
def scan_pe_file(file_path: str, model: MalwareModel):
    features = extract_infos(file_path)
    result = model.predict_from_features(features, COLUMNS)
    return {
        "filename": features[0],
        "result": result
    }