from django import forms

# 2. tworzymy ten form i uzywamy go w views
class AvalilabilityForm(forms.Form):
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])