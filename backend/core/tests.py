import datetime
import json
import re

from django.core import mail
from django.test import TestCase
from django.utils import timezone
from django.test.utils import override_settings
from rest_framework.test import APIClient, APIRequestFactory

from .models import (
    Role,
    Utilisateur,
    Client,
    Destination,
    TypeService,
    Vehicule,
    Chauffeur,
    Tournee,
    Expedition,
    Facture,
    Incident,
    PasswordResetToken,
)
from .views import analytics_advanced_view


@override_settings(DEBUG=False)
class AnalyticsAdvancedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role_admin = Role.objects.create(code='ADMIN', libelle='Admin')
        cls.user = Utilisateur.objects.create(
            username='admin',
            email='admin@example.com',
            password='password123',
            nom='Admin',
            prenom='User',
            role=cls.role_admin,
            is_active=True,
        )

        cls.client_model = Client.objects.create(
            type_client='entreprise',
            nom='Client',
            prenom='A',
            email='clienta@example.com',
        )

        cls.destination = Destination.objects.create(
            pays='Algeria',
            ville='Algiers',
            zone_geographique='Nord',
            code_zone='N1',
            latitude=36.7538,
            longitude=3.0588,
            tarif_base_defaut=100,
            is_active=True,
        )

        cls.type_service = TypeService.objects.create(code='STD', libelle='Standard', is_active=True)
        cls.vehicule = Vehicule.objects.create(
            immatriculation='123-AL-16',
            type_vehicule='Camion',
            capacite_kg=1000,
            capacite_m3=10,
        )
        cls.chauffeur = Chauffeur.objects.create(
            matricule='CHF-00001',
            nom='Driver',
            prenom='One',
            num_permis='PERMIS-1',
        )

        today = timezone.now().date()

        cls.tour_prev = Tournee.objects.create(
            code_tournee='TRN-PREV',
            date_tournee=today - datetime.timedelta(days=35),
            chauffeur=cls.chauffeur,
            vehicule=cls.vehicule,
            statut='Terminée',
            distance_km=100,
            duree_minutes=120,
            consommation_litres=10,
        )
        cls.tour_cur = Tournee.objects.create(
            code_tournee='TRN-CUR',
            date_tournee=today - datetime.timedelta(days=10),
            chauffeur=cls.chauffeur,
            vehicule=cls.vehicule,
            statut='Terminée',
            distance_km=150,
            duree_minutes=180,
            consommation_litres=18,
        )

        # Expeditions: 1 previous period, 2 current period (1 delivered, 1 failed)
        exp_prev = Expedition.objects.create(
            code_expedition='EXP-PREV',
            client=cls.client_model,
            type_service=cls.type_service,
            destination=cls.destination,
            poids_kg=1,
            volume_m3=1,
            statut='Livré',
            montant_total=200,
            tournee=cls.tour_prev,
        )
        exp_cur_ok = Expedition.objects.create(
            code_expedition='EXP-CUR-OK',
            client=cls.client_model,
            type_service=cls.type_service,
            destination=cls.destination,
            poids_kg=1,
            volume_m3=1,
            statut='Livré',
            montant_total=300,
            tournee=cls.tour_cur,
        )
        exp_cur_fail = Expedition.objects.create(
            code_expedition='EXP-CUR-FAIL',
            client=cls.client_model,
            type_service=cls.type_service,
            destination=cls.destination,
            poids_kg=1,
            volume_m3=1,
            statut='Échec de livraison',
            montant_total=150,
            tournee=cls.tour_cur,
        )

        # Override auto_now_add timestamps for period tests
        Expedition.objects.filter(id=exp_prev.id).update(date_creation=timezone.now() - datetime.timedelta(days=40))
        Expedition.objects.filter(id=exp_cur_ok.id).update(date_creation=timezone.now() - datetime.timedelta(days=10))
        Expedition.objects.filter(id=exp_cur_fail.id).update(date_creation=timezone.now() - datetime.timedelta(days=12))

        # Delayed marker via incident type RETARD
        Incident.objects.create(type_incident='RETARD', expedition=exp_cur_ok, tournee=cls.tour_cur)

        # Factures (one previous, one current)
        Facture.objects.create(
            numero_facture='FACT-PREV',
            client=cls.client_model,
            date_facture=today - datetime.timedelta(days=35),
            total_ttc=200,
        )
        Facture.objects.create(
            numero_facture='FACT-CUR',
            client=cls.client_model,
            date_facture=today - datetime.timedelta(days=10),
            total_ttc=450,
        )

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def _login(self):
        res = self.client.post('/api/auth/login/', {'username': 'admin', 'password': 'password123'}, format='json')
        self.assertEqual(res.status_code, 200)

    def test_analytics_advanced_requires_auth(self):
        req = self.factory.get('/api/analytics/advanced/')
        res = analytics_advanced_view(req)
        self.assertIn(res.status_code, [401, 403])

    def test_analytics_advanced_returns_expected_shape(self):
        today = timezone.now().date()
        start = (today - datetime.timedelta(days=30)).isoformat()
        end = today.isoformat()

        req = self.factory.get('/api/analytics/advanced/', {'start': start, 'end': end})
        req.user_obj = self.user
        res = analytics_advanced_view(req)
        self.assertEqual(res.status_code, 200)

        payload = res.data
        self.assertIn('shipments', payload)
        self.assertIn('revenue', payload)
        self.assertIn('routes', payload)
        self.assertIn('fuel', payload)
        self.assertIn('incidents', payload)
        self.assertIn('profitability', payload)
        self.assertIn('staffing', payload)
        self.assertIn('map', payload)

        self.assertGreaterEqual(payload['shipments']['total'], 1)
        self.assertIn('delayed', payload['shipments'])
        self.assertIsInstance(payload['shipments']['series'], list)
        self.assertIsInstance(payload['map']['destination_points'], list)


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    FRONTEND_BASE_URL='http://testserver',
)
class PasswordResetFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        role = Role.objects.create(code='ADMIN_PR', libelle='Admin')
        cls.user = Utilisateur.objects.create(
            username='user1',
            email='user1@example.com',
            password='password123',
            nom='User',
            prenom='One',
            role=role,
            is_active=True,
        )

    def setUp(self):
        self.client = APIClient()
        mail.outbox[:] = []

    def test_password_reset_request_unknown_email_returns_200(self):
        res = self.client.post('/api/auth/password-reset/request/', {'email': 'unknown@example.com'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(PasswordResetToken.objects.count(), 0)

    def test_password_reset_request_and_confirm_success(self):
        res = self.client.post('/api/auth/password-reset/request/', {'email': self.user.email}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(PasswordResetToken.objects.count(), 1)

        self.assertEqual(len(mail.outbox), 1)
        body = mail.outbox[0].body

        m = re.search(r"token=([^\s&]+)", body)
        self.assertIsNotNone(m)
        token = m.group(1)

        res2 = self.client.post(
            '/api/auth/password-reset/confirm/',
            {'token': token, 'new_password': 'newpass123', 'new_password_confirm': 'newpass123'},
            format='json',
        )
        self.assertEqual(res2.status_code, 200)

        # Token should be marked used
        t = PasswordResetToken.objects.first()
        self.assertIsNotNone(t.used_at)

        # Login with new password works
        res3 = self.client.post('/api/auth/login/', {'username': self.user.email, 'password': 'newpass123'}, format='json')
        self.assertEqual(res3.status_code, 200)

    def test_password_reset_confirm_invalid_token(self):
        res = self.client.post(
            '/api/auth/password-reset/confirm/',
            {'token': 'invalid', 'new_password': 'newpass123', 'new_password_confirm': 'newpass123'},
            format='json',
        )
        self.assertEqual(res.status_code, 400)
