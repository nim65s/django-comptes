from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from .models import Dette, Occasion, Remboursement


class OccasionTests(TestCase):
    def setUp(self):
        a = User.objects.create_user('a', 'a@example.org')
        b = User.objects.create_user('b', 'b@example.org')
        c = User.objects.create_user('c', 'c@example.org')
        o = Occasion(nom='O', slug='o', description='test occasion 1', debut=now(), fin=now() + timedelta(days=30))
        o.save()
        p = Occasion(nom='P', slug='p', description='test occasion 2', debut=now(), fin=now() + timedelta(days=30))
        p.save()
        p.membres.add(a)
        p.membres.add(b)

    def test_str(self):
        o, p = Occasion.objects.order_by('id').all()
        self.assertEqual(str(o), 'Occasion: O')
        self.assertEqual(str(p), 'Occasion: P')
