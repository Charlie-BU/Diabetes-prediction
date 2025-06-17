import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.combine import SMOTEENN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression  # meta‑model
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import xgboost
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, accuracy_score, roc_auc_score

# Load and preprocess raw data
df = pd.read_csv('diabetes_prediction_dataset.csv')
df['gender'] = df['gender'].map({'Female': 0, 'Male': 1, 'Other': 2})
smoking_map = {
    'never': 0, 'No Info': 1, 'current': 2,
    'former': 3, 'ever': 4, 'not current': 5
}
df['smoking_history'] = df['smoking_history'].map(smoking_map)

diab_X = df.drop('diabetes', axis=1)
diab_y = df['diabetes']

# Load pickled models
with open('JJC_diabetes_prediction_xgboost_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)

nn_params = {
    'n_layers': 2,
    'units': 16,
    'dropout_rate': 0.36852608614904786,
    'lr': 0.001787326642744812,
    'batch_size': 64
}

# Rebuild NN model architecture so that we can load pickled weights into it
def build_nn(input_dim, params):
    model = Sequential()
    # first layer (needs input_dim)
    model.add(Dense(params['units'],
                    activation='relu',
                    input_shape=(input_dim,)))
    model.add(Dropout(params['dropout_rate']))
    # remaining hidden layers
    for _ in range(params['n_layers'] - 1):
        model.add(Dense(params['units'], activation='relu'))
        model.add(Dropout(params['dropout_rate']))
    # output layer for binary classification
    model.add(Dense(1, activation='sigmoid'))

    model.compile(
        optimizer=Adam(learning_rate=params['lr']),
        loss='binary_crossentropy',
        metrics=['accuracy',
                 tf.keras.metrics.AUC(name='auc')]
    )
    return model

input_dim = diab_X.shape[1]
nn_model = build_nn(input_dim, nn_params)

with open('Diabetes_best_nn_weights.pkl', 'rb') as f:
    weights = pickle.load(f)

nn_model.set_weights(weights)

# The NN uses normalized data because it improves training stability. The XGBoost one does not, because Trees work just as well on features at different scales. So we create one normaized version of the data for the NN:
scaler = StandardScaler()
diab_X_proc = scaler.fit_transform(diab_X)

# Generate predictions from both models (probability of the positive class)
# We’ll use predict_proba and take the column [:, 1]
pred_xgb = xgb_model.predict_proba(diab_X)[:, 1]
pred_nn  = nn_model.predict(diab_X_proc).ravel()

# Stack the two prediction vectors into a 2 x <num_datapoints> matrix to train the pereceptron
meta_X = np.vstack([pred_xgb, pred_nn]).T
meta_y = diab_y.values

diab_X_train, diab_X_test, diab_y_train, diab_y_test = train_test_split(
    meta_X, meta_y, test_size=0.1, stratify=meta_y, random_state=42)

# Train the perecpetron:
meta_model = LogisticRegression(class_weight='balanced', random_state=42)
meta_model.fit(diab_X_train, diab_y_train)

# Predict class labels and probabilities on the test set
y_pred_proba = meta_model.predict_proba(diab_X_test)[:, 1]
y_pred      = meta_model.predict(diab_X_test)

# Compute performance scores
acc   = accuracy_score(diab_y_test, y_pred)
auc   = roc_auc_score(diab_y_test, y_pred_proba)

print(f"Test Accuracy : {acc:.4f}")
print(f"Test ROC AUC  : {auc:.4f}")

print("\nClassification Report:")
print(classification_report(diab_y_test, y_pred, digits=4))

cm = confusion_matrix(diab_y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)

print("Ensemble weights (log‑odds coefficients):", meta_model.coef_)