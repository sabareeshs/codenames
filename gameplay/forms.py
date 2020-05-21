from django import forms
from gameplay.models import Board 

class BoardForm(forms.ModelForm):
	name = forms.CharField(max_length=128,
                           help_text="Please enter a descriptive name.")
	class Meta:
		model = Board
		fields = ('name',)

class CluesForm(forms.ModelForm):
	clue = forms.CharField(max_length=128)
	num_clues = forms.IntegerField()
	class Meta:
		model = Board
		fields = ('clue', 'num_clues', )
