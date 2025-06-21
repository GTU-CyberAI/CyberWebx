# model.py
import pickle
import pandas as pd
import numpy as np

class MalwareModel:
    def __init__(self, model_path: str, scaler_path: str):
        # Model ve selector'ı yükle
        self.classifier = pickle.load(open(model_path, 'rb'))    # RandomForestClassifier
        self.selector = pickle.load(open(scaler_path, 'rb'))   # SelectFromModel

    def predict_from_features(self, features, columns):
        # Name ve md5 hariç, sadece modelin eğitildiği özellikleri al
        feature_values = np.array([features[2:]])  # 2D array
        
        # Özellik seçimi (SelectFromModel)
        selected_features = self.selector.transform(feature_values)
        
        # Model tahmini
        prediction = self.classifier.predict(selected_features)[0]

        # Sonucu etiketle
        return "legitimate" if str(prediction) == str(1) else "malicious"
