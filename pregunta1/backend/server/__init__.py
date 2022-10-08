from ast import Del
from crypt import methods
from hashlib import new
import json

from flask import (
    Flask,
    abort,
    jsonify,
    request
)

from flask_cors import CORS
from models import setup_db, Planta, Delivery, db

PLANTAS_PER_PAGE=5


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    #TODO
    

    @app.after_request
    def after_resquest(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true') # Decimos, que headers permitimos al cliente
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PATCH, PUT, DELETE') # Metodos que se permiten
        return response # Retornamos todo ello  

    #---------------Plantas---------------
    @app.route('/plantas', methods=['GET'])
    def get_plantas():
        page = request.args.get('page', 1, type=int)
        plantas = Planta.query.order_by('id').limit(PLANTAS_PER_PAGE).offset((page-1)*PLANTAS_PER_PAGE).all()
        total_plantas = Planta.query.count()

        if len(plantas) == 0:
            abort(404)

        return jsonify({ 
            'success': True,
            'plantas': [planta.format() for planta in plantas], 
            'total_plantas': total_plantas
        })  

    @app.route('/plantas', methods=['POST'])
    def create_planta():
        body = request.get_json()
        nombre = body.get('nombre', None)
        precio = body.get('precio', None)
        alto = body.get('alto', None)
        ancho = body.get('ancho', None)
        color = body.get('color', None)
        delivery_id = body.get('delivery_id', None)
        search = body.get('search', None)

        if search:
            plantas = Planta.query.order_by('plant_id').filter(Planta.nombre.like('%{}%'.format(search))).all() # VEERLOOOOOOO
            return jsonify({ 
                'success': True,
                'plantas': [planta.format() for planta in plantas], 
                'total_plantas': len(plantas)
            })
        else:
            if 'nombre' not in body:
                abort(422)

            if 'plant_id' not in body:
                abort(422)
            
            response = {}
            try:
                planta = Planta(nombre=nombre, precio=precio, alto=alto, ancho=ancho, color=color, delivery_id=delivery_id)
                response['success'] = True
                created_id = planta.insert()
                planta.id = created_id
                response['planta'] = planta.format()

            except Exception as e:
                response['success'] = False
                print(e)
                abort(500)

            return jsonify(response)
    
    @app.route('/plantas/<planta_id>', methods=['PATCH'])
    def update_planta(planta_id):
        response = {}
        try:
            planta = Planta.query.get(planta_id)
            if planta is None:
                abort(404)

            body = request.get_json()
            if 'nombre' in body:
                planta.nombre = body.get('nombre', '')

            if 'precio' in body:
                planta.precio = body.get('precio', False)

            if 'precio' in body:
                planta.precio = body.get('precio', False)
            
            if 'alto' in body:
                planta.alto = body.get('alto', False)
            
            if 'ancho' in body:
                planta.ancho = body.get('ancho', False)
            
            if 'color' in body:
                planta.color = body.get('color', False)

            if 'delivery_id' in body:
                planta.delivery_id = body.get('delivery_id', 1)
            
            response['success'] = True
            response['planta'] = planta.format()

            error = planta.update()
            if error:
                abort(422)
            
        except Exception as e:
            response['success'] = False
            print(e)
            if error:
                abort(500)

        return jsonify(response)

    @app.route('/plantas/<planta_id>', methods=['DELETE'])
    def delete_planta_by_id(planta_id):
        error_404 = False
        try:
            planta = Planta.query.get(planta_id)
            if planta is None: 
                error_404 = True 
                raise Exception

            planta.delete() 

            return jsonify({
                'success': True,
                'deleted': planta_id, 
                'total_plantas': Planta.query.count()
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/plantas/under-price/<price>', methods=['GET'])
    def plants_cheaper_than(price):
        #TODO
        return jsonify({})

    #---------------Delivery---------------
    @app.route('/deliveries', methods=['GET'])
    def get_deliveries():
        error_404 = False
        try:
            deliverys = {delivery.plant_id: {'id': delivery.plant_id, 'nombre': delivery.nombre, 'precio':delivery.precio, 'alto':delivery.alto,'ancho':delivery.ancho,'color':delivery.color} for delivery in Delivery.query.order_by('delivery_id').all()}
        
            if len(deliverys) == 0:
                error_404 = True
                raise Exception

            return jsonify({
                'success': True,
                'categories': deliverys,
                'total_categories': len(deliverys)
            })
        
        except Exception as e:
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/deliveries', methods=['POST'])
    def create_delivery():
        confict_409 = False
        try:
            body = request.get_json()
            nombre = body.get('nombre', None)

            if nombre in [None, '']:
                abort(422)

            exist_delivery = Delivery.query.filter_by(nombre=nombre).one_or_none()

            if exist_delivery:
                confict_409 = True
                raise Exception

            new_delivery = Delivery(nombre=nombre)
            delivery_id = new_delivery.insert()
            
            return jsonify({
                'success': True,
                'created': delivery_id
            })

        except Exception as e:
            print(e)
            if confict_409:
                abort(409)
            else:
                abort(422)

    
    @app.route('/deliveries/<delivery_id>', methods=['PATCH'])
    def update_delivery(delivery_id):
        #TODO
        return jsonify({})


    @app.route('/deliveries/<delivery_id>', methods=['DELETE'])
    def delete_delivery_by_id(delivery_id):
        error_404 = False
        try:
            delivery = Delivery.query.get(delivery_id)
            if delivery is None:
                error_404 = True
                raise Exception

            plantas = delivery.todos
            for planta in plantas:
                planta.delete() # Se a eleminado todos los hijos de ese padre, osea 'todo' es el hijo
                              # Ojo este delete esta en la clase de todo
            delivery.delete() # Este otro delete esta en la clase Category.
            # De acuerdo a ello que se a eliminado una categoria.

        except Exception as e:
            print(e)   
            if error_404:
                abort(404)
            else:
                abort(500) 

        return jsonify({
            'success': True
        })


    @app.route('/deliveries/<delivery_id>', methods=['GET'])
    def get_bill(delivery_id):
        #TODO
        return jsonify({})


    return app
