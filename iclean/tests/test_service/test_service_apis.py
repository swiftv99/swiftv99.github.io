import json
import pytest

from apps.service.models import Service


@pytest.mark.django_db
class TestServiceEndpoints:

    endpoint = '/services/'

    def test_list(self, api_client, service_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, service_create):
        
        expected_json = {
            'name': service_create.name,
            'type_of_service': service_create.type_of_service,
            'cost_of_service': service_create.cost_of_service,
            'created_at': service_create.created_at,
            'company': service_create.company.name,
            'slug': service_create.slug,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["name"] == expected_json["name"]
        assert json.loads(response.content)["type_of_service"] == expected_json["type_of_service"]
        assert json.loads(response.content)["cost_of_service"] == str(expected_json["cost_of_service"])
        assert json.loads(response.content)["company"] == expected_json["company"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]


    def test_retrieve(self, api_client, service_create):
        
        expected_json = {
            'name': service_create.name,
            'type_of_service': service_create.type_of_service,
            'cost_of_service': service_create.cost_of_service,
            'created_at': service_create.created_at,
            'company': service_create.company.name,
            'slug': service_create.slug,
        }
        url = f'{self.endpoint}{service_create.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["name"] == expected_json["name"]
        assert json.loads(response.content)["type_of_service"] == expected_json["type_of_service"]
        assert json.loads(response.content)["cost_of_service"] == str(expected_json["cost_of_service"])
        assert json.loads(response.content)["company"] == expected_json["company"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]


    def test_update(self, api_client, service_create, service_update):
        
        service_dict = {
            'name': service_update.name,
            'type_of_service': service_update.type_of_service,
            'cost_of_service': service_update.cost_of_service,
            'slug': service_update.slug,
        } 

        url = f'{self.endpoint}{service_create.id}/'

        response = api_client().put(
            url,
            service_dict,
            format='json'
        )
        print(json.loads(response.content))
        print(service_dict)
        assert response.status_code == 200
        # assert json.loads(response.content) == service_dict
        assert json.loads(response.content)["name"] == service_dict["name"]
        assert json.loads(response.content)["type_of_service"] == service_dict["type_of_service"]
        assert json.loads(response.content)["cost_of_service"] == str(service_dict["cost_of_service"])
        assert json.loads(response.content)["slug"] == service_dict["slug"]


    @pytest.mark.parametrize('field',[
        ('name'),
        ('type_of_service'),
        ('cost_of_service'),
        ('slug'),
    ])
    def test_partial_update(self, field, api_client, new_service):
        service_dict = {
            'name': new_service.name,
            'type_of_service': new_service.type_of_service,
            'cost_of_service': new_service.cost_of_service,
            'slug': new_service.slug,
        } 
        valid_field = service_dict[field]
        url = f'{self.endpoint}{new_service.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, service_create):

        url = f'{self.endpoint}{service_create.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Service.objects.all().count() == 0
