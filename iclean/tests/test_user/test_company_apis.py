import json
import pytest

from apps.user.models import Company


@pytest.mark.django_db
class TestCompanyEndpoints:

    endpoint = '/companys/'

    def test_list(self, api_client, company_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, company_create):
        
        expected_json = {
            'user': company_create.user.id,
            'name': company_create.name,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["user"] == expected_json["user"]
        assert json.loads(response.content)["name"] == expected_json["name"]


    def test_retrieve(self, api_client, company_create):
        
        expected_json = {
            'user': company_create.user.id,
            'name': company_create.name,
        }
        url = f'{self.endpoint}{company_create.user.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["user"] == expected_json["user"]
        assert json.loads(response.content)["name"] == expected_json["name"]


    def test_update(self, api_client, company_create, company_update):
        
        company_dict = {
            'user': company_update.user.id,
            'name': company_update.name,
        } 

        url = f'{self.endpoint}{company_create.user.id}/'

        response = api_client().put(
            url,
            company_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)["user"] == company_dict["user"]
        assert json.loads(response.content)["name"] == company_dict["name"]


    @pytest.mark.parametrize('field',[
        ('name'),
    ])
    def test_partial_update(self, field, api_client, company_create):
        company_dict = {
            'name': company_create.name,
        } 
        valid_field = company_dict[field]
        url = f'{self.endpoint}{company_create.user.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, company_create):

        url = f'{self.endpoint}{company_create.user.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Company.objects.all().count() == 0