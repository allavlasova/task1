# -*- coding: utf-8 -*-
__author__ = 'alla'
import noseapp
from noseapp_requests import RequestsEx, make_config
from requests import HTTPError
from utils import make_result

suite = noseapp.Suite(__name__)

@suite.register
class TestCase(noseapp.TestCase):

    def setUp(self):
        endpoint = make_config()
        endpoint.configure(
            base_url='http://127.0.0.1:5000',
            key='target-test'
        )
        endpoint.session_configure(
            always_return_json=True,
            raise_on_http_error=True
        )
        self.requests_ex = RequestsEx(endpoint)
        self.api = self.requests_ex.get_endpoint_session('target-test')

    #---------------Post-----------------------------
    #отправляем корректный запрос
    def test_post_200OK(self):
        key = 'key'
        value = 'val'
        self.assertEquals(make_result(value), self.api.post('/dictionary/',{'key': key, 'value': value}))
        self.api.delete('/dictionary/',{'key': key})

    #отправляем запрос в котором отсутствует одно из полей
    def test_post_400(self):
        key = 'key'
        value = 'val'
        with self.assertRaises(HTTPError):
            self.api.post('/dictionary/',{'key': key})
        with self.assertRaises(HTTPError):
            self.api.post('/dictionary/',{'value': value})

    #отправляем запрос с уже существующим ключом
    def test_post_409(self):
        key = 'key'
        value = 'val'
        self.api.post('/dictionary/',{'key': key , 'value': value})
        with self.assertRaises(HTTPError):
            self.api.post('/dictionary/',{'key': key , 'value': value})
        self.api.delete('/dictionary/',{'key': key})

    #---------------DELETE-----------------------------
    #корректный запрос на удаление
    def test_delete_200OK(self):
        key = 'key1'
        value = 'val1'
        self.api.post('/dictionary/',{'key': key , 'value': value})
        self.assertEquals(make_result(None), self.api.delete('/dictionary/',{'key': key}))

    #запрос на удаление по не существующему ключу
    def test_delete_200OK_bad_kee(self):
        self.assertEquals(make_result(None), self.api.delete('/dictionary/',{'key': 'bad_key'}))

    #некорректный запрос на удаление
    def test_delete_404(self):
        with self.assertRaises(HTTPError):
            self.api.delete('/dictionary/',{'key1': 'bad_key'})

    #---------------PUT-----------------------------

    def test_put_200OK(self):
        key = 'key1'
        value = 'val1'
        new_value = 'new_val1'
        self.api.post('/dictionary/',{'key': key , 'value': value})
        self.assertEquals(make_result(new_value), self.api.put('/dictionary/',{'key': key, 'value': new_value}))
        self.api.delete('/dictionary/',{'key': key})

    def test_put_400(self):
        key = 'key1'
        value = 'val1'
        with self.assertRaises(HTTPError):
            self.api.put('/dictionary/',{'key': key})
        with self.assertRaises(HTTPError):
            self.api.put('/dictionary/',{'value': value})

    def test_put_404(self):
        key = 'key1'
        value = 'val1'
        with self.assertRaises(HTTPError):
            self.api.put('/dictionary/',{'key': key, 'value': value})


    #---------------GET-----------------------------
    #Запрашиваем ключ который существует
    def test_get_200(self):
        key = 'key1'
        value = 'val1'
        self.api.post('/dictionary/',{'key': key , 'value': value})
        self.assertEquals(make_result(value), self.api.get('/dictionary/',key= key))
        self.api.delete('/dictionary/',{'key': key})

    #Запрашиваем несуществующий ключ
    def test_get_404(self):
        key = 'key1'
        with self.assertRaises(HTTPError):
            self.api.get('/dictionary/',key= key)


test_app = noseapp.NoseApp(__name__)
test_app.register_suite(suite)

if __name__ == '__main__':
    test_app.run()