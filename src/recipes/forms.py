from django import forms

CHART_CHOICES = (
  ('#1', 'Bar chart'),    
  ('#2', 'Pie chart'),
  ('#3', 'Line chart')
)

DIFFICULTY_CHOICES = (
  ('', 'Any difficulty'),
  ('Easy', 'Easy'),
  ('Medium', 'Medium'),    
  ('Intermediate', 'Intermediate'),
  ('Hard', 'Hard')
)

#class-based form, using Django form as parent class
class RecipeSearchForm(forms.Form):
  recipe_name = forms.CharField(required=False, label='Type recipe name',max_length=120)
  difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=False, label='Select difficulty')
  ingredient = forms.CharField(required=False, label='Type ingredient',  max_length=120)