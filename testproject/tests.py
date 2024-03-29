"""Main test module."""
from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from comptes.models import Dette, Occasion, Remboursement

ROOT_URL = "comptes"


class ComptesTests(TestCase):
    """Main test class."""

    def setUp(self):
        """Create a few guys and their interractions for all tests."""
        dt = now()
        a, b, c = (
            User.objects.create_user(guy, email=f"{guy}@example.org", password=guy)
            for guy in "abc"
        )
        o = Occasion(
            name="O",
            slug="o",
            description="test occasion 1",
            debut=dt,
            fin=dt + timedelta(days=30),
        )
        p = Occasion(
            name="P",
            slug="p",
            description="test occasion 2",
            debut=dt,
            fin=dt + timedelta(days=30),
        )
        o.save()
        p.save()
        p.membres.add(a)
        p.membres.add(b)
        d = Dette(
            creancier=a,
            montant=9,
            moment=dt,
            occasion=o,
            scribe=a,
            description="Lorem Ipsum",
        )
        d.save()
        d.debiteurs.add(a)
        d.debiteurs.add(b)
        d.debiteurs.add(c)
        Remboursement(
            crediteur=b, credite=a, montant=3, moment=dt, scribe=c, occasion=o
        ).save()

    # MODELS

    def test_get_absolute_url(self):
        """Test absolute urls of models."""
        o = Occasion.objects.first()
        d = Dette.objects.first()
        r = Remboursement.objects.first()
        self.assertEqual(o.get_absolute_url(), f"/{ROOT_URL}/{o.slug}")
        self.assertEqual(d.get_absolute_url(), f"/{ROOT_URL}/{o.slug}")
        self.assertEqual(r.get_absolute_url(), f"/{ROOT_URL}/{o.slug}")

    # Occasion

    def test_occasion_get_membres(self):
        """Check that members belongs to the right occasions."""
        for occasion in Occasion.objects.all():
            for user in User.objects.all():
                if user.username == "c" and occasion.name == "P":
                    self.assertNotIn(user, occasion.get_membres())
                else:
                    self.assertIn(user, occasion.get_membres())

    def test_occasion_solde_des_membres(self):
        """Check that members get the right balance."""
        a, b, c = User.objects.all()
        self.assertEqual(
            Occasion.objects.first().solde_des_membres(), [(3, a), (0, b), (-3, c)]
        )

    def test_occasion_depenses(self):
        """Check the total amount of spent money."""
        self.assertEqual(Occasion.objects.first().depenses(), 9)

    # Dette

    def test_dette_str(self):
        """Check the string representation of a Dette."""
        self.assertEqual(
            str(Dette.objects.first()), "a a payé 9.00 € à a, b & c pour «Lorem Ipsum»"
        )

    def test_dette_debiteurs_list(self):
        """Check the string representation of the list of debitors."""
        dette = Dette.objects.first()
        self.assertEqual(dette.debiteurs_list(), "a, b & c")
        dette.debiteurs.remove(User.objects.first())
        dette.debiteurs.remove(User.objects.last())
        self.assertEqual(dette.debiteurs_list(), "b")

    def test_dette_part(self):
        """Check the share of a Dette."""
        self.assertEqual(Dette.objects.first().part(), 3)

    # Remboursement

    def test_remboursement_str(self):
        """Check the string representation of a Remboursement."""
        self.assertEqual(str(Remboursement.objects.first()), "b a remboursé 3.00 € à a")

    # VIEWS

    def test_access_home(self):
        """Check access rights on the main page."""
        self.assertEqual(self.client.get(reverse("comptes:home")).status_code, 302)
        self.client.login(username="a", password="a")
        self.assertEqual(self.client.get(reverse("comptes:home")).status_code, 200)

    def test_access_occasion(self):
        """Check access rights on a given Occasion."""
        self.assertEqual(
            self.client.get(
                reverse("comptes:occasion", kwargs={"slug": "p"})
            ).status_code,
            302,
        )
        self.client.login(username="a", password="a")
        self.assertEqual(
            self.client.get(
                reverse("comptes:occasion", kwargs={"slug": "p"})
            ).status_code,
            200,
        )
        self.client.login(username="c", password="c")
        self.assertEqual(
            self.client.get(
                reverse("comptes:occasion", kwargs={"slug": "p"})
            ).status_code,
            403,
        )

    def test_access_dette(self):
        """Check access rights on a Dette."""
        self.client.login(username="a", password="a")
        self.assertEqual(
            self.client.get(
                reverse("comptes:dette", kwargs={"oc_slug": "p"})
            ).status_code,
            200,
        )
        self.client.login(username="c", password="c")
        self.assertEqual(
            self.client.get(
                reverse("comptes:dette", kwargs={"oc_slug": "p"})
            ).status_code,
            403,
        )

    def test_create_dette(self):
        """Check the creation of a Dette."""
        self.client.login(username="a", password="a")

        dette_data = {
            "creancier": 1,
            "debiteurs": [2],
            "montant": 20,
            "description": "test",
            "moment_0": date(1990, 6, 14),
            "moment_1": time(4, 2),
        }
        r = self.client.post(
            reverse("comptes:dette", kwargs={"oc_slug": "p"}), dette_data
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/comptes/p")

        dette_data["add_another"] = 1
        r = self.client.post(
            reverse("comptes:dette", kwargs={"oc_slug": "p"}), dette_data
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/comptes/p/dette")

    def test_create_remboursement(self):
        """Check the creation of a Remboursement."""
        self.assertEqual(len(mail.outbox), 0)
        dette_data = {
            "crediteur": 2,
            "credite": 3,
            "montant": 20,
            "moment_0": date(1990, 6, 14),
            "moment_1": time(4, 2),
        }

        r = self.client.post(
            reverse("comptes:remboursement", kwargs={"oc_slug": "o"}), dette_data
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/accounts/login/?next=/comptes/o/remboursement")

        self.client.login(username="a", password="a")

        r = self.client.post(
            reverse("comptes:remboursement", kwargs={"oc_slug": "o"}), dette_data
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, "/comptes/o")

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("</li>", mail.outbox[0].alternatives[0][0])
        self.assertIn("a a ajouté", mail.outbox[0].alternatives[0][0])
