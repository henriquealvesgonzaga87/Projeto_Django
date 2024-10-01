from django.urls import reverse
from rest_framework import test
from unittest.mock import patch
from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIV2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse("recipes:recipes-api-list")

        return api_url
    
    def get_recipes_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result=reverse_result)
        response = self.client.get(api_url)

        return response
    
    def get_auth_data(self, username="user", password="pass"):
        userdata = {
            "username": username,
            "password": password
        }
        user = self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password')
        )
        response = self.client.post(reverse('recipes:token_obtain_pair'), data={**userdata})
        return {
            "jwt_access_token": response.data.get('access'),
            "jwt_refresh_token": response.data.get('refresh'),
            "user": user
            }
    
    def get_recipe_raw_data(self):
        return {
            'title': 'this is the title',
            'description': 'this is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'minutes',
            'servings': 1,
            'servings_unit': 'Person',
            'preparation_steps': 'This is the preparation steps'
        }


class RecipeAPIV2Test(test.APITestCase, RecipeAPIV2TestMixin):
    
    def test_recipe_api_list_returns_setatus_code_200(self):
        response = self.get_recipes_api_list()
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeApiV2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(quantity=wanted_number_of_recipes)
        
        response = self.client.get(reverse('recipes:recipes-api-list'))
        qtd_of_loaded_recipes = len(response.data.get('results'))
        
        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )

    def test_recipe_api_list_do_not_show_published_recipes(self):
        recipes = self.make_recipe_in_batch(quantity=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        
        response = self.get_recipes_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeApiV2Pagination.page_size', new=10)
    def test_recipes_api_list_loads_recipes_by_category_category_id(self):
        # create categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # creates 10 recipes
        recipes = self.make_recipe_in_batch(quantity=10)

        # changes all the recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()
        
        # changes one recipe to the not wanted category
        # as a result, this recipe should not show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # action get recipes by wanted category id
        api_url = reverse('recipes:recipes-api-list') + f'?category_id={category_wanted.id}'
        response = self.get_recipes_api_list(reverse_result=api_url)

        # we should see only the wanted category
        self.assertEqual(
            len(response.data.get('results')),
            9
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_acccess_token = auth_data.get('jwt_access_token')
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f"Bearer {jwt_acccess_token}"
        )
        self.assertEqual(
            response.status_code, 201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Arrange (config do test)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        wanted_new_title = f'The new title updated by {author.username}'
        
        # Action (Ação)
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={
                'title': wanted_new_title
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        
        # Assertion (Afirmação)
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.data.get('title'),
            wanted_new_title,
        )

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(self):
        # Arrange (config do test)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')

        #this user cannot update the recipe because it's owned by another user
        another_user = self.get_auth_data(username='cant_update')
        jwt_access_token_from_another_user = another_user.get('jwt_access_token')

        # this is the actual owner of the recipe
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        
        # Action (Ação)
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token_from_another_user}'
        )
        
        # Assertion (Afirmação)
        self.assertEqual(
            response.status_code,
            403,
        )
