try:
    import unittest, json
    from CarApi import collection_Users
    from controllers.UsersController import app 
    from bson import ObjectId
except Exception as e:
    print("Something went wrong when importing modules")
    
    

    
class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    
    def test_get_all_users(self):
        tester = app.test_client(self)
        response = tester.get("/all_users")
        statuscode = response.status_code
        
        self.assertEqual(statuscode, 200)
   
   
    def test_get_user_success(self):
        test_user_id = ObjectId()
        test_user_data ={
            "_id": test_user_id,
            "email": "testuser@test.test",
            "first_name": "testuser",
            "password": "test",
            "phone": 111222333,
            "second_name": "test",
            "user_privileges": "basicUser",
            "username": "testuser"
        }
        
        collection_Users.insert_one(test_user_data)
        response = self.app.get(f'/user/{test_user_id}')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)

        
        self.assertEqual(data['_id'], str(test_user_id))
        collection_Users.delete_one({"_id": test_user_id})
        
    def test_get_user_failure(self):
          test_user_id = ObjectId()
          test_user_data ={
              "_id": "invalidID",
              "email": "testuser@test.test",
              "first_name": "testuser",
              "password": "test",
              "phone": 111222333,
              "second_name": "test",
              "user_privileges": "basicUser",
              "username": "testuser"
          }
          
          collection_Users.insert_one(test_user_data)
          response = self.app.get(f'/user/{test_user_id}')
          
          self.assertEqual(response.status_code, 404)
          
          data = json.loads(response.data)

          collection_Users.delete_one({"_id": "invalidID"})
          
    def test_signUp_success(self):
        
        response = self.app.post(f'/user/signup', json = {
            "email": "testuser@test.test",
            "first_name": "testuser",
            "password": "test",
            "phone": 111222333,
            "second_name": "test",
            "user_privileges": "basicUser",
            "username": "testuser"
        })
        
        self.assertEqual(response.status_code, 201)
        
    def test_signUp_failure(self):
        
        #Response status code 400 expected as I try to add existing user
        response = self.app.post(f'/user/signup', json = {
            "email": "testuser@test.test",
            "first_name": "testuser",
            "password": "test",
            "phone": 111222333,
            "second_name": "test",
            "user_privileges": "basicUser",
            "username": "testuser"})
    
        self.assertEqual(response.status_code, 400)
        
    def test_login_success(self):
        #login with credentials that previous signup testcases added using username
        response = self.app.post(f'/user/login', json = {"usernameOrMail":"testuser", "password":"test"})
        self.assertEqual(response.status_code, 200)
        #login with credentials that previous signup testcases added using email
        response = self.app.post(f'/user/login', json = {"usernameOrMail":"testuser@test.test", "password":"test"})
        self.assertEqual(response.status_code, 200)
        
    def test_login_failure(self):
        #login with wrong password
        response = self.app.post(f'/user/login', json = {"usernameOrMail":"testuser", "password":"invalidPassword"})
        self.assertEqual(response.status_code, 401)
        #login with wrong username or mail
        response = self.app.post(f'/user/login', json = {"usernameOrMail":"testuser", "password":"invalidPassword"})
        self.assertEqual(response.status_code, 401)
        
    def test_logout_success(self):
        pass
        
        
if __name__ == '__main__':
    unittest.main()