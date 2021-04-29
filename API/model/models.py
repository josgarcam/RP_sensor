from model import db

from sqlalchemy import Column, Integer, Float, DateTime


class DHT11(db.Base):
    __tablename__ = 'agricultura'

    id_measurement = Column(Integer, primary_key=True)
    id_rp = Column(Integer)
    id_sensor = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    measured_date = Column(DateTime)
    save_date = Column(DateTime)
