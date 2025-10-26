from django import forms
from .models import Player, GameResult

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']

class GameResultForm(forms.ModelForm):
    class Meta:
        model = GameResult
        fields = ['player', 'number_to_guess', 'attempts', 'success']
