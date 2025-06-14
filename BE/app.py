from robyn import Robyn, ALLOW_CORS, jsonify

from algorithm import start_predict
from models import session, Patient

app = Robyn(__file__)
ALLOW_CORS(app, origins=["*"])


@app.get("/")
async def index():
    return "HELLO FROM DIABETES PREDICTION BACKEND"


@app.get("/api/getPatientData")
async def getPatientData(request):
    params = request.query_params.to_dict()
    try:
        query = session.query(Patient)
        page = params.get("page")[0]
        pageSize = params.get("pageSize")[0]

        gender = params.get("gender")[0] if params.get("gender") and params.get("gender")[0] != "null" else None
        ageMin = params.get("ageMin")[0] if params.get("ageMin") and params.get("ageMin")[0] != "null" else None
        ageMax = params.get("ageMax")[0] if params.get("ageMax") and params.get("ageMax")[0] != "null" else None
        hypertension = params.get("hypertension")[0] if params.get("hypertension") and params.get("hypertension")[
            0] != "null" else None
        heart_disease = params.get("heart_disease")[0] if params.get("heart_disease") and params.get("heart_disease")[
            0] != "null" else None
        smoking_history = params.get("smoking_history")[0] if params.get("smoking_history") and \
                                                              params.get("smoking_history")[0] != "null" else None
        smoking_history = smoking_history.replace("+", " ") if smoking_history else None
        bmiMin = params.get("bmiMin")[0] if params.get("bmiMin") and params.get("bmiMin")[0] != "null" else None
        bmiMax = params.get("bmiMax")[0] if params.get("bmiMax") and params.get("bmiMax")[0] != "null" else None
        HbA1c_levelMin = params.get("HbA1c_levelMin")[0] if params.get("HbA1c_levelMin") and \
                                                            params.get("HbA1c_levelMin")[0] != "null" else None
        HbA1c_levelMax = params.get("HbA1c_levelMax")[0] if params.get("HbA1c_levelMax") and \
                                                            params.get("HbA1c_levelMax")[0] != "null" else None
        blood_glucose_levelMin = params.get("blood_glucose_levelMin")[0] if params.get("blood_glucose_levelMin") and \
                                                                            params.get("blood_glucose_levelMin")[
                                                                                0] != "null" else None
        blood_glucose_levelMax = params.get("blood_glucose_levelMax")[0] if params.get("blood_glucose_levelMax") and \
                                                                            params.get("blood_glucose_levelMax")[
                                                                                0] != "null" else None
        diabetes = params.get("diabetes")[0] if params.get("diabetes") and params.get("diabetes")[0] != "null" else None
        if gender:
            query = query.filter(Patient.gender == gender)
        if ageMin:
            query = query.filter(Patient.age >= int(ageMin))
        if ageMax:
            query = query.filter(Patient.age <= int(ageMax))
        if hypertension:
            query = query.filter(Patient.hypertension == hypertension)
        if heart_disease:
            query = query.filter(Patient.heart_disease == heart_disease)
        if smoking_history:
            query = query.filter(Patient.smoking_history == smoking_history)
        if bmiMin:
            query = query.filter(Patient.bmi >= bmiMin)
        if bmiMax:
            query = query.filter(Patient.bmi <= bmiMax)
        if HbA1c_levelMin:
            query = query.filter(Patient.HbA1c_level >= HbA1c_levelMin)
        if HbA1c_levelMax:
            query = query.filter(Patient.HbA1c_level <= HbA1c_levelMax)
        if blood_glucose_levelMin:
            query = query.filter(Patient.blood_glucose_level >= blood_glucose_levelMin)
        if blood_glucose_levelMax:
            query = query.filter(Patient.blood_glucose_level <= blood_glucose_levelMax)
        if diabetes:
            query = query.filter(Patient.diabetes == diabetes)

        total = query.count()
        patients = query.offset((int(page) - 1) * int(pageSize)) \
            .limit(pageSize) \
            .all()
        return jsonify({
            "status": 200,
            "message": "Success",
            "patients": [patient.to_json() for patient in patients] if len(patients) != 0 else [],
            "total": total,
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": 500,
            "message": "Fail",
        })


@app.post("/api/predict")
async def predict(request):
    params = request.query_params.to_dict()
    disease = params["disease"][0]
    data = request.json()
    result = start_predict(disease, data)
    return jsonify({
        "status": 200,
        "message": "Success",
        "result": result
    })


# def data_transfer2():
#     import pandas as pd
#     df = pd.read_csv('dataset1.csv')
#     count = fail_count = 0
#     fields = ["gender", "age", "hypertension", "heart_disease", "smoking_history", "bmi", "HbA1c_level",
#               "blood_glucose_level", "diabetes"]
#     for _, row in df.iterrows():
#         try:
#             data = {field: row.get(field) for field in fields}
#             patient = Patient(**data)
#             session.add(patient)
#             count += 1
#             print(f"进行第{count}项")
#         except Exception as e:
#             fail_count += 1
#     session.commit
#     print(f"成功{count}项，失败{fail_count}项")


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=6060)
