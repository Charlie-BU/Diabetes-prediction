from sqlalchemy import create_engine, ForeignKey, Boolean, Column, Integer, Text, DateTime, Date, Float, JSON
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.mutable import MutableList

from config import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=True)
# 数据库表基类
Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata.naming_convention = naming_convention
# 会话，用于通过ORM操作数据库
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    gender = Column(Integer, nullable=True)
    age = Column(Integer, nullable=True)
    hypertension = Column(Boolean, nullable=True)
    heart_disease = Column(Boolean, nullable=True)
    smoking_history = Column(Integer, nullable=True)
    bmi = Column(Float, nullable=True)
    HbA1c_level	 = Column(Float, nullable=True)
    blood_glucose_level = Column(Integer, nullable=True)
    diabetes = Column(Boolean, nullable=True)

    def to_json(self):
        data = {
            "id": self.id,
            "gender": self.gender,
            "age": self.age,
            "hypertension": self.hypertension,
            "heart_disease": self.heart_disease,
            "smoking_history": self.smoking_history,
            "bmi": self.bmi,
            "HbA1c_level": self.HbA1c_level,
            "blood_glucose_level": self.blood_glucose_level,
            "diabetes": self.diabetes,
        }
        return data



# 创建所有表（被alembic替代）
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
