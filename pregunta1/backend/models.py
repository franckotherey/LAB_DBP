from email.policy import default
from flask_sqlalchemy import SQLAlchemy

database_name='plantdb'
database_path='postgresql://{}:1234@{}/{}'.format('francko', 'localhost', database_name)
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    db.create_all()


class Planta(db.Model): # Hijo

    __tablename__ = "Plantas"
    plant_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), nullable = False)
    precio = db.Column(db.Float, nullable = False)
    alto = db.Column(db.Float, nullable = False)
    ancho = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(), nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('Deliverys.delivery_id'),nullable=False) # FALTA IMPLEMENTAR
    '''
    propiedades:
    
    PK planta id
    nombre
    precio
    alto
    ancho
    color
    FK delivery id
    '''
    def format(self):
        return {
            'id': self.plant_id,
            'nombre': self.nombre,
            'precio': self.precio,
            'alto': self.alto,
            'ancho': self.ancho,
            'color':self.color,
            'delivery_id': self.delivery_id
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.plant_id
        except:
            db.session.rollback()
        finally:
            db.session.close()
        
        return created_id

    def update(self):
        error = False
        try:
            print('self: ', self)
            db.session.commit()
        except Exception as e:
            print('error: ', e)
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        return error

    def delete(self):
        print('delete->>>>>!!!!!!!!!!!!!!!')
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


class Delivery(db.Model): # Padre
    
    __tablename__ = "Deliverys"
    delivery_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), nullable = False)
    direccion = db.Column(db.String(), nullable=False)
    horario = db.Column(db.String(), nullable=False)
    completado = db.Column(db.Boolean, nullable=False, default=False)
    plantas = db.relationship('Planta', backref='Plantas', lazy=True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.delivery_id
        except:
            db.session.rollback()
        finally:
            db.session.close()
        
        return created_id

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()

    '''
    propiedades:

    PK delivery id
    nombre
    direccion
    horario
    completado
    '''
