from django.test import TestCase
from django.utils import timezone
from .models import Customer

class CustomerModelTests(TestCase):
    def test_next_birthday(self):
        today = timezone.localdate()
        # birthday later this year
        dob = today.replace(year=today.year - 30) + timezone.timedelta(days=1)
        c = Customer.objects.create(name="Test", dob=dob)
        self.assertEqual(c.next_birthday, dob)
