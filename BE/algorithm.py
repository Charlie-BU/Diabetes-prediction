import pandas as pd
import pickle
import warnings

warnings.filterwarnings('ignore')

DIABETES_MODEL = "./pkl/JJC_diabetes_prediction_xgboost_model.pkl"
HEART_DISEASE_MODEL = "./pkl/JJC_heartdisease_prediction_xgboost_model.pkl"
HYPERTENSION_MODEL = "./pkl/JJC_hypertension_prediction_xgboost_model.pkl"
OPTIMAL_THRESHOLD = 0.44398162


def preprocess_data(df):
    # Handle categorical variables
    df_processed = df.copy()
    # Handle gender
    df_processed['gender'] = df_processed['gender'].replace({'Female': 0, 'Male': 1, 'Other': 2})
    # Handle smoking_history
    smoking_map = {
        'never': 0,
        'No Info': 1,
        'current': 2,
        'former': 3,
        'ever': 4,
        'not current': 5
    }
    df_processed['smoking_history'] = df_processed['smoking_history'].map(smoking_map)
    return df_processed


def load_model(model_filename=DIABETES_MODEL):
    model = pickle.load(open(model_filename, 'rb'))
    return model


def start_predict(disease_type, sample_data):
    # 预处理输入数据
    if isinstance(sample_data, dict):
        # 如果输入是字典，转换为DataFrame
        sample_df = pd.DataFrame([sample_data])
        sample_df = preprocess_data(sample_df)
        sample = sample_df.values
    else:
        sample = sample_data
    match disease_type:
        case 'diabetes':
            model = load_model(DIABETES_MODEL)
        case 'heartdisease':
            model = load_model(HEART_DISEASE_MODEL)
        case 'hypertension':
            model = load_model(HYPERTENSION_MODEL)
        case _:
            raise Exception("Disease type not recognized")
    # 预测概率
    pred_proba = model.predict_proba(sample)[0, 1]
    # 使用最优阈值进行分类
    pred_class = 1 if pred_proba >= OPTIMAL_THRESHOLD else 0
    return {
        'probability': float(pred_proba),
        'prediction': int(pred_class),
        'risk_level': 'High' if pred_class == 1 else 'Low'
    }


if __name__ == '__main__':
    test_data = {
        'HbA1c_level': '2.21',
        'age': '12',
        'blood_glucose_level': '23',
        'bmi': '23.2',
        'gender': 'Female',
        'heart_disease': '0',
        'hypertension': '1',
        'smoking_history': 'current'
    }
    res = start_predict("diabetes", test_data)
    print(res)
