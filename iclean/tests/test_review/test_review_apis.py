import json
import pytest

from apps.review.models import Review


@pytest.mark.django_db
class TestReviewEndpoints:

    endpoint = '/reviews/'

    def test_list(self, api_client, review_create):

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)["results"]) == 1


    def test_create(self, api_client, review_create):
        
        expected_json = {
            'comment': review_create.comment,
            'rating': review_create.rating,
            'created_at': review_create.created_at,
            'client': review_create.client.first_name,
            'company': review_create.company.name,
            'slug': review_create.slug,
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json',
        )

        assert response.status_code == 201
        assert json.loads(response.content)["comment"] == expected_json["comment"]
        assert json.loads(response.content)["rating"] == expected_json["rating"]
        assert json.loads(response.content)["client"] == expected_json["client"]
        assert json.loads(response.content)["company"] == expected_json["company"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]


    def test_retrieve(self, api_client, review_create):
        
        expected_json = {
            'comment': review_create.comment,
            'rating': review_create.rating,
            'created_at': review_create.created_at,
            'client': review_create.client.first_name,
            'company': review_create.company.name,
            'slug': review_create.slug,
        }
        url = f'{self.endpoint}{review_create.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content)["comment"] == expected_json["comment"]
        assert json.loads(response.content)["rating"] == expected_json["rating"]
        assert json.loads(response.content)["client"] == expected_json["client"]
        assert json.loads(response.content)["company"] == expected_json["company"]
        assert json.loads(response.content)["slug"] == expected_json["slug"]


    def test_update(self, api_client, review_create, review_update):
        
        review_dict = {
            'comment': review_update.comment,
            'rating': review_update.rating,
            'slug': review_update.slug,
        } 

        url = f'{self.endpoint}{review_create.id}/'

        response = api_client().put(
            url,
            review_dict,
            format='json'
        )
        print(json.loads(response.content))
        print(review_dict)
        assert response.status_code == 200
        # assert json.loads(response.content) == review_dict
        assert json.loads(response.content)["comment"] == review_dict["comment"]
        assert json.loads(response.content)["rating"] == review_dict["rating"]
        assert json.loads(response.content)["slug"] == review_dict["slug"]


    @pytest.mark.parametrize('field',[
        ('comment'),
        ('rating'),
        ('slug'),
    ])
    def test_partial_update(self, field, api_client, review_create, review_update):
        review_dict = {
            'comment': review_update.comment,
            'rating': review_update.rating,
            'slug': review_update.slug,
        } 
        valid_field = review_dict[field]
        url = f'{self.endpoint}{review_create.id}/'

        response = api_client().patch(
            url,
            {field: valid_field},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field


    def test_delete(self, api_client, review_create):

        url = f'{self.endpoint}{review_create.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Review.objects.all().count() == 0
