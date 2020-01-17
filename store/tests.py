import unittest
from unittest import mock

from django.db.models import QuerySet
from django.test import TestCase
from store.management.commands.update_db import Command
from store import models
from store.models import Categories, Products, Nutriments_for_100g, User_Favorites_Substitutes

categories = ['Viandes']

fake_received_nutriments = {
    "fat_100g": "10,5",
    "saturated-fat_100g": "3.5",
    "sugars_100g": "2,5",
    "salt_100g": "1.8",
    "oder_nutriment1": "X,Y",
    "oder_nutriment2": "X,Y",
    "oder_nutriment3": "X,Y"
}

fake_received_data = {"products": [{"id": 30957,
                                    "product_name": "name",
                                    "generic_name_fr": "name_generic",
                                    "brands": "brand_name",
                                    "nutrition_grade_fr": "e",
                                    "nova_groups": "3",
                                    "ingredients_text_fr": "ingredients",
                                    "url": "url_page",
                                    "image_url": "url_image",
                                    "nutriments": fake_received_nutriments,
                                    "categories": "fist_oder_categorie, second_oder_categorie",
                                    "countries_lc": "fr",
                                    "oder_param_x": "param_x",
                                    "oder_param_y": "param_y"
                                    }]
                      }

fake_result_filtered_nutriments = {"Matières grasses/lipides": "10,5",
                                   "Acide gras saturés": "3,5",
                                   "Sucres": "2,5",
                                   "Sel": "1,8"
                                   }

fake_result_filtered_data = [{"id": 30957,
                              "product_name": "name",
                              "generic_name_fr": "name_generic",
                              "brands": "brand_name",
                              "nutrition_grade_fr": "e",
                              "nova_groups": "3",
                              "ingredients_text_fr": "ingredients",
                              "url": "url_page",
                              "image_url": "url_image",
                              "nutriments": fake_result_filtered_nutriments,
                              "categories": "fist_oder_categorie, second_oder_categorie",
                              }]


class CommandTestCase(TestCase):

    # This mock method will replace requests.get from "Command._search_api_data()"
    def mock_requests_get(self, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(fake_received_data, 200)

    @mock.patch('store.management.commands.update_db.requests.get', side_effect=mock_requests_get)
    def test_search_api_data(self, mock_get):
        result = Command._search_api_data(categories)
        self.assertEqual(result, fake_result_filtered_data)

    def test_filtered_api_data(self):
        result = Command._filtered_api_data(fake_received_data)
        self.assertEqual(result, fake_result_filtered_data)

    def test_filtered_nutriments(self):
        result = Command._filtered_nutriments(fake_received_nutriments)
        self.assertEqual(result, fake_result_filtered_nutriments)

    @mock.patch('store.management.commands.update_db.settings.CATEGORIES', categories)
    @mock.patch('store.management.commands.update_db.requests.get', side_effect=mock_requests_get)
    def test_update_db(self, mock_data):
        """ Test if all fake data in database """
        # Call update command patched with fake data
        Command.update_db()
        ############## Test if fake categories in database categories table ###############################
        self.assertEqual(len(Categories.objects.all()), 3)
        # Fake categories list
        oder_categorie = fake_result_filtered_data[0]["categories"].split(',')
        # List of all categories
        for cat in oder_categorie:
            categories.append(cat)
        # Categorie list in database
        value = [value for (key, value) in Categories.objects.values_list()]
        # Test if fake categories data list in database (Categories)
        i = 0
        for cat in categories:
            self.assertEqual(value[i], cat)
            i += 1

        ############ Test if fake filtered products in database products table #####################################
        self.assertTrue(Products.objects.filter(pk=30957).exists())
        product = Products.objects.get(pk=30957)
        # List product fields name
        product_fields = [field.name for field in Products._meta.fields]
        # List fake_data_values
        fake_product_data_values = [value for value in fake_result_filtered_data[0].values()]
        i = 0
        # Test if all fake product data in product database (Products)
        for product_n in product_fields:
            self.assertEqual(getattr(product, product_n), fake_product_data_values[i])
            i += 1

        ########### Test if fake filtered nutriments in database nutriments table ##############################
        i = 0
        # Nutriment names list in database
        nutriment_name = [nutriment[1] for nutriment in Nutriments_for_100g.objects.values_list()]
        # Nutriment values list in database
        nutriment_value = [nutriment[2] for nutriment in Nutriments_for_100g.objects.values_list()]
        # Test if fake filtered nutriments in database nutriments table (Nutriment_for_100g)
        for fake_nutri_name, fake_nutri_value in fake_result_filtered_nutriments.items():
            self.assertEqual(nutriment_name[i], fake_nutri_name)
            self.assertEqual(nutriment_value[i], fake_nutri_value)
            i += 1


if __name__ == '__main__':
    unittest.main()
