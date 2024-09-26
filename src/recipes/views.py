from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from .utils import get_top_ingredients_chart, get_difficulty_spread_chart, get_cooking_time_by_difficulty_chart

#to protect class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

#search functionality imports
from .forms import RecipeSearchForm
import pandas as pd


# Create your views here.
def home(request):
  return render(request, 'recipes/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
  model = Recipe
  template_name = 'recipes/recipes_overview.html'

  #recipe search view
  def get_queryset(self):
    queryset = super().get_queryset()

    #retrieve search parameters
    recipe_name = self.request.GET.get('recipe_name')
    ingredient = self.request.GET.get('ingredient')
    difficulty = self.request.GET.get('difficulty')

    #filter queryset based on search parameters
    if recipe_name:
      queryset = queryset.filter(name__icontains=recipe_name)
    if ingredient:
      queryset = queryset.filter(ingredients__icontains=ingredient)
    if difficulty and difficulty != '':
      queryset = queryset.filter(difficulty=difficulty)
    
    return queryset
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    queryset = self.get_queryset()

    df = pd.DataFrame(list(queryset.values('id', 'name','pic', 'cooking_time')))
    recipes = df.to_dict('records') if not df.empty else []
    for recipe in recipes:
      recipe_instance = Recipe.objects.get(pk=recipe["id"])
      recipe["get_absolute_url"] = recipe_instance.get_absolute_url()
      recipe["pic_url"] = recipe_instance.pic.url if recipe_instance.pic else None

    # Adds the modified list of recipes to the context.
    context["object_list"] = recipes
    num_results = len(context["object_list"])
    title_parts = []

    #retrieve search parameters
    recipe_name = self.request.GET.get('recipe_name')
    ingredient = self.request.GET.get('ingredient')
    difficulty = self.request.GET.get('difficulty')

    if recipe_name:
      title_parts.append(f"'{recipe_name}' in the name")
    if ingredient:
      title_parts.append(f"'{ingredient}' in ingredients")
    if difficulty and difficulty != '':
      title_parts.append(f"difficulty of {difficulty}")
    
    # Constructing the main title and detailed search criteria
    if title_parts:
      context['main_title'] = "Results for:"
      recipe_word = "Recipe" if num_results == 1 else "Recipes"
      details_intro = f"{recipe_word} with "  # Adjust the intro based on number of results
      context['search_details'] = details_intro + ", ".join(title_parts)
    else:
      context['main_title'] = "Full List of Recipes"
      context['search_details'] = ""
    
    # Additional context for search form and charts based on the filtered recipes.  
    # recipes_list = list(queryset.values('id', 'name', 'ingredients', 'description', 'pic', 'cooking_time', 'difficulty'))
    context["search_form"] = RecipeSearchForm(self.request.GET)  # Retain the search form input
    context['show_all_recipes_button'] = bool(self.request.GET)

    #adds charts to context
    recipes_list = list(queryset.values('id', 'name', 'ingredients', 'pic', 'cooking_time', 'difficulty'))
    context['top_ing_chart'] = get_top_ingredients_chart(recipes_list)
    context['difficulty_spread_chart'] = get_difficulty_spread_chart(recipes_list)
    context['difficulty_and_time_chart'] = get_cooking_time_by_difficulty_chart(recipes_list)

    return context





class RecipeDetailView(LoginRequiredMixin, DetailView):
  model = Recipe
  template_name = 'recipes/recipe_details.html'