from model.models import DHT11
from model import db
from datetime import datetime


def record(request):
    try:
        session = db.Session()
        db.Base.metadata.create_all(db.engine)
        ob = DHT11(save_date=datetime.now(),
                   measured_date=request.form.get("measured_date"),
                   id_rp=request.form.get("id_rp"),
                   id_sensor=request.form.get("id_sensor"),
                   temperature=request.form.get("temperature"),
                   humidity=request.form.get("humidity"))
        
        
        session.add(ob)
        session.commit()
        
        return str(ob.measured_date), 200
        
        
    except:
        try:
            session.close()
        except:
            pass
        finally:
            return 'Error', 500
    
    



def read(id_rp, id_sensor):
    db.Base.metadata.create_all(db.engine)
    ob = db.session.query(DHT11).filter(DHT11.id_rp == id_rp).filter(DHT11.id_sensor == id_sensor).all()
    i = 0
    data = {}

    for obj in ob:
        data[i] = {'save_date': obj.save_date,
                   'measured_date': obj.measured_date,
                   'id_rp': obj.id_rp,
                   'id_sensor': obj.id_sensor,
                   'temperature': obj.temperature,
                   'humidity': obj.humidity
                   }
        i += 1

    return (data)