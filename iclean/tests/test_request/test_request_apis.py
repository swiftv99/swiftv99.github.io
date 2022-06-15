import json
import pytest

from apps.request.models import Request


@pytest.mark.django_db
class TestRequestEndpoints:

    endpoint = '/requests/'

    def test_list(self, api_client, request_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, request_create):
        
        expected_json = {
            'name': request_create.name,
            'total_area': request_create.total_area,
            'created_at': request_create.created_at,
            'client': request_create.client.first_name,
            'company': request_create.company.name,
            'status': request_create.status.name,
            'service': request_create.service.name,
            'slug': request_create.slug,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["name"] == expected_json["name"]
        assert json.loads(response.content)["total_area"] == str(expected_json["total_area"])
        assert json.loads(response.content)["client"] == expected_json["client"]
        assert json.loads(response.content)["company"] == expected_json["company"]
        assert json.loads(response.content)["status"] == expected_json["status"]
        assert json.loads(response.content)["service"] == expected_json["service"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]


    def test_retrieve(self, api_client, request_create):
        
        expected_json = {
            'name': request_create.name,
            'total_area': request_create.total_area,
            'created_at': request_create.created_at,
            'client': request_create.client.first_name,
            'company': request_create.company.name,
            'status': request_create.status.name,
            'service': request_create.service.name,
            'slug': request_create.slug,
        }
        url = f'{self.endpoint}{request_create.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["name"] == expected_json["name"]
        assert json.loads(response.content)["total_area"] == str(expected_json["total_area"])
        assert json.loads(response.content)["client"] == expected_json["client"]
        assert json.loads(response.content)["company"] == expected_json["company"]
        assert json.loads(response.content)["status"] == expected_json["status"]
        assert json.loads(response.content)["service"] == expected_json["service"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]


    def test_update(self, api_client, request_create, request_update):
        
        request_dict = {
            'name': request_update.name,
            'total_area': request_update.total_area,
            'created_at': request_update.created_at,
            'status': request_update.status.name,
            'service': request_update.service.name,
            'slug': request_update.slug,
        } 

        url = f'{self.endpoint}{request_create.id}/'

        response = api_client().put(
            url,
            request_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)["name"] == request_dict["name"]
        assert json.loads(response.content)["total_area"] == str(request_dict["total_area"])
        assert json.loads(response.content)["status"] == request_dict["status"]
        assert json.loads(response.content)["service"] == request_dict["service"]
        assert json.loads(response.content)["slug"] == request_dict["slug"]


    @pytest.mark.parametrize('field',[
        ('name'),
        ('total_area'),
        ('status'),
        ('service'),
        ('slug'),
    ])
    def test_partial_update(self, field, api_client, request_create):
        service_dict = {
            'name': request_create.name,
            'total_area': request_create.total_area,
            'status': request_create.status.name,
            'service': request_create.service.name,
            'slug': request_create.slug,
        } 
        valid_field = service_dict[field]
        url = f'{self.endpoint}{request_create.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, request_create):

        url = f'{self.endpoint}{request_create.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Request.objects.all().count() == 0