import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.pipeline import Pipeline
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import optuna
from optuna.integration import TFKerasPruningCallback
from sklearn.neighbors import KNeighborsClassifier
from imblearn.combine import SMOTEENN
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, accuracy_score 
import matplotlib.pyplot as plt

df = pd.read_csv('diabetes_prediction_dataset.csv')

df['gender'] = df['gender'].replace({'Female': 0, 'Male': 1, 'Other': 2})

smoking_map = {
    'never': 0,
    'No Info': 1,
    'current': 2,
    'former': 3,
    'ever': 4,
    'not current': 5
}
df['smoking_history'] = df['smoking_history'].map(smoking_map)

# Build KNN model:
diab_X = df.drop('diabetes', axis=1)
diab_y = df["diabetes"]

# diab_X_train, diab_X_test, diab_y_train, diab_y_test = train_test_split(
#     diab_X, diab_y, test_size=0.1, stratify=diab_y, random_state=42)

# We used this train, val test split during hyper parameter search
diab_X_train, diab_X_testval, diab_y_train, diab_y_testval = train_test_split(
    diab_X, diab_y, test_size=0.2, stratify=diab_y, random_state=42)
diab_X_test, diab_X_val, diab_y_test, diab_y_val = train_test_split(
    diab_X_testval, diab_y_testval, test_size=0.5, stratify=diab_y_testval, random_state=42)

numeric_features = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
diab_categorical_features = ['gender','hypertension','heart_disease', 'smoking_history']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), diab_categorical_features)
])

knn_pipeline = ImbPipeline([
    ('pre', preprocessor),
    ('resample', SMOTEENN(random_state=42)),
    ('knn', KNeighborsClassifier(n_neighbors=9, weights='uniform', p=1))
    # ('knn', KNeighborsClassifier()) # <- used during hyperparameter search
])

# # We used this to optimize the hyper parameters of the KNN
# # Define hyperparameter grid for KNN
# grid_params = {
#     'knn__n_neighbors': [3,5,7,9],
#     'knn__weights': ['uniform','distance'],
#     'knn__p': [1,2]  # 1=Manhattan, 2=Euclidean
# }

# # Compute class weights if imbalance is severe (optional for KNN)
# # scikit-learn KNN does not accept class_weight, but you can incorporate via sample_weight in fit.

# # Grid search with stratified validation
# grid_search = GridSearchCV(
#     knn_pipeline,
#     grid_params,
#     cv=5,
#     scoring='roc_auc',
#     n_jobs=-1,
#     error_score = 'raise'
# )

# # Fit on train set
# grid_search.fit(diab_X_train, diab_y_train)
# print("Best KNN params:", grid_search.best_params_)
# print(f"Validation AUC: {grid_search.best_score_:.4f}")

# # Evaluate on val set
# test_auc_knn = grid_search.score(diab_X_val, diab_y_val)
# print(f"Test AUC (KNN): {test_auc_knn:.4f}")


knn_pipeline.fit(diab_X_train, diab_y_train)

X_val_pre = diab_X_test
y_pred_knn = knn_pipeline.predict(diab_X_test)
y_pred_proba_knn = knn_pipeline.predict_proba(diab_X_test)[:,1]

print("Diabetes Classification Report (KNN):")
print(classification_report(diab_y_test, y_pred_knn))
print("Diabetes Confusion Matrix (KNN):")
print(confusion_matrix(diab_y_test, y_pred_knn))

# ROC Curve for KNN
fpr_k, tpr_k, _ = roc_curve(diab_y_test, y_pred_proba_knn)
roc_auc_k = auc(fpr_k, tpr_k)
plt.figure()
plt.plot(fpr_k, tpr_k, label=f"AUC={roc_auc_k:.3f}")
plt.plot([0,1],[0,1],'--')
plt.xlabel('FPR'); plt.ylabel('TPR'); plt.title('Diabetes KNN ROC Curve'); plt.legend(); plt.show()


# Normalize features
scaler = StandardScaler()
type(diab_X)
# X_scaled = scaler.fit_transform(X)
X_train_proc = scaler.fit_transform(diab_X_train)
X_test_proc = scaler.fit_transform(diab_X_test)

# Compute class weights to handle imbalance
y_classes = np.unique(diab_y_train)
class_weights = compute_class_weight(
    class_weight='balanced', classes=y_classes, y=diab_y_train)
class_weight_dict = {cls: w for cls, w in zip(y_classes, class_weights)}
print("Class weights:", class_weight_dict)

