from django import forms


class DateInput(forms.DateInput): #klasa potrzebna do kalendarza w formularzu
    input_type = 'date'

# 2. tworzymy ten form i uzywamy go w views
class AvalilabilityForm(forms.Form):
    # ROOM_CATEGORIES = (            jezeli chce miec do wyboru w formularzu
    #     ('YAC', 'AC'),
    #     ('NAC', 'NON-AC'),
    #     ('DEL', 'DELUXE'),
    #     ('KIN', 'KING'),
    #     ('QUE', 'QUEEN'),
    # )
    # room_category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateField(required=True, widget=DateInput,) #input_formats=["%Y-%m-%dT%H:%M", ],) widget DateInput - widok kalendarza
    check_out = forms.DateField(required=True, widget=DateInput,) #input_formats=["%Y-%m-%dT%H:%M", ],)

