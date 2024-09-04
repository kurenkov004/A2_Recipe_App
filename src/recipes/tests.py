from django.test import TestCase
from .models import Recipe

# Create your tests here.
class RecipeModelTest(TestCase):
  def setUpTestData():
    #set up non-modified objects used by all test methods
    Recipe.objects.create(name="Tea", ingredients="Tea leaves, Water", cooking_time=5, )
  
  #------------------------------NAME TESTS------------------------------#
  def test_recipe_name(self):
    #get a recipe object to test
    recipe = Recipe.objects.get(id=1)
    #get metadata for the 'name' field and use it to query its data
    field_label = recipe._meta.get_field('name').verbose_name
    #compare value to expected result
    self.assertEqual(field_label, 'name')
  
  def test_recipe_name_length(self):
    #get a recipe object to test
    recipe = Recipe.objects.get(id=1)
    #get metadata for the 'name' field and use it to query its data
    max_length = recipe._meta.get_field('name').max_length
    #compare value to expected result
    self.assertEqual(max_length, 50)

  #------------------------------INGREDIENTS TESTS------------------------------#
  def test_igredients_max_length(self):
    #get a recipe object to test
    recipe = Recipe.objects.get(id=1)
    # get metadata for 'ingredients' field and use it to query its data
    max_length = recipe._meta.get_field("ingredients").max_length
    #compare values
    self.assertEqual(max_length, 225)

  #------------------------------COOKING TIME TESTS------------------------------#
  def test_cooking_time_data_type(self):
    #get a recipe object to test
    recipe = Recipe.objects.get(id=1)
    # get metadata for 'cooking_time' field and use it to query its data
    cooking_time_input = recipe.cooking_time
    #compare values
    self.assertIsInstance(cooking_time_input, int)

  #------------------------------DIFFICULTY TESTS------------------------------#
  def test_difficulty_calc(self):
    #get a recipe object to test
    recipe = Recipe.objects.get(id=1)
    #compare values
    self.assertEqual(recipe.calculate_difficulty(), "Easy")