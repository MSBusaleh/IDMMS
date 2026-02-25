import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error, r2_score

# ==========================================
# 1. DATA GENERATOR (Strict Error Control)
# ==========================================
def generate_data(samples=5000):
    #np.random.seed(42)
    
    data = {
        'Barite_ppb': np.random.uniform(0, 200, samples),
        'Bentonite_ppb': np.random.uniform(5, 25, samples),
        'KCl_ppb': np.random.uniform(0, 40, samples),
        'Starch_ppb': np.random.uniform(1, 6, samples),
        'Caustic_ppb': np.random.uniform(0.1, 1.2, samples),
        'Temp_F': np.random.uniform(80, 200, samples)
    }
    df = pd.DataFrame(data)

    # Physics-based outputs
    df['Density_ppg'] = 8.33 + (df['Barite_ppb'] * 0.014) + (df['Bentonite_ppb'] * 0.005)
    df['YP_lb100ft2'] = (df['Bentonite_ppb'] * 1.8) * np.exp(-0.015 * df['KCl_ppb']) - (0.05 * df['Temp_F'])
    df['pH'] = 8.5 + 3.2 * np.log10(1 + df['Caustic_ppb'] * 8)
    df['Fluid_Loss_mL'] = 18 * np.exp(-0.35 * df['Starch_ppb']) + (0.04 * df['Temp_F'])
    
    noise_level = 0.005 
    for col in ['Density_ppg', 'YP_lb100ft2', 'pH', 'Fluid_Loss_mL']:
        df[col] += np.random.normal(0, df[col].mean() * noise_level, samples)
        
    return df

# ==========================================
# 2. AI TRAINING ENGINE
# ==========================================
df = generate_data()
X = df[['Barite_ppb', 'Bentonite_ppb', 'KCl_ppb', 'Starch_ppb', 'Caustic_ppb', 'Temp_F']]
Y = df[['Density_ppg', 'YP_lb100ft2', 'pH', 'Fluid_Loss_mL']]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Multi-output Random Forest
model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# ==========================================
# 3. LOSS CALCULATION (Verification)
# ==========================================
predictions = model.predict(X_test)

# MAPE represents the average percentage error (e.g., 0.02 = 2% error)
mape = mean_absolute_percentage_error(y_test, predictions)
accuracy_pct = (1 - mape) * 100

print(f"--- ERROR ANALYSIS ---")
print(f"Mean Absolute Percentage Error (MAPE): ({mape*100:.2f}%)")
print(f"Model Accuracy: {accuracy_pct:.2f}%")
print(f"R2 Score: {r2_score(y_test, predictions):.4f}")

# ==========================================
# 4. CONTROLLER SIMULATION
# ==========================================
test_well = [120, 15, 10, 4, 0.8, 150]
current_preds = model.predict([test_well])[0]

print(f"\n--- PREDICTED MUD PROPERTIES ---")
print(f"Density: {current_preds[0]:.2f} ppg")
print(f"Yield Point: {current_preds[1]:.2f} lb/100ft2")
print(f"Fluid Loss: {current_preds[3]:.2f} mL")