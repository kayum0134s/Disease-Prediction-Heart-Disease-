"""
CardioPredict — SQLite Patient History Database
"""
import os
import json
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, Text
)
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(__file__), 'cardiopredict.db')
engine  = create_engine(f'sqlite:///{DB_PATH}', connect_args={'check_same_thread': False})
Base    = declarative_base()
Session = sessionmaker(bind=engine)


class Patient(Base):
    __tablename__ = 'patients'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(100), nullable=False)
    age         = Column(Integer)
    sex         = Column(String(10))
    inputs_json = Column(Text)        # JSON string of all raw inputs
    prediction  = Column(Integer)     # 0 or 1
    risk_score  = Column(Float)       # 0.0–100.0
    risk_label  = Column(String(30))
    rf_prob     = Column(Float)
    lr_prob     = Column(Float)
    svm_prob    = Column(Float)
    recommendations = Column(Text)    # JSON list
    timestamp   = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'name':         self.name,
            'age':          self.age,
            'sex':          'Male' if self.sex == '1' else 'Female',
            'prediction':   self.prediction,
            'risk_score':   self.risk_score,
            'risk_label':   self.risk_label,
            'rf_prob':      self.rf_prob,
            'lr_prob':      self.lr_prob,
            'svm_prob':     self.svm_prob,
            'inputs':       json.loads(self.inputs_json or '{}'),
            'recommendations': json.loads(self.recommendations or '[]'),
            'timestamp':    self.timestamp.strftime('%Y-%m-%d %H:%M') if self.timestamp else '',
        }


def init_db():
    Base.metadata.create_all(engine)


def save_patient(name, inputs, result):
    """Save a prediction result to the database."""
    session = Session()
    per_model = result.get('per_model', {})
    patient = Patient(
        name        = name,
        age         = inputs.get('age'),
        sex         = str(inputs.get('sex', '')),
        inputs_json = json.dumps(inputs),
        prediction  = result.get('prediction'),
        risk_score  = result.get('risk_score'),
        risk_label  = result.get('risk_label'),
        rf_prob     = per_model.get('Random Forest', {}).get('probability'),
        lr_prob     = per_model.get('Logistic Regression', {}).get('probability'),
        svm_prob    = per_model.get('SVM', {}).get('probability'),
        recommendations = json.dumps(result.get('recommendations', [])),
    )
    session.add(patient)
    session.commit()
    pid = patient.id
    session.close()
    return pid


def get_all_patients():
    session = Session()
    patients = session.query(Patient).order_by(Patient.timestamp.desc()).all()
    result = [p.to_dict() for p in patients]
    session.close()
    return result


def get_patient_by_id(pid):
    session = Session()
    patient = session.query(Patient).filter(Patient.id == pid).first()
    result = patient.to_dict() if patient else None
    session.close()
    return result
