from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError


class WeatherForm(forms.Form):
    condition = forms.CharField(
        label="Enter Weather Condition: ", max_length=50, required=True)

    def clean_condition(self):
        data = self.cleaned_data["condition"]

        if(data.lower() not in (cond.lower() for cond in settings.VALID_CONDITIONS)):
            raise ValidationError(
                "Weather condition should be one of the following: " + ", ".join(settings.VALID_CONDITIONS))
        return data
