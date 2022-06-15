import json
import pytest

from apps.request.models import RequestStatus


@pytest.mark.django_db
class TestRequestStatusEndpoints:

    endpoint = '/requeststatuses/'

    def test_list(self, api_client, request_status_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, request_status_create):
        
        expected_json = {
            'name': request_status_create.name,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["name"] == expected_json["name"]


    def test_retrieve(self, api_client, request_status_create):
        
        expected_json = {
            'name': request_status_create.name,
        }
        url = f'{self.endpoint}{request_status_create.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["name"] == expected_json["name"]


    def test_update(self, api_client, request_status_create, request_status_update):
        
        request_dict = {
            'name': request_status_update.name,
        } 

        url = f'{self.endpoint}{request_status_create.id}/'

        response = api_client().put(
            url,
            request_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)["name"] == request_dict["name"]


    @pytest.mark.parametrize('field',[
        ('name'),
    ])
    def test_partial_update(self, field, api_client, request_status_create):
        request_status_dict = {
            'name': request_status_create.name,
        } 
        valid_field = request_status_dict[field]
        url = f'{self.endpoint}{request_status_create.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, request_status_create):

        url = f'{self.endpoint}{request_status_create.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert RequestStatus.objects.all().count() == 0