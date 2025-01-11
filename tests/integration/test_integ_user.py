import pytest
from django.test import Client 

BASE_URL = "localhost:8000"
class testUsers_integration():
    def setup_module(module):
        pass

    def teardown_module(module):
        pass

    def test_get_posts(client):
        response = client.get(f"{BASE_URL}/api/users")
        assert response.status_code in [200,201]
        assert isinstance(response.get_json(), list)
    
    def test_user_by_id(client):
        user_id = 3
        response = client.get(f"{BASE_URL}/api/users/{user_id}")
        assert response.status_code in [200,201,202,203,204,205]

    # def test_create_user(client):
    #     new_user = {
    #         "userName": "",
    #         "email": "New Post Title",
    #         "first-name": "This is the body of the new post"
    #         "last-name": "This is the body of the new post"
    #     }
    #     response = client.post(f"{BASE_URL}/api/posts", json=new_post)
    #     assert response.status_code == 201
    #     response_data = response.get_json()
    #     assert response_data["userId"] == new_post["userId"]
    #     assert response_data["title"] == new_post["title"]
    #     assert response_data["body"] == new_post["body"]
    
