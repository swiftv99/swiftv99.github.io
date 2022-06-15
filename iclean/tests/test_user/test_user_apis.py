import json
import pytest

from apps.user.models import User


@pytest.mark.django_db
class TestUserEndpoints:

    endpoint = '/users/'

    def test_list(self, api_client, user_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, user_create):
        
        expected_json = {
            'email': user_create.email,
            'role': user_create.role.role,
            'phone': user_create.phone,
            'country': user_create.country,
            'city': user_create.city,
            'is_staff': user_create.is_staff,
            'is_active': user_create.is_active,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["email"] == expected_json["email"]
        assert json.loads(response.content)["role"] == expected_json["role"]
        assert json.loads(response.content)["phone"] == expected_json["phone"]
        assert json.loads(response.content)["country"] == expected_json["country"]
        assert json.loads(response.content)["city"] == expected_json["city"]
        assert json.loads(response.content)["is_staff"] == expected_json["is_staff"]
        assert json.loads(response.content)["is_active"] == expected_json["is_active"]


    def test_retrieve(self, api_client, user_create):
        
        expected_json = {
            'email': user_create.email,
            'role': user_create.role.role,
            'phone': user_create.phone,
            'country': user_create.country,
            'city': user_create.city,
            'is_staff': user_create.is_staff,
            'is_active': user_create.is_active,
        }
        url = f'{self.endpoint}{user_create.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["email"] == expected_json["email"]
        assert json.loads(response.content)["role"] == expected_json["role"]
        assert json.loads(response.content)["phone"] == expected_json["phone"]
        assert json.loads(response.content)["country"] == expected_json["country"]
        assert json.loads(response.content)["city"] == expected_json["city"]
        assert json.loads(response.content)["is_staff"] == expected_json["is_staff"]
        assert json.loads(response.content)["is_active"] == expected_json["is_active"]


    def test_update(self, api_client, user_create, user_update):
        
        user_dict = {
            'role': user_update.role.role,
            'phone': user_update.phone,
            'country': user_update.country,
            'city': user_update.city,
            'is_staff': user_update.is_staff,
            'is_active': user_update.is_active,
        } 

        url = f'{self.endpoint}{user_create.id}/'

        response = api_client().put(
            url,
            user_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)["role"] == user_dict["role"]
        assert json.loads(response.content)["phone"] == user_dict["phone"]
        assert json.loads(response.content)["country"] == user_dict["country"]
        assert json.loads(response.content)["city"] == user_dict["city"]
        assert json.loads(response.content)["is_staff"] == user_dict["is_staff"]
        assert json.loads(response.content)["is_active"] == user_dict["is_active"]


    @pytest.mark.parametrize('field',[
        ('role'),
        ('phone'),
        ('country'),
        ('city'),
    ])
    def test_partial_update(self, field, api_client, user_create):
        
        user_dict = {
            'role': user_create.role.role,
            'phone': user_create.phone,
            'country': user_create.country,
            'city': user_create.city,
        } 
        valid_field = user_dict[field]
        url = f'{self.endpoint}{user_create.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, user_create):

        url = f'{self.endpoint}{user_create.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert User.objects.all().count() == 0