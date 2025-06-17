reformat.py
This script converts the "Physical_Examination_Data.xlsx" (needs to be in the same directory) file into one that is a close as I could get it to the Kaggle dataset. It exports the new file as "reformed_file.xlsx" and prints statistics and generates plots about the features.

NNandKNN.py
Contains the code for the hyper parameter tuning (commented out) and the NN model training and KNN and NN performance on the test dataset. Exports the NN model weights as a .pkl file.

train_ensemble.py
Loads the diabetes XGBoost model and NN model .pkl files (have to be in the same directory) and trains a perceptron to combine their predictions.

JJC_Final_Project.ipynb  
Contains the code for exploratory data analysis and XGBoost model for Diabetes with hyperparameter tuning optimised for AUC but without managing class imbalance.  
JJC_Final_Project_HeartDisease.ipynb  
Contains the code for XGBoost model for Heart Disease with hyperparameter tuning optimised for AUC but without managing class imbalance.  
JJC_Final_Project_Hypertension.ipynb  
Contains the code for XGBoost model for Hypertension with hyperparameter tuning optimised for AUC but without managing class imbalance.  

JJC2_Final_Project.ipynb  
Contains the code for exploratory data analysis and XGBoost model for Diabetes with hyperparameter tuning optimised for F1 and management of class imbalance.  
JJC2_Final_Project_HeartDisease.ipynb  
Contains the code for XGBoost model for Heart Disease with hyperparameter tuning optimised for AUC and management of class imbalance.  
JJC2_Final_Project_Hypertension.ipynb  
Contains the code for XGBoost model for Hypertension with hyperparameter tuning optimised for AUC and management of class imbalance.  
