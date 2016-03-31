from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

from .models import Dette, Occasion, Remboursement

ROOT_URL = 'comptes'


class ComptesTests(TestCase):
    def setUp(self):
        dt = now()
        a, b, c = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'abc')
        o = Occasion(nom='O', slug='o', description='test occasion 1', debut=dt, fin=dt + timedelta(days=30))
        p = Occasion(nom='P', slug='p', description='test occasion 2', debut=dt, fin=dt + timedelta(days=30))
        o.save()
        p.save()
        p.membres.add(a)
        p.membres.add(b)
        d = Dette(creancier=a, montant=9, date=dt, occasion=o, scribe=a, description='Lorem Ipsum')
        d.save()
        d.debiteurs.add(a)
        d.debiteurs.add(b)
        d.debiteurs.add(c)
        Remboursement(crediteur=b, credite=a, montant=3, date=dt.date(), time=dt.time(), scribe=c, occasion=o).save()

    # MODELS

    def test_get_absolute_url(self):
        o = Occasion.objects.first()
        d = Dette.objects.first()
        r = Remboursement.objects.first()
        self.assertEqual(o.get_absolute_url(), '/%s/%s' % (ROOT_URL, o.slug))
        self.assertEqual(d.get_absolute_url(), '/%s/%s' % (ROOT_URL, o.slug))
        self.assertEqual(r.get_absolute_url(), '/%s/%s' % (ROOT_URL, o.slug))

    # Occasion

    def test_occasion_str(self):
        o, p = Occasion.objects.all()
        self.assertEqual(str(o), 'Occasion: O')
        self.assertEqual(str(p), 'Occasion: P')

    def test_occasion_get_membres(self):
        for occasion in Occasion.objects.all():
            for user in User.objects.all():
                if user.username == 'c' and occasion.nom == 'P':
                    self.assertNotIn(user, occasion.get_membres())
                else:
                    self.assertIn(user, occasion.get_membres())

    def test_occasion_solde_des_membres(self):
        a, b, c = User.objects.all()
        self.assertEqual(Occasion.objects.first().solde_des_membres(), [(3, a), (0, b), (-3, c)])

    def test_occasion_depenses(self):
        self.assertEqual(Occasion.objects.first().depenses(), 9)

    # Dette

    def test_dette_str(self):
        self.assertEqual(str(Dette.objects.first()), 'Dette: a a payé 9.00 à 3 personnes pour «Lorem Ipsum»')

    def test_dette_debiteurs_list(self):
        self.assertEqual(Dette.objects.first().debiteurs_list(), 'a, b, c')

    # Remboursement

    def test_remboursement_str(self):
        self.assertEqual(str(Remboursement.objects.first()), 'b a remboursé 3.00 € à a')

    # VIEWS

    def test_access_home(self):
        self.assertEqual(self.client.get(reverse('comptes:home')).status_code, 302)
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('comptes:home')).status_code, 200)

    def test_access_occasion(self):
        self.assertEqual(self.client.get(reverse('comptes:occasion', kwargs={'slug': 'p'})).status_code, 302)
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('comptes:occasion', kwargs={'slug': 'p'})).status_code, 200)
        self.client.login(username='c', password='c')
        self.assertEqual(self.client.get(reverse('comptes:occasion', kwargs={'slug': 'p'})).status_code, 403)

    def test_access_dette(self):
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('comptes:dette', kwargs={'oc_slug': 'p'})).status_code, 200)
        self.client.login(username='c', password='c')
        self.assertEqual(self.client.get(reverse('comptes:dette', kwargs={'oc_slug': 'p'})).status_code, 302)

    def test_create_dette(self):
        self.client.login(username='a', password='a')

        dette_data = {
            'creancier': 1,
            'debiteurs': [2],
            'montant': 20,
            'description': 'test',
            'date': date(1990, 6, 14),
            'time': time(4, 2),
        }
        r = self.client.post(reverse('comptes:dette', kwargs={'oc_slug': 'p'}), dette_data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/comptes/p')

        dette_data['add_another'] = 1
        r = self.client.post(reverse('comptes:dette', kwargs={'oc_slug': 'p'}), dette_data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/comptes/p/dette')

    def test_create_remboursement(self):
        self.client.login(username='a', password='a')

        dette_data = {
            'crediteur': 2,
            'credite': 3,
            'montant': 20,
            'date': date(1990, 6, 14),
            'time': time(4, 2),
        }
        r = self.client.post(reverse('comptes:remboursement', kwargs={'oc_slug': 'o'}), dette_data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, '/comptes/o')