# # We used this for hpyer parameter optimization of the NN with Optuna
# X_val_proc = scaler.fit_transform(diab_X_val)

# def create_model(trial):
#     # Hyperparameters to tune
#     n_layers = trial.suggest_int('n_layers', 1, 3)
#     units = trial.suggest_categorical('units', [8, 16, 32, 64])
#     dropout_rate = trial.suggest_float('dropout_rate', 0.0, 0.5)
#     lr = trial.suggest_loguniform('lr', 1e-4, 1e-2)

#     model = Sequential()
#     model.add(Dense(units, activation='relu', input_shape=(diab_X_train.shape[1],)))
#     model.add(Dropout(dropout_rate))
#     for _ in range(n_layers - 1):
#         model.add(Dense(units, activation='relu'))
#         model.add(Dropout(dropout_rate))
#     model.add(Dense(1, activation='sigmoid'))

#     optimizer = Adam(learning_rate=lr)
#     model.compile(
#         optimizer=optimizer,
#         loss='binary_crossentropy',
#         metrics=[tf.keras.metrics.AUC(name='auc')]
#     )
#     return model

# def objective(trial):
#     model = create_model(trial)
#     callbacks = [
#         EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
#         TFKerasPruningCallback(trial, 'val_loss')
#     ]
#     history = model.fit(
#         diab_X_train, diab_y_train,
#         validation_data=(diab_X_val, diab_y_val),
#         epochs=100,
#         batch_size=trial.suggest_categorical('batch_size', [32, 64, 128]),
#         callbacks=callbacks,
#         class_weight=class_weight_dict,
#         verbose=0
#     )
#     # Evaluate on validation set
#     val_auc = model.evaluate(diab_X_val, diab_y_val, verbose=0)[1]
#     return val_auc

# # Create study and optimize
# study = optuna.create_study(direction='maximize', study_name='binary_classifier')
# study.optimize(objective, n_trials=50, timeout=600)

# print("Best trial:")
# best = study.best_trial
# print(f"  AUC: {best.value}")
# for key, val in best.params.items():
#     print(f"  {key}: {val}")

X = diab_X
X_train = diab_X_train
y_train = diab_y_train
X_test = diab_X_test
y_test = diab_y_test
test_name = "Diabetes"

nn_params = {
    'n_layers': 2,
    'units': 16,
    'dropout_rate': 0.36852608614904786,
    'lr': 0.001787326642744812,
    'batch_size': 64
}

model = Sequential()
model.add(Dense(nn_params['units'], activation='relu', input_shape=(X_train_proc.shape[1],)))
model.add(Dropout(nn_params['dropout_rate']))
for _ in range(nn_params['n_layers'] - 1):
    model.add(Dense(nn_params['units'], activation='relu'))
    model.add(Dropout(nn_params['dropout_rate']))
model.add(Dense(1, activation='sigmoid'))

model.compile(
    optimizer=Adam(learning_rate=nn_params['lr']),
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
)

history = model.fit(
    X_train_proc, y_train,
    validation_data=(X_test_proc, y_test),
    epochs=100,
    batch_size=nn_params['batch_size'],
    class_weight=class_weight_dict,
    callbacks=[EarlyStopping('val_loss', patience=5, restore_best_weights=True)],
    verbose=1
)

# Save weights
weights = model.get_weights()
filename = test_name + "_best_nn_weights.pkl"
with open(filename, 'wb') as f:
    pickle.dump(weights, f)
print(f"Saved NN weights to {test_name}_best_nn_weights.pkl")

# Predictions and metrics on validation set
y_pred_proba_nn = model.predict(X_test_proc).ravel()
y_pred_nn = (y_pred_proba_nn >= 0.5).astype(int)
print(f"\n{test_name} Neural Network Performance on Validation Set:")
print(classification_report(y_test, y_pred_nn))
print(f"{test_name} Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_nn))

ROC_title = test_name + " Neural Network ROC Curve"
# ROC curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba_nn)
roc_auc = auc(fpr, tpr)
plt.figure()
plt.plot(fpr, tpr, label=f"AUC={roc_auc:.3f}")
plt.plot([0,1],[0,1],'--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title(ROC_title)
plt.legend()
plt.show()

Loss_title = test_name + " NN Loss Curves"
# Loss and Accuracy Curves
plt.figure()
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title(Loss_title)
plt.show()

Accuracy_title = test_name + " NN Accuracy Curves"
plt.figure()
plt.plot(history.history['accuracy'], label='train_acc')
plt.plot(history.history['val_accuracy'], label='val_acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title(Accuracy_title)
plt.show()