from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from home.models import CityDistrictPostal
from django import forms
from django.core.exceptions import ValidationError
from home.models import UserProfile, FoodAttribute
from django.utils.safestring import mark_safe

charfield_widget = {'class': 'form-control opacity-75 rounded-2 shadow border-dark',
                    'placeholder': 'useless_placeholder'}
checkbox_widget = {'class':'form-check-input'}
attributes_select_widget = {'class':'btn btn-primary', 'data-bs-toggle':'button'}

def merge(dict1, dict2):
    return {**dict1, **dict2} 

class LoginForm(forms.Form):
    username = forms.CharField(label="Prihlasovacie meno", widget=forms.TextInput(charfield_widget))
    password = forms.CharField(label="Heslo", widget=forms.PasswordInput(charfield_widget))
 
 
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Prihlasovacie meno"
        self.fields['username'].help_text = 'Username (150 characters or fewer, letters, digits and @/./+/-/_ only)'
        self.fields['username'].widget = forms.TextInput(charfield_widget)

    COUNTRIES = (
        ("CZ","SK"),
        ("SK","CZ"),
    )
    firstname = forms.CharField(label="Meno", widget=forms.TextInput(charfield_widget))
    lastname = forms.CharField(label="Priezvisko", widget=forms.TextInput(charfield_widget))
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(charfield_widget))

    newsletter = forms.BooleanField(label="newsletter",
                                    help_text="Súhlasíte so zasielaním propagačných emailov?", 
                                    widget=forms.CheckboxInput(checkbox_widget))
    terms_conditions = forms.BooleanField(label="terms_conditions",
                                          help_text="Súhlasíte s <a hrf='#Obchodné podmienky'>obchodnými podmienkami</a>?",
                                          required=True)
    
    food_attributes = forms.ModelMultipleChoiceField(label="Attributes", help_text="Zvolte obľúbené atribúty", 
                                                queryset=FoodAttribute.objects.all(), 
                                                widget=forms.CheckboxSelectMultiple())

    phone = forms.CharField(min_length=5, label="Telefónne číslo", help_text='* Môže byť použité počas doručovania', required=True, widget=forms.TextInput(merge(charfield_widget,{'value':'+421'})))

    street = forms.CharField(label="street",help_text='Ulica:',required=False, widget=forms.TextInput(attrs={'list':'streets'}))
    house_no = forms.CharField(label="house_no",help_text='Číslo domu:', required=True)
    district = forms.CharField(label="district",help_text='Okres:',required=True, widget=forms.TextInput(attrs={'list':'districts'}))
    city = forms.CharField(label="city",help_text='Mesto:',required=True, widget=forms.TextInput(attrs={'list':'cities'}))
    postal = forms.CharField(min_length=5, max_length=5,label="postal", help_text='PSČ:',required=True, widget=forms.TextInput(attrs={'list':'postal_codes'}))
    country = forms.ChoiceField(label="country",choices=COUNTRIES, required=True, help_text='Krajina:')
    
    class Meta:
        model = User
        fields = ["username",
                "firstname",
                "lastname", 
                "email",
                "newsletter",
                "terms_conditions",
                "food_attributes",
                "phone",
                "street",
                "house_no",
                "city",
                "district",
                "postal",
                "country",
                "password1",
                "password2"
                ]

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if data[:4] not in ["+421", "+420"]:
            raise ValidationError("Unknown or missing dialing code")
        #if len(data) < 5:
         #   raise ValidationError("Phone number too short (must contain at least 5 numbers)")

        return data
    
    def clean_house_no(self):
        data = self.cleaned_data['house_no']
        for i in data:
            if i not in '0123456789/-:':
                raise ValidationError("House number can only contain numbers or /-: characters")

        return data

    def clean_district(self):
        data = self.cleaned_data['district']
        if not CityDistrictPostal.objects.filter(district=data).exists():
            raise ValidationError("Unknown district name - make sure you choose from given list and use special characters")
        return data

    def clean_city(self):
        data = self.cleaned_data['city']
        if not CityDistrictPostal.objects.filter(city=data).exists():
            raise ValidationError("Unknown city - make sure you choose from given list and use special characters")
        return data

    def clean_postal(self):
        data = self.cleaned_data['postal']
        #some streets have no postal codes in Bratislava (Adlerova, Alexyho...) - user should leave '-'
        if not CityDistrictPostal.objects.filter(code=data).exists() and data != '-':
            raise ValidationError("Unknown postal code - make sure you choose from given list and use special characters")
        return data

    def clean_country(self):
        data = self.cleaned_data['country']
        if data not in ["SK", "CZ"]:
            raise ValidationError("Unknown country - make sure you choose from given list and use special characters")
        return data

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        district = cleaned_data.get("district")
        postal = cleaned_data.get("postal")
        street = cleaned_data.get("street")
        house_no = cleaned_data.get("house_no")
        valid_city = CityDistrictPostal.objects.filter(city=city, district=district)
        if not valid_city:
            # There is no such combination - the user probably used wrong district
            
            for_city = CityDistrictPostal.objects.filter(city=city)
            if not for_city:
                raise ValidationError(
                    mark_safe(f"We could not find city {city} in our database. Check the spelling, choose from suggested names or contact the admin")
                )
            message = f'We only have following districts and postal codes (or streets) associated with city <strong>{city}</strong> and postal code <strong>{postal}</strong>: <ul>'
            for obj in for_city:
                message += f'<li>District: <strong>{obj.district}</strong>, Postal code: <strong>{obj.postal}</strong>'
                if obj.street != '':
                    message += f"Street: <strong>{obj.street}</strong>"
                message += '</li>'
            message += "</ul>"
            raise ValidationError(
                mark_safe(message)
            )
        # then check if there is a city in that district with given postal code
        valid_city = CityDistrictPostal.objects.filter(city=city, district=district, postal=postal)
        num_res = valid_city.count()
        if num_res < 1 and postal != '-':
            # if there is no result
            exp = CityDistrictPostal.objects.filter(city=city)
            if not exp:
                raise ValidationError(mark_safe(f"No results for city <strong>{city}</strong>"))
            exp_distr = map(lambda x: x[0], exp.values_list("district").distinct())
            exp_post = [x[0] if x[0] != '' else '-' for x in exp.values_list("postal").distinct()]
            raise ValidationError(
                mark_safe(f"""No results for provided address: {city}, {district}, {postal}.
                For city {city} there are only following districts to select:
                <strong><ul><li>{'</li><li>'.join(exp_distr)}</li></ul></strong>
                and only following postal codes:
                <strong><ul><li>{'</li><li>'.join(exp_post)}</li></ul></strong>""")
            )
        elif num_res == 1 and valid_city[0].street != '' and valid_city[0].street != street:
            #if there is only one row then it either needs additional info (street) or its enough
            raise ValidationError(
                mark_safe(f"""We only have city <strong>{city}</strong>, district <strong>{district}</strong>, postal code <strong>{postal}</strong>
                associated with street <strong>{valid_city.street}</strong>. Check your input and try again.""")
            )
        elif num_res > 1:
            #If the query returns more than one then it has to depend on the street - checking that
            expected_streets = map(lambda x: x[0], valid_city.values_list("street").distinct())
            if street not in expected_streets:
                #if the provided street is not associated with any of the given city, district and postal than it has to be wrong
                
                raise ValidationError(
                        mark_safe(f"""We only have city <strong>{city}</strong>, district <strong>{district}</strong>, postal code <strong>{postal}</strong>
                associated with following streets:<strong><ul><li>{'</li><li>'.join(expected_streets)}</li></ul></strong>""")
                )

        valid_city = CityDistrictPostal.objects.filter(city=city, district=district, street=street)
        num_res = valid_city.count()
        if num_res < 1 and postal == '-':
            # if there is no result
            exp = CityDistrictPostal.objects.filter(city=city)
            if not exp:
                raise ValidationError(mark_safe(f"No results for city <strong>{city}</strong>"))
            exp_distr = map(lambda x: x[0], exp.values_list("district").distinct())
            exp_streets = [x[0] for x in exp.values_list("street").distinct()]
            raise ValidationError(
                mark_safe(f"""No results for provided address: {city}, {district}, {street} and no postal code.
                For city {city} there are only following districts to select:
                <strong><ul><li>{'</li><li>'.join(exp_distr)}</li></ul></strong>
                and only following streets with <strong>NO POSTAL CODE</strong>:
                <strong><ul><li>{'</li><li>'.join(exp_streets)}</li></ul></strong>""")
            )
        if num_res == 1 and valid_city[0].postal == '':
            # for some streets there are no postal codes provided - checking if that is the case
            if postal != '-':
                raise ValidationError(
                    mark_safe(f"For the city <strong>{city}</strong>, district <strong>{district}</strong> and street <strong>{street}</strong> there is no postal code and should be left '-'.")
                )
            if house_no != '':
                raise ValidationError(
                    mark_safe(f"For the city <strong>{city}</strong>, district <strong>{district}</strong> and street <strong>{street}</strong> there is no postal code so a house number is required")
                )
        elif num_res > 1:
            # check if there is a postal code associated with the rest
            expected_postal = [x[0] if x[0] != '' else '-' for x in valid_city.values_list("postal").distinct()]
            if postal not in expected_postal:
                #if there is no valid combination with postal
                raise ValidationError(
                    mark_safe(f"""For the city <strong>{city}</strong>, district <strong>{district}</strong> and street <strong>{street}</strong>
                    there are only following postal codes provided: <strong><ul><li>{'</li><li>'.join(expected_postal)}</li></ul></strong>""")
                )


