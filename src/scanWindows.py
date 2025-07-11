# Gerekli kütüphaneler içe aktarılıyor
import pefile # PE (Portable Executable) dosyalarını analiz etmek için
import os
import hashlib  # Dosyanın hash'ini almak için
import array
import math
import model as ml_model  # Model işlemleri için kendi yazdığın "model.py"
import pandas as pd
from model import MalwareModel  # Sınıf bazlı model sınıfı

# Modelin beklediği özellik isimleri
COLUMNS = [
    # Dosya ismi ve md5 hash
    "Name",
    "md5",
    # PE Header bilgileri
    "Machine",
    "SizeOfOptionalHeader",
    "Characteristics",
    "MajorLinkerVersion",
    "MinorLinkerVersion",
    "SizeOfCode",
    "SizeOfInitializedData",
    "SizeOfUninitializedData",
    "AddressOfEntryPoint",
    "BaseOfCode",
    "BaseOfData",
    "ImageBase",
    "SectionAlignment",
    "FileAlignment",
    "MajorOperatingSystemVersion",
    "MinorOperatingSystemVersion",
    "MajorImageVersion",
    "MinorImageVersion",
    "MajorSubsystemVersion",
    "MinorSubsystemVersion",
    "SizeOfImage",
    "SizeOfHeaders",
    "CheckSum",
    "Subsystem",
    "DllCharacteristics",
    "SizeOfStackReserve",
    "SizeOfStackCommit",
    "SizeOfHeapReserve",
    "SizeOfHeapCommit",
    "LoaderFlags",
    "NumberOfRvaAndSizes",
    # Section sayısı ve istatistikleri
    "SectionsNb",
    "SectionsMeanEntropy",
    "SectionsMinEntropy",
    "SectionsMaxEntropy",
    "SectionsMeanRawsize",
    "SectionsMinRawsize",
    "SectionMaxRawsize",
    "SectionsMeanVirtualsize",
    "SectionsMinVirtualsize",
    "SectionMaxVirtualsize",
    # Import/Export bilgileri
    "ImportsNbDLL",
    "ImportsNb",
    "ImportsNbOrdinal",
    "ExportNb",
    # Resource bilgileri
    "ResourcesNb",
    "ResourcesMeanEntropy",
    "ResourcesMinEntropy",
    "ResourcesMaxEntropy",
    "ResourcesMeanSize",
    "ResourcesMinSize",
    "ResourcesMaxSize",
    # Diğer bilgiler
    "LoadConfigurationSize",
    "VersionInformationSize"
]


# Dosyanın md5 hash'ini hesaplar
def get_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# Verilen veri (byte array) için entropi hesaplar
def get_entropy(data):
    if len(data) == 0:
        return 0.0
    occurences = array.array('L', [0] * 256)
    for x in data:
        occurences[x if isinstance(x, int) else ord(x)] += 1

    entropy = 0
    for x in occurences:
        if x:
            p_x = float(x) / len(data)
            entropy -= p_x * math.log(p_x, 2)

    return entropy


# PE dosyasındaki resource'ları alır ve entropi ile birlikte döner
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


# PE dosyasından versiyon bilgilerini çıkartır
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


# Verilen bir PE dosyasından tüm gerekli özellikleri çıkarır
def extract_infos(fpath):
    res = []
    res.append(os.path.basename(fpath))  # Dosya adı
    res.append(get_md5(fpath))  # md5 hash
    pe = pefile.PE(fpath)

    # PE Header bilgileri
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

    # Section sayısı ve istatistikleri
    res.append(len(pe.sections))
    entropy = list(map(lambda x: x.get_entropy(), pe.sections))
    # Ortalama entropi
    res.append(sum(entropy)/len(entropy))
    res.append(min(entropy))
    res.append(max(entropy))
    raw_sizes = list(map(lambda x: x.SizeOfRawData, pe.sections))
    res.append(sum(raw_sizes)/len(raw_sizes))
    res.append(min(raw_sizes))
    res.append(max(raw_sizes))
    virtual_sizes = list(map(lambda x: x.Misc_VirtualSize, pe.sections))
    res.append(sum(virtual_sizes)/len(virtual_sizes))
    res.append(min(virtual_sizes))
    res.append(max(virtual_sizes))

    # Import/Export bilgileri
    try:
        res.append(len(pe.DIRECTORY_ENTRY_IMPORT))
        imports = sum([x.imports for x in pe.DIRECTORY_ENTRY_IMPORT], [])
        res.append(len(imports))
        # ordinal import sayısı
        res.append(len([x for x in imports if x.name is None]))
    except AttributeError:
        res += [0, 0, 0]

    try:
        # Export edilen semboller
        res.append(len(pe.DIRECTORY_ENTRY_EXPORT.symbols))
    except AttributeError:
        res.append(0)

    # Resource bilgileri
    resources = get_resources(pe)
    res.append(len(resources))
    if resources:
        entropy = [x[0] for x in resources]
        sizes = [x[1] for x in resources]
        res += [
            sum(entropy)/len(entropy), min(entropy), max(entropy),
            sum(sizes)/len(sizes), min(sizes), max(sizes)
        ]
    else:
        res += [0] * 6

    # Load Config ve Version Info
    try:
        res.append(pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.Size)
    except AttributeError:
        res.append(0)
    try:
        version_info = get_version_info(pe)
        res.append(len(version_info))
    except AttributeError:
        res.append(0)

    # PE dosyasını kapat (bellek sızıntısını önlemek için)
    try:
        pe.close()
    except Exception:
        pass
    del pe

    return res


# Belirli bir PE dosyasını tarar ve modeli kullanarak sonucu döner
def scan_pe_file(file_path: str, model: MalwareModel):
    features = extract_infos(file_path)
    result = model.predict_from_features(features, COLUMNS)
    return {
        "filename": features[0],
        "result": result
    }
