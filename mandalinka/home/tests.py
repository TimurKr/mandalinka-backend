from django.test import TestCase
from .models import CityDistrictPostal
from .forms import SignupForm
# Create your tests here.

class CityDistrictPostalTestCase(TestCase):
    def setUp(self):
        with open('cspdd_test.csv', 'r') as csv:
            for line in csv:
                city, street, postal, dpost, district = map(lambda x: x.strip(), line.split(';'))
                CityDistrictPostal.objects.create(city=city, street=street, postal=postal, district=district, country="SK")

    def test_create_address(self):
        """ Check if addresses get created correctly"""
        data_postal = {
            'firstname': 'John',
            'lastname': 'Smith',
            'email': 'john@example.com',
            'phone': '+421-555-5555',
            'password1': 'poiqwe123',
            'password2': 'poiqwe123',
            'terms_conditions': 'true',
            'food_attr': 'Asian',
            'num_portions': '2',
            'city':'Bratislava',
            'district':'Bratislava I',
            'street': 'Adlerova',
            'postal':'873 91',
            'house_no': '92',
            'country':'SK',       
            }

        form = SignupForm(data_postal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['postal'].errors)


        data_postal['postal'] = '811 04'
        form = SignupForm(data_postal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['postal'].errors)

        data_postal['postal'] = '-'
        form = SignupForm(data_postal)
        self.assertTrue(form.is_valid())

        data_postal['street'] = 'Alviano'
        form = SignupForm(data_postal)
        self.assertTrue(form.is_valid())

        data_postal['street'] = 'Benkova'
        form = SignupForm(data_postal)
        self.assertTrue(form.is_valid())

        data_postal['street'] = 'Dubčekova'
        form = SignupForm(data_postal)
        self.assertTrue(form.is_valid())

        data_postal['street'] = 'Fullova'
        form = SignupForm(data_postal)
        self.assertTrue(form.is_valid())

        data_postal['postal'] = '841 10'
        form = SignupForm(data_postal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['__all__'])

        data_postal['street'] = 'Staviteľská'
        form = SignupForm(data_postal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['__all__'])

        data_postal['postal'] = '831 04'
        form = SignupForm( data_postal)
        self.assertTrue(form.is_valid())

        data_postal['district'] = 'Poprad'
        form = SignupForm(data_postal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['district'].errors)

        data_postal['district'] = 'Bratislava I'
        data_postal['street'] = 'Okulele'
        form = SignupForm(data_postal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['street'].errors)

        data_postal['street'] = 'Staviteľská'
        data_postal['city'] = 'Pernek'
        form = SignupForm(data_postal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form['city'].errors)

        with open('cspdd_test.csv', 'r') as csv:
            for line in csv:
                city, street, postal, dpost, district = map(lambda x: x.strip(), line.split(';'))
                if not postal:
                    postal = '-'
                if not street:
                    street = '-'
                for attr in ('city', city), ('street', street), ('postal',postal), ('district', district),('country', 'SK'):
                    data_postal[attr[0]] = attr[1]
                form = SignupForm(data_postal)
                self.assertTrue(form.is_valid())



