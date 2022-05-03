from .models import Move
from django import forms
from django.core.exceptions import ValidationError

class MoveForm(forms.ModelForm):
    class Meta:
        model = Move
        exclude = ['game']

    def clean(self):
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        game = self.instance.game
        try:
            if game.board()[x][y] is not None:
                raise ValidationError('Square is not empty')
        except IndexError:
            raise ValidationError('Invalid Coordinates')
        return self.cleaned_data