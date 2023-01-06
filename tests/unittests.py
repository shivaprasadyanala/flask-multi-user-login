import unittest
import requests
import jwt
import os


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"
    agent_logindata = {
        "email": "prasad@gmail.com",
        "password": "Prasad@123"
    }
    admin_logindata = {
        "email": "shiva@gmail.com",
        "password": "Shiva@123"
    }
    registerdata = {
        "email": "reddy@gmail.com",
        "password": "Reddy@123",
        "username": "reddy",
        "role": "agent"
    }
    agent_token = ""
    admin_token = ""

    def test_register(self):
        try:
            response = requests.post(
                self.URL+'/register', json=self.registerdata)
            self.assertEqual(response.status_code, 201)
            print("test 1 passed")
        except Exception as error:
            print("Test 1 failed"+str(error))

    def test_login(self):
        try:
            response = requests.post(
                self.URL+'/login', json=self.admin_logindata)
            self.assertEqual(response.status_code, 200)
            token = response.json()['token']
            data = jwt.decode(
                token, os.environ.get(
                    'SIGNING_KEY'), algorithms=['HS256'])
            if data['role'] == "admin":
                self.admin_token = token
            elif data['role'] == "agent":
                self.agent_token = token
            print("test 2 passed")
        except Exception as error:
            print("Test 2 failed "+str(error))

    def test_get_admin(self):
        try:
            resp = requests.get(self.URL+'/admin',
                                headers={"x-access-token": str(self.admin_token)})
            self.assertEqual(resp.status_code, 200)
            print("Test 3 passed")
        except Exception as error:
            print("Test 3 failed"+str(error))

    def test_get_agent(self):
        try:
            resp = requests.get(self.URL+'/agent',
                                headers={"x-access-token": self.agent_token})
            self.assertEqual(resp.status_code, 200)
            print("Test 4 passed")
        except Exception as error:
            print("Test 4 failed"+str(error))

    def test_get_users(self):
        try:
            resp = requests.get(self.URL+'/login',
                                headers={"x-access-token": str(self.admin_token)})
            self.assertEqual(resp.status_code, 200)
            print("Test 5 passed")
        except Exception as error:
            print("Test 5 failed"+str(error))


if __name__ == "__main__":
    tester = TestAPI()
    tester.test_login()
    tester.test_get_admin()
    tester.test_get_users()
    tester.test_get_agent()
    tester.test_register()
