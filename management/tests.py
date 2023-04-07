from django.test import TestCase

# Create your tests here.


class ManagementTestCase(TestCase):

    def test_true(self):
        self.assertEqual(1, 1)

    def test_false(self):
        self.assertEqual(2, 2)
