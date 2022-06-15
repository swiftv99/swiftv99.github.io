import json
import pytest

from apps.notification.models import Notification


@pytest.mark.django_db
class TestNotificationEndpoints:

    endpoint = '/notifications/'

    def test_list(self, api_client, notification_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1

    def test_create(self, api_client, notification_create):

        expected_json = {
            'name': notification_create.name,
            'details': notification_create.details,
            'viewed_by_company': notification_create.viewed_by_company,
            'created_at': notification_create.created_at,
            'request': notification_create.request.name,
            'company': notification_create.company.name,
            'slug': notification_create.slug,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["name"] == expected_json["name"]
        assert json.loads(response.content)[
            "details"] == expected_json["details"]
        assert json.loads(response.content)["viewed_by_company"] == str(
            expected_json["viewed_by_company"])
        assert json.loads(response.content)[
            "request"] == expected_json["request"]
        assert json.loads(response.content)[
            "company"] == expected_json["company"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]

    def test_retrieve(self, api_client, notification_create):

        expected_json = {
            'name': notification_create.name,
            'details': notification_create.details,
            'viewed_by_company': notification_create.viewed_by_company,
            'created_at': notification_create.created_at,
            'request': notification_create.request.name,
            'company': notification_create.company.name,
            'slug': notification_create.slug,
        }
        url = f'{self.endpoint}{notification_create.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["name"] == expected_json["name"]
        assert json.loads(response.content)[
            "details"] == expected_json["details"]
        assert json.loads(response.content)["viewed_by_company"] == str(
            expected_json["viewed_by_company"])
        assert json.loads(response.content)[
            "request"] == expected_json["request"]
        assert json.loads(response.content)[
            "company"] == expected_json["company"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]

    def test_update(self, api_client, notification_create, notification_update):

        notification_dict = {
            'name': notification_update.name,
            'details': notification_update.details,
            'viewed_by_company': notification_update.viewed_by_company,
            'slug': notification_update.slug,
        }

        url = f'{self.endpoint}{notification_create.id}/'

        response = api_client().put(
            url,
            notification_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[
            "name"] == notification_dict["name"]
        assert json.loads(response.content)[
            "details"] == notification_dict["details"]
        assert json.loads(response.content)["viewed_by_company"] == str(
            notification_dict["viewed_by_company"])
        assert json.loads(response.content)[
            "slug"] == notification_dict["slug"]

    @pytest.mark.parametrize('field', [
        ('name'),
        ('details'),
        ('viewed_by_company'),
        ('slug'),
    ])
    def test_partial_update(self, field, api_client, notification_create):
        service_dict = {
            'name': notification_create.name,
            'details': notification_create.details,
            'viewed_by_company': notification_create.viewed_by_company,
            'slug': notification_create.slug,
        }
        valid_field = service_dict[field]
        url = f'{self.endpoint}{notification_create.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        # assert json.loads(response.content)[field] == valid_field
        assert json.loads(response.content)["name"] == valid_field["name"]
        assert json.loads(response.content)[
            "details"] == valid_field["details"]
        assert json.loads(response.content)["viewed_by_company"] == str(
            valid_field["viewed_by_company"])
        assert json.loads(response.content)["slug"] == valid_field["slug"]

    def test_delete(self, api_client, notification_create):

        url = f'{self.endpoint}{notification_create.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Notification.objects.all().count() == 0
