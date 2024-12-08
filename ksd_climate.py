# -*- coding: utf-8 -*-
"""KSD Climate.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MNm_KxImNfRPZhBTtIINqI91f2oXEJYM
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/climate_change_impact_on_agriculture_2024.csv')

df.head()

df.info()

"""10000 instance

15 features

No missing values

only 4 categorical features
"""

df.describe()

# Pemeriksaan Kualitas Data
print("\nJumlah Nilai Kosong di Setiap Kolom:")
print(df.isnull().sum())

df['Crop_Type'].value_counts()

df['Country'].value_counts()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Histogram untuk kolom numerik
numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
df[numerical_cols].hist(bins=15, figsize=(15, 10))
plt.suptitle("Distribusi Data Numerik", fontsize=16)
plt.show()

# Heatmap untuk korelasi data numerik
plt.figure(figsize=(10, 8))
sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Heatmap Korelasi")
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 1. Encoding Fitur Kategorikal
categorical_features = ['Country', 'Region', 'Crop_Type', 'Adaptation_Strategies']
numerical_features = [
    'Year', 'Average_Temperature_C', 'Total_Precipitation_mm', 'CO2_Emissions_MT',
    'Extreme_Weather_Events', 'Irrigation_Access_%', 'Pesticide_Use_KG_per_HA',
    'Fertilizer_Use_KG_per_HA', 'Soil_Health_Index', 'Economic_Impact_Million_USD'
]

# Target (Crop Yield)
target = 'Crop_Yield_MT_per_HA'

# Memisahkan target dan fitur
X = df.drop(columns=[target])
y = df[target]

# Pipeline untuk preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),  # Normalisasi fitur numerik
        ('cat', OneHotEncoder(drop='first'), categorical_features)  # One-hot encoding untuk kategorikal
    ]
)

# 2. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Pipeline untuk Data Training
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
])

# Transformasi data
X_train_processed = pipeline.fit_transform(X_train)
X_test_processed = pipeline.transform(X_test)

print("Shape data setelah preprocessing:")
print("X_train:", X_train_processed.shape)
print("X_test:", X_test_processed.shape)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# 1. Model Awal: Linear Regression
model_lr = LinearRegression()

# Melatih model
model_lr.fit(X_train_processed, y_train)

# Prediksi pada data uji
y_pred_lr = model_lr.predict(X_test_processed)

# Evaluasi Model
mae_lr = mean_absolute_error(y_test, y_pred_lr)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print("Linear Regression Performance:")
print(f"MAE: {mae_lr:.2f}")
print(f"MSE: {mse_lr:.2f}")
print(f"R²: {r2_lr:.2f}")

# 2. Model Lanjutan: Random Forest Regressor
model_rf = RandomForestRegressor(random_state=42)

# Melatih model
model_rf.fit(X_train_processed, y_train)

# Prediksi pada data uji
y_pred_rf = model_rf.predict(X_test_processed)

# Evaluasi Model
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("\nRandom Forest Regressor Performance:")
print(f"MAE: {mae_rf:.2f}")
print(f"MSE: {mse_rf:.2f}")
print(f"R²: {r2_rf:.2f}")

from sklearn.model_selection import GridSearchCV

# Parameter yang akan diuji
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Grid Search untuk Random Forest
grid_search = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid=param_grid,
    cv=5,  # Cross-validation dengan 5 fold
    scoring='r2',
    n_jobs=-1,  # Gunakan semua prosesor yang tersedia
    verbose=2
)

# Melakukan pencarian parameter terbaik
grid_search.fit(X_train_processed, y_train)

# Model terbaik
best_rf_model = grid_search.best_estimator_

print("Best Parameters:", grid_search.best_params_)
print("Best Cross-Validation R²:", grid_search.best_score_)

from sklearn.model_selection import cross_val_score

# Evaluasi dengan cross-validation
cv_scores = cross_val_score(best_rf_model, X_train_processed, y_train, cv=5, scoring='r2')

print(f"Cross-Validation R² Scores: {cv_scores}")
print(f"Mean R²: {np.mean(cv_scores):.2f}, Std Dev: {np.std(cv_scores):.2f}")

# Prediksi pada data uji
y_pred_test = best_rf_model.predict(X_test_processed)

# Evaluasi model
mae_test = mean_absolute_error(y_test, y_pred_test)
mse_test = mean_squared_error(y_test, y_pred_test)
r2_test = r2_score(y_test, y_pred_test)

print("\nFinal Model Performance on Test Data:")
print(f"MAE: {mae_test:.2f}")
print(f"MSE: {mse_test:.2f}")
print(f"R²: {r2_test:.2f}")

print(f"Panjang Feature Importance: {len(feature_importance)}")
print(f"Panjang Feature Names: {len(feature_names)}")

# Mendapatkan nama fitur setelah preprocessing
# OneHotEncoder secara otomatis menambahkan nama kategori, StandardScaler hanya meneruskan nama aslinya.
feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()

# Cek jumlah nama fitur
print(f"Panjang Feature Names: {len(feature_names)}")
print(f"Contoh Feature Names: {feature_names[:10]}")

from sklearn.ensemble import RandomForestRegressor

# Melatih model
model_rf = RandomForestRegressor(random_state=42)
model_rf.fit(X_train_processed, y_train)

# Mendapatkan feature importance
feature_importance = model_rf.feature_importances_

# Membuat DataFrame untuk Feature Importance
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importance
}).sort_values(by='Importance', ascending=False)

print(importance_df.head())

import matplotlib.pyplot as plt

# Plot Feature Importance
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'][:10], importance_df['Importance'][:10], color='skyblue')
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Feature Importance")
plt.gca().invert_yaxis()  # Membalikkan urutan untuk fitur dengan importance tertinggi di atas
plt.show()

!pip install shap

import os

# Membuat struktur folder
os.makedirs("project/model", exist_ok=True)

# Membuat file kosong (untuk keperluan struktur)
open("project/app.py", "w").close()
open("project/model/pipeline.pkl", "w").close()
open("project/model/model.pkl", "w").close()

print("Struktur folder berhasil dibuat!")

import joblib

# Simpan pipeline preprocessing
joblib.dump(pipeline, 'project/model/pipeline.pkl')

# Simpan model terlatih
joblib.dump(model_rf, 'project/model/model.pkl')

!pip install fastapi uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Inisialisasi FastAPI
app = FastAPI()

# Muat model dan pipeline
model = joblib.load('project/model/model.pkl')  # Ganti dengan path yang sesuai
pipeline = joblib.load('project/model/pipeline.pkl')  # Ganti dengan path yang sesuai

# Mendefinisikan model input untuk FastAPI
class CropPredictionRequest(BaseModel):
    Year: int
    Country: str
    Region: str
    Crop_Type: str
    Average_Temperature_C: float
    Total_Precipitation_mm: float
    CO2_Emissions_MT: float
    Extreme_Weather_Events: int
    Irrigation_Access_percent: float  # Ganti nama atribut di sini
    Pesticide_Use_KG_per_HA: float
    Fertilizer_Use_KG_per_HA: float
    Soil_Health_Index: float
    Adaptation_Strategies: str
    Economic_Impact_Million_USD: float

# Fungsi untuk memproses input dan menghasilkan prediksi
@app.post("/predict")
def predict_crop_yield(data: CropPredictionRequest):
    # Ubah input menjadi dataframe
    input_data = pd.DataFrame([data.dict()])

    # Preprocessing data
    processed_data = pipeline.transform(input_data)

    # Prediksi dengan model terlatih
    prediction = model.predict(processed_data)

    # Mengembalikan hasil prediksi
    return {"predicted_crop_yield": prediction[0]}

# Endpoint untuk mengecek status aplikasi
@app.get("/")
def read_root():
    return {"message": "Aplikasi prediksi hasil panen berjalan"}