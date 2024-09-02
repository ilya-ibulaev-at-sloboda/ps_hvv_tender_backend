from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from air_pollution.models import Pollution


class PollutionStatsAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authenticated tests
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()

        # Sample Pollution data
        Pollution.objects.create(
            entity="USA",
            year=2020,
            nitrogen_oxide=12.34,
            sulphur_dioxide=56.78,
            carbon_monoxide=9.01,
            organic_carbon=23.45,
            non_methane_volatile_organic_compounds=67.89,
            black_carbon=10.11,
            ammonia=12.13,
        )

        self.valid_entity = "USA"
        self.invalid_entity = "INVALID_ENTITY"
        self.url = reverse(
            "air_pollution:stats-by-entity", kwargs={"entity": self.valid_entity}
        )
        self.invalid_url = reverse(
            "air_pollution:stats-by-entity", kwargs={"entity": self.invalid_entity}
        )

    def test_unauthorized_user_gets_403(self):
        # Simulate unauthorized access (without logging in)
        response = self.client.get(self.url)

        # Check that the status code is 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_entity_returns_404(self):
        # Login with a valid user
        self.client.login(username="testuser", password="testpass")

        # Request with an invalid entity
        response = self.client.get(self.invalid_url)

        # Check that the status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success_returns_200_and_valid_structure(self):
        # Login with a valid user
        self.client.login(username="testuser", password="testpass")

        # Request with a valid entity
        response = self.client.get(self.url)

        # Check that the status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response has the correct structure
        expected_structure = {
            "entity": str,
            "average": {
                "nitrogen_oxide": float,
                "sulphur_dioxide": float,
                "carbon_monoxide": float,
                "organic_carbon": float,
                "nmvoc": float,
                "black_carbon": float,
                "ammonia": float,
            },
            # "median": {
            #     "nitrogen_oxide": float,
            #     "sulphur_dioxide": float,
            #     "carbon_monoxide": float,
            #     "organic_carbon": float,
            #     "nmvoc": float,
            #     "black_carbon": float,
            #     "ammonia": float,
            # },
            "std_dev": {
                "nitrogen_oxide": float,
                "sulphur_dioxide": float,
                "carbon_monoxide": float,
                "organic_carbon": float,
                "nmvoc": float,
                "black_carbon": float,
                "ammonia": float,
            },
        }

        # Get the first item in the response (as it's a list)
        actual_data = response.json()[0]

        def assert_structure(expected, actual):
            for key, value_type in expected.items():
                if isinstance(value_type, dict):
                    assert_structure(value_type, actual[key])
                else:
                    self.assertIsInstance(actual[key], value_type)

        # Validate the structure
        assert_structure(expected_structure, actual_data)
