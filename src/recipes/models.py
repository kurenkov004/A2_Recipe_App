from django.db import models

class Recipe(models.Model):
  #defining main attributes
  name = models.CharField(max_length=50)
  ingredients = models.CharField(max_length=225, help_text="Enter recipe ingredients, separated by a comma")
  cooking_time = models.IntegerField(help_text="Enter cooking time in minutes.")

  #calculate recipe difficulty
  def calculate_difficulty(self):
    ingredient_count = len(self.ingredients.split(", "))
    if self.cooking_time < 10 and ingredient_count < 4:
      difficulty = "Easy"
    elif self.cooking_time < 10 and ingredient_count >= 4:
      difficulty = "Medium"
    elif self.cooking_time >= 10 and ingredient_count < 4:
      difficulty = "Intermediate"
    elif self.cooking_time >= 10 and ingredient_count >= 4:
      difficulty = "Hard"
    return difficulty

  #string representation
  def __str__(self):
    return(f"{self.name}")