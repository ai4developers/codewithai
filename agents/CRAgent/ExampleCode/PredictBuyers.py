# ============================================
# Simple Home Buyer Prediction Example
# All data is hardcoded for demo purposes.
# ============================================

# Disclaimer: This is for learning only, not for production.

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ------------------------------
# 1. Hardcoded dataset
# Each row: [Age, Income (in $1000s), Credit Score, Years at Job]
# Labels: 1 = will buy house, 0 = won't buy
# ------------------------------
X = np.array([
    [25, 50, 700, 2],
    [30, 60, 720, 4],
    [22, 40, 680, 1],
    [35, 80, 750, 5],
    [40, 90, 770, 10],
    [28, 55, 710, 3],
    [50, 100, 800, 15],
    [45, 85, 780, 12],
    [23, 45, 690, 2],
    [33, 70, 740, 5],
])

y = np.array([0, 1, 0, 1, 1, 0, 1, 1, 0, 1])  # Labels

# ------------------------------
# 2. Split into training and test sets
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ------------------------------
# 3. Build the model
# ------------------------------
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# ------------------------------
# 4. Predict and evaluate
# ------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Predictions:", y_pred)
print("Actual     :", y_test)
print(f"Model Accuracy: {accuracy:.2f}")

# ------------------------------
# 5. Predict for a new buyer
# ------------------------------
new_buyer = np.array([[29, 65, 730, 3]])  # Example: 29 yrs, $65k income, 730 score, 3 yrs at job
prediction = model.predict(new_buyer)
print(f"New buyer prediction (1=buy, 0=not buy): {prediction[0]}")
