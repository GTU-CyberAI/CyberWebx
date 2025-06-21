import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("MalwareData.csv", sep="|")

# Print dataset info
legit = df[0:41323].drop(["legitimate"], axis=1)
mal = df[41323:].drop(["legitimate"], axis=1)
print(f"The legitimate dataset is: {legit.shape[0]} samples, {legit.shape[1]} features")
print(f"The malicious dataset is: {mal.shape[0]} samples, {mal.shape[1]} features\n")

# Prepare X and y
X = df.drop(["Name", "md5", "legitimate"], axis=1).values
y = df["legitimate"].values

# Feature selection
extratrees = ExtraTreesClassifier().fit(X, y)
selector = SelectFromModel(extratrees, prefit=True)
X_selected = selector.transform(X)

print(f"The new dataset contains now: {X_selected.shape[1]} features\n")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2)

# Train classifier
clf = RandomForestClassifier(n_estimators=50)
clf.fit(X_train, y_train)

# Print score
print("The score of the algorithm is:", clf.score(X_test, y_test) * 100)

# Save model
with open("Classifier/finalized_model.sav", "wb") as f:
    pickle.dump(clf, f)

# Save feature selector
with open("Classifier/scaler.pkl", "wb") as f:
    pickle.dump(selector, f)

print("\nModel and selector saved successfully.")
