import unittest

from server import create_app
from models import setup_db,Planta,Delivery
import json
import random
class TestPlantaApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = 'plantdb_test'
        self.path = 'postgresql://{}:1234@{}/{}'.format('francko', 'localhost', self.database_name)
        setup_db(self.app, self.path)

        self.new_planta = {
            'nombre': 'new nombre',
            'completed': False
        }

        self.client.delete('/deliverys')
    #---------------Planta---------------
    def test_post_planta_success_200(self):
        random_delivery_str = "sindelivery{}".format(random.choice([x for x in range(1000)]))
        response = self.client.post('/deliveries', json={'nombre': random_delivery_str})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_get_planta_success_200(self):
        pass

    def test_get_planta_failed_404(self):
        pass

    def test_post_planta_failed_422(self):
        pass

    def test_patch_planta_color_sucess_200(self):
        pass

    def test_patch_planta_failed_422(self):
        pass

    def test_delete_planta_success_200(self):
        pass

    def test_delete_planta_failed_404(self):
        pass

    def test_get_under_price_50_success_200(self):
        pass

    def test_get_above_price_50_failed_404(self):
        pass

    #---------------Delivery---------------
    def test_get_deliveries_success_200(self):
        pass

    def test_get_deliveries_failed_404(self):
        pass

    def test_post_delivery_success_200(self):
        pass

    def test_post_delivery_failed_422(self):
        pass

    def test_patch_delivery_color_sucess_200(self):
        pass

    def test_patch_delivery_failed_422(self):
        pass

    def test_delete_delivery_success_200(self):
        pass

    def test_delete_delivery_failed_404(self):
        pass

    def test_get_bill_success_200(self):
        pass

    def test_get_bill_failed_404(self):
        pass


    def tearDown(self):
        pass
