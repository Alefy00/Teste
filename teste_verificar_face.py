import unittest
from unittest.mock import patch
from celere import verificar_face
import requests

class TestVerificarFace(unittest.TestCase):
    def test_verificar_face_autorizado(self):
        # Mock para simular uma resposta bem-sucedida da API
        with patch('celere.requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {'authorized': True}

            resultado = verificar_face('teste.jpg')

        self.assertTrue(resultado)

    def test_verificar_face_nao_autorizado(self):
        # Mock para simular uma resposta bem-sucedida da API, mas usuário não autorizado
        with patch('celere.requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {'authorized': False}

            resultado = verificar_face('teste.jpg')

        self.assertFalse(resultado)

    def test_verificar_face_erro_api(self):
        # Mock para simular um erro na requisição à API
        with patch('celere.requests.post') as mock_post:
            mock_post.side_effect = requests.exceptions.RequestException("Erro na requisição")

            resultado = verificar_face('teste.jpg')

        self.assertFalse(resultado)

    def test_verificar_face_erro_generico(self):
        # Mock para simular um erro genérico
        with patch('celere.requests.post') as mock_post:
            mock_post.return_value.status_code = 500

            resultado = verificar_face('teste.jpg')

        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()
