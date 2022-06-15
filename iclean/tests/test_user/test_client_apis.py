import json
import pytest

from apps.user.models import Client


@pytest.mark.django_db
class TestClientEndpoints:

    endpoint = '/clients/'

    def test_list(self, api_client, client_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, client_create):
        
        expected_json = {
            'first_name': client_create.first_name,
            'last_name': client_create.last_name,
            'street': client_create.street,
            'house_number': client_create.house_number,
            'apartment': client_create.apartment,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["first_name"] == expected_json["first_name"]
        assert json.loads(response.content)["last_name"] == expected_json["last_name"]
        assert json.loads(response.content)["street"] == expected_json["street"]
        assert json.loads(response.content)["house_number"] == str(expected_json["house_number"])
        assert json.loads(response.content)["apartment"] == expected_json["apartment"]


    def test_retrieve(self, api_client, client_create):
        
        expected_json = {
            'user': client_create.user.id,
            'first_name': client_create.first_name,
            'last_name': client_create.last_name,
            'street': client_create.street,
            'house_number': client_create.house_number,
            'apartment': client_create.apartment,
        }
        url = f'{self.endpoint}{client_create.user.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["user"] == expected_json["user"]
        assert json.loads(response.content)["first_name"] == expected_json["first_name"]
        assert json.loads(response.content)["last_name"] == expected_json["last_name"]
        assert json.loads(response.content)["street"] == expected_json["street"]
        assert json.loads(response.content)["house_number"] == str(expected_json["house_number"])
        assert json.loads(response.content)["apartment"] == expected_json["apartment"]


    def test_update(self, api_client, client_create, client_update):
        
        client_dict = {
            'first_name': client_update.first_name,
            'last_name': client_update.last_name,
            'street': client_update.street,
            'house_number': client_update.house_number,
            'apartment': client_update.apartment,
        } 

        url = f'{self.endpoint}{client_create.user.id}/'

        response = api_client().put(
            url,
            client_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)["first_name"] == client_dict["first_name"]
        assert json.loads(response.content)["last_name"] == client_dict["last_name"]
        assert json.loads(response.content)["street"] == client_dict["street"]
        assert json.loads(response.content)["house_number"] == str(client_dict["house_number"])
        assert json.loads(response.content)["apartment"] == client_dict["apartment"]


    @pytest.mark.parametrize('field',[
        ('first_name'),
        ('last_name'),
        ('street'),
        ('house_number'),
        ('apartment'),
    ])
    def test_partial_update(self, field, api_client, client_create):
        client_dict = {
            'first_name': client_create.first_name,
            'last_name': client_create.last_name,
            'street': client_create.street,
            'house_number': client_create.house_number,
            'apartment': client_create.apartment,
        } 
        valid_field = client_dict[field]
        url = f'{self.endpoint}{client_create.user.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, client_create):

        url = f'{self.endpoint}{client_create.user.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Client.objects.all().count() == 0