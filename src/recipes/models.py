from django.db import models
from django.shortcuts import reverse

class Recipe(models.Model):
  # defining main attributes
  name = models.CharField(max_length=50)
  ingredients = models.CharField(max_length=225, help_text="Enter recipe ingredients, separated by a comma")
  cooking_time = models.IntegerField(help_text="Enter cooking time in minutes.")
  difficulty = models.CharField(max_length=20, default="TBD")
  pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

  # calculate recipe difficulty
  def calculate_difficulty(self):
    ingredient_count = len(self.ingredients.split(", "))
    if self.cooking_time < 10 and ingredient_count < 4:
      return "Easy"
    elif self.cooking_time < 10 and ingredient_count >= 4:
      return "Medium"
    elif self.cooking_time >= 10 and ingredient_count < 4:
      return "Intermediate"
    elif self.cooking_time >= 10 and ingredient_count >= 4:
      return "Hard"

  def save(self, *args, **kwargs):
    self.difficulty = self.calculate_difficulty() # Set the difficulty level before saving.
    super().save(*args, **kwargs) # Call the parent class's save method to handle saving the instance.

  # string representation
  def str(self):
    return f"{self.name}"

  def get_absolute_url(self):
    return reverse('recipes:detail', kwargs={'pk': self.pk})