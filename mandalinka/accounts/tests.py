from django.test import TestCase, Client
from django.db.models import Max
from .models import User, Address

# Create your tests here.
class UserTestCase(TestCase):

    def setUp(self):

        # Create Users
        u1 = User.objects.create(
            first_name='Timur',
            last_name='Kramar',
            pronoun='male',
            email='test@example.com',
            phone='+421910333225',
            newsletter=True,
            terms_conditions=True, 
        )

        # Create Addresses
        Address.objects.create(
            name='Domov',
            address='Beskydská 10',
            city = 'Bratislava',
            district='Staré mesto',
            postal='811 04',
            country='Slovensko',
            coordinates='10.000,11.000',
            user=u1
        )
        Address.objects.create(
            name='Chata',
            address='Beskydská 12',
            city = 'Bratislava',
            district='Staré mesto',
            postal='811 04',
            country='Slovensko',
            coordinates='10.000,11.000',
            user=u1
        )
        
    def test_single_primary_address_per_user(self):
        """
        Check if user always has exactly one primary address
        """
        user = User.objects.get(first_name='Timur')
        self.assertEqual(user.addresses.filter(primary=True).count(), 1)
        
        #Check after adding new one
        Address.objects.create(
            name='Práca',
            address='Beskydská 15',
            city = 'Bratislava',
            district='Staré mesto',
            postal='811 04',
            country='Slovensko',
            coordinates='10.000,11.000',
            user=user,
        )        
        self.assertEqual(user.addresses.filter(primary=True).count(), 1)
        
        # Check after changing primary
        user.addresses.get(name='Domov').make_primary()
        user.save()
        self.assertEqual(user.addresses.filter(primary=True).count(), 1)
        
        # Check after deleting primary
        user.addresses.get(primary=True).delete()
        user.save()
        self.assertEqual(user.addresses.filter(primary=True).count(), 1)

