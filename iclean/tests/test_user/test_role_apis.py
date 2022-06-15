import json
import pytest

from apps.user.models import Role


@pytest.mark.django_db
class TestRoleEndpoints:

    endpoint = '/roles/'

    def test_list(self, api_client, role_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, role_create):
        
        expected_json = {
            'role': role_create.role,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["role"] == expected_json["role"]


    def test_retrieve(self, api_client, role_create):
        
        expected_json = {
            'role': role_create.role,
        }
        url = f'{self.endpoint}{role_create.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["role"] == expected_json["role"]


    def test_update(self, api_client, role_create, role_update):
        
        role_dict = {
            'role': role_update.role,
        } 

        url = f'{self.endpoint}{role_create.id}/'

        response = api_client().put(
            url,
            role_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)["role"] == role_dict["role"]


    @pytest.mark.parametrize('field',[
        ('role'),
    ])
    def test_partial_update(self, field, api_client, role_create):
        
        role_dict = {
            'role': role_create.role,
        } 
        valid_field = role_dict[field]
        url = f'{self.endpoint}{role_create.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, role_create):

        url = f'{self.endpoint}{role_create.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Role.objects.all().count() == 0