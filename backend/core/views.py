import datetime
import hashlib
import secrets
import math

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import models
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date
from .models import (
    Utilisateur, Role, AuditLog,
    Client, Chauffeur, Vehicule, Destination, TypeService, Tarification,
    Expedition, TrackingExpedition, Tournee,
    Incident, IncidentAttachment, Alerte,
    Reclamation,
    Facture, FactureExpedition, Paiement,
    PasswordResetToken
)
from .serializers import (
    LoginSerializer, UtilisateurSerializer, UtilisateurCreateSerializer,
    UtilisateurUpdateSerializer, PasswordResetSerializer, AuditLogSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    RoleSerializer, ClientSerializer, ChauffeurSerializer, VehiculeSerializer,
    DestinationSerializer, TypeServiceSerializer, TarificationSerializer,
    ExpeditionSerializer, TrackingExpeditionSerializer, TourneeSerializer,
    IncidentSerializer, AlerteSerializer,
    ReclamationSerializer,
    FactureSerializer, FactureExpeditionSerializer, PaiementSerializer
)
from .permissions import IsAuthenticated, IsAdminSysteme, IsAgentAdministratif
from .utils import create_audit_log


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint de connexion.
    Authentifie l'utilisateur et crée une session.
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Renouveler la clé de session pour éviter la fixation de session
        try:
            request.session.cycle_key()
        except Exception:
            # En dernier recours, flush
            request.session.flush()
        
        # Créer la session
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        request.session['role_code'] = user.role.code
        
        # Log de connexion réussie
        create_audit_log(
            user=user,
            action_type='LOGIN_SUCCESS',
            request=request
        )
        
        user_data = UtilisateurSerializer(user).data
        return Response({
            'message': 'Connexion réussie',
            'user': user_data
        }, status=status.HTTP_200_OK)
    else:
        # Log de connexion échouée
        username = request.data.get('username', 'unknown')
        create_audit_log(
            username=username,
            action_type='LOGIN_FAILED',
            request=request,
            details={'errors': serializer.errors}
        )
        
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """
    Endpoint de déconnexion.
    Détruit la session utilisateur.
    Toujours sans erreur, même si non authentifié.
    """
    # Log de déconnexion si on a un utilisateur attaché
    try:
        if hasattr(request, 'user_obj') and request.user_obj:
            create_audit_log(
                user=request.user_obj,
                action_type='LOGOUT',
                request=request
            )
    finally:
        # Détruire la session quelle que soit la situation
        try:
            request.session.flush()
        except Exception:
            pass
    
    return Response({
        'message': 'Déconnexion réussie'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    if hasattr(request, 'user_obj') and request.user_obj:
        serializer = UtilisateurSerializer(request.user_obj)
        return Response(serializer.data)
    # Session invalide ou absente: la nettoyer explicitement
    try:
        request.session.flush()
    except Exception:
        pass
    return Response(
        {'detail': 'Non authentifié'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@ensure_csrf_cookie
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    Endpoint pour obtenir le token CSRF.
    """
    return Response({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    user = Utilisateur.objects.filter(email__iexact=email, is_active=True).first()

    # Always return success to avoid email enumeration.
    if not user:
        return Response({'message': 'Si le compte existe, un email a été envoyé.'}, status=status.HTTP_200_OK)

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

    expires_at = timezone.now() + datetime.timedelta(hours=1)
    PasswordResetToken.objects.create(user=user, token_hash=token_hash, expires_at=expires_at)

    frontend_base = getattr(settings, 'FRONTEND_BASE_URL', 'http://localhost:3000')
    reset_link = f"{frontend_base}/reset-password?token={raw_token}"

    subject = "Réinitialisation du mot de passe"
    body = (
        f"Bonjour {user.get_full_name()},\n\n"
        f"Vous avez demandé la réinitialisation de votre mot de passe.\n"
        f"Cliquez sur le lien suivant pour définir un nouveau mot de passe (valide 1 heure):\n\n"
        f"{reset_link}\n\n"
        f"Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email.\n"
    )

    send_mail(
        subject,
        body,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost'),
        [user.email],
        fail_silently=True,
    )

    create_audit_log(
        user=user,
        action_type='PASSWORD_RESET',
        request=request,
        details={'mode': 'self_service_request'},
    )

    return Response({'message': 'Si le compte existe, un email a été envoyé.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    raw_token = serializer.validated_data['token']
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

    token_obj = PasswordResetToken.objects.select_related('user').filter(token_hash=token_hash).first()
    if not token_obj or not token_obj.is_valid():
        return Response({'detail': 'Token invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)

    user = token_obj.user
    user.password = make_password(serializer.validated_data['new_password'])
    user.save(update_fields=['password'])

    token_obj.used_at = timezone.now()
    token_obj.save(update_fields=['used_at'])

    create_audit_log(
        user=user,
        action_type='PASSWORD_RESET',
        request=request,
        details={'mode': 'self_service_confirm'},
    )

    return Response({'message': 'Mot de passe mis à jour avec succès.'}, status=status.HTTP_200_OK)


def _parse_period(request):
    end = parse_date(request.query_params.get('end') or '')
    start = parse_date(request.query_params.get('start') or '')

    if end is None:
        end_dt = timezone.now().date()
    else:
        end_dt = end

    if start is None:
        start_dt = end_dt - datetime.timedelta(days=365)
    else:
        start_dt = start

    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    return start_dt, end_dt


def _fill_month_series(rows, start_dt, end_dt, key='count'):
    def _month_key(val):
        if val is None:
            return None
        if hasattr(val, 'date') and callable(getattr(val, 'date')):
            val = val.date()
        return val.replace(day=1)

    by_month = {k: (r.get(key) or 0) for r in rows if (k := _month_key(r.get('month'))) is not None}
    out = []
    cur = datetime.date(start_dt.year, start_dt.month, 1)
    end_month = datetime.date(end_dt.year, end_dt.month, 1)
    while cur <= end_month:
        out.append({'month': cur.isoformat(), key: float(by_month.get(cur, 0))})
        if cur.month == 12:
            cur = datetime.date(cur.year + 1, 1, 1)
        else:
            cur = datetime.date(cur.year, cur.month + 1, 1)
    return out


def _growth_rate(current, previous):
    if previous in (None, 0):
        return None
    return round(((current - previous) / previous) * 100.0, 2)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_summary_view(request):
    start_dt, end_dt = _parse_period(request)
    prev_end = start_dt
    prev_start = start_dt - (end_dt - start_dt)

    # Shipments
    exp_current_qs = Expedition.objects.filter(date_creation__date__gte=start_dt, date_creation__date__lte=end_dt)
    exp_prev_qs = Expedition.objects.filter(date_creation__date__gte=prev_start, date_creation__date__lt=prev_end)
    shipments_total = exp_current_qs.count()
    shipments_prev = exp_prev_qs.count()
    shipments_growth = _growth_rate(shipments_total, shipments_prev)

    shipments_by_month_rows = (
        exp_current_qs.annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    shipments_series = _fill_month_series(shipments_by_month_rows, start_dt, end_dt, key='count')

    # Revenue (invoiced)
    fac_current_qs = Facture.objects.filter(date_facture__gte=start_dt, date_facture__lte=end_dt)
    fac_prev_qs = Facture.objects.filter(date_facture__gte=prev_start, date_facture__lt=prev_end)
    revenue_total = fac_current_qs.aggregate(v=Sum('total_ttc'))['v'] or 0
    revenue_prev = fac_prev_qs.aggregate(v=Sum('total_ttc'))['v'] or 0
    revenue_growth = _growth_rate(revenue_total, revenue_prev)

    revenue_by_month_rows = (
        fac_current_qs.annotate(month=TruncMonth('date_facture'))
        .values('month')
        .annotate(total=Sum('total_ttc'))
        .order_by('month')
    )
    revenue_series = _fill_month_series(revenue_by_month_rows, start_dt, end_dt, key='total')

    # Routes (completed)
    tour_current_qs = Tournee.objects.filter(date_tournee__gte=start_dt, date_tournee__lte=end_dt)
    tour_prev_qs = Tournee.objects.filter(date_tournee__gte=prev_start, date_tournee__lt=prev_end)
    routes_completed_total = tour_current_qs.filter(statut='Terminée').count()
    routes_completed_prev = tour_prev_qs.filter(statut='Terminée').count()
    routes_growth = _growth_rate(routes_completed_total, routes_completed_prev)

    # Delivery success rate
    delivered = exp_current_qs.filter(statut='Livré').count()
    failed = exp_current_qs.filter(statut='Échec de livraison').count()
    denom = delivered + failed
    success_rate = round((delivered / denom) * 100.0, 2) if denom else None

    # Top customers by volume
    top_customers_volume = (
        exp_current_qs.values('client_id', 'client__nom', 'client__prenom')
        .annotate(shipments=Count('id'))
        .order_by('-shipments')[:10]
    )
    top_customers_volume = [
        {
            'client_id': r['client_id'],
            'client_name': (f"{r['client__nom']} {r['client__prenom']}".strip() if r['client__prenom'] else r['client__nom']),
            'shipments': r['shipments'],
        }
        for r in top_customers_volume
        if r['client_id'] is not None
    ]

    # Top customers by revenue
    top_customers_revenue = (
        fac_current_qs.values('client_id', 'client__nom', 'client__prenom')
        .annotate(revenue=Sum('total_ttc'))
        .order_by('-revenue')[:10]
    )
    top_customers_revenue = [
        {
            'client_id': r['client_id'],
            'client_name': (f"{r['client__nom']} {r['client__prenom']}".strip() if r['client__prenom'] else r['client__nom']),
            'revenue': float(r['revenue'] or 0),
        }
        for r in top_customers_revenue
        if r['client_id'] is not None
    ]

    # Top destinations
    top_destinations = (
        exp_current_qs.values('destination_id', 'destination__ville', 'destination__pays', 'destination__zone_geographique')
        .annotate(shipments=Count('id'))
        .order_by('-shipments')[:10]
    )
    top_destinations = [
        {
            'destination_id': r['destination_id'],
            'label': f"{r['destination__ville']}, {r['destination__pays']}",
            'zone': r['destination__zone_geographique'],
            'shipments': r['shipments'],
        }
        for r in top_destinations
        if r['destination_id'] is not None
    ]

    # Incidents by zone (based on expedition destination)
    incident_current_qs = Incident.objects.filter(created_at__date__gte=start_dt, created_at__date__lte=end_dt)
    incident_zones = (
        incident_current_qs.filter(expedition__isnull=False)
        .values('expedition__destination__zone_geographique')
        .annotate(incidents=Count('id'))
        .order_by('-incidents')
    )
    incident_zones = [
        {'zone': r['expedition__destination__zone_geographique'] or 'N/A', 'incidents': r['incidents']}
        for r in incident_zones
    ]

    top_zones_by_shipments = (
        exp_current_qs.values('destination__zone_geographique')
        .annotate(shipments=Count('id'))
        .order_by('-shipments')[:10]
    )
    top_zones_by_shipments = [
        {'zone': r['destination__zone_geographique'] or 'N/A', 'shipments': r['shipments']}
        for r in top_zones_by_shipments
    ]

    top_zones_by_incidents = incident_zones[:10]

    # Top drivers (completed routes + incidents)
    driver_rows = (
        tour_current_qs.filter(statut='Terminée', chauffeur__isnull=False)
        .values('chauffeur_id', 'chauffeur__nom', 'chauffeur__prenom')
        .annotate(
            tournees=Count('id'),
            distance=Sum('distance_km'),
            fuel=Sum('consommation_litres'),
            incidents=Count('incidents', distinct=True),
        )
        .order_by('-tournees')[:10]
    )
    top_drivers = []
    for r in driver_rows:
        score = (r['tournees'] or 0) - 0.5 * (r['incidents'] or 0)
        top_drivers.append({
            'chauffeur_id': r['chauffeur_id'],
            'name': f"{r['chauffeur__nom']} {r['chauffeur__prenom']}",
            'tournees_completed': r['tournees'] or 0,
            'distance_km': float(r['distance'] or 0),
            'fuel_l': float(r['fuel'] or 0),
            'incidents': r['incidents'] or 0,
            'score': round(score, 2),
        })

    # Peak periods (top 6 months by shipments)
    peak_months = sorted(shipments_series, key=lambda x: x['count'], reverse=True)[:6]

    # Forecast (simple moving average of last 3 months)
    def _forecast(series, key):
        vals = [s[key] for s in series if s[key] is not None]
        if len(vals) < 3:
            return []
        window = vals[-3:]
        avg = sum(window) / 3.0
        last_month = datetime.date.fromisoformat(series[-1]['month'])
        out = []
        cur = last_month
        for _ in range(3):
            if cur.month == 12:
                cur = datetime.date(cur.year + 1, 1, 1)
            else:
                cur = datetime.date(cur.year, cur.month + 1, 1)
            out.append({'month': cur.isoformat(), key: round(float(avg), 2)})
        return out

    shipments_forecast = _forecast(shipments_series, 'count')
    revenue_forecast = _forecast(revenue_series, 'total')

    return Response({
        'period': {'start': start_dt.isoformat(), 'end': end_dt.isoformat()},
        'shipments': {
            'total': shipments_total,
            'growth_rate_percent': shipments_growth,
            'delivered': delivered,
            'failed': failed,
            'success_rate_percent': success_rate,
            'series': shipments_series,
            'forecast_next_3_months': shipments_forecast,
        },
        'revenue': {
            'total_ttc': round(float(revenue_total), 2),
            'growth_rate_percent': revenue_growth,
            'series': revenue_series,
            'forecast_next_3_months': revenue_forecast,
        },
        'routes': {
            'completed': routes_completed_total,
            'growth_rate_percent': routes_growth,
        },
        'rankings': {
            'top_customers_by_volume': top_customers_volume,
            'top_customers_by_revenue': top_customers_revenue,
            'top_destinations': top_destinations,
            'top_drivers': top_drivers,
        },
        'incidents': {
            'by_zone': incident_zones,
        },
        'peaks': {
            'months': peak_months,
        },
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_advanced_view(request):
    import traceback
    try:
        start_dt, end_dt = _parse_period(request)
        prev_end = start_dt
        prev_start = start_dt - (end_dt - start_dt)

        exp_current_qs = Expedition.objects.filter(date_creation__date__gte=start_dt, date_creation__date__lte=end_dt)
        exp_prev_qs = Expedition.objects.filter(date_creation__date__gte=prev_start, date_creation__date__lt=prev_end)
        fac_current_qs = Facture.objects.filter(date_facture__gte=start_dt, date_facture__lte=end_dt)
        fac_prev_qs = Facture.objects.filter(date_facture__gte=prev_start, date_facture__lt=prev_end)
        tour_current_qs = Tournee.objects.filter(date_tournee__gte=start_dt, date_tournee__lte=end_dt)
        tour_prev_qs = Tournee.objects.filter(date_tournee__gte=prev_start, date_tournee__lt=prev_end)
        incident_current_qs = Incident.objects.filter(created_at__date__gte=start_dt, created_at__date__lte=end_dt)
        incident_prev_qs = Incident.objects.filter(created_at__date__gte=prev_start, created_at__date__lt=prev_end)

        def _forecast(series, key):
            vals = [s[key] for s in series if s.get(key) is not None]
            if len(vals) < 3:
                return []
            window = vals[-3:]
            avg = sum(window) / 3.0
            last_month = datetime.date.fromisoformat(series[-1]['month'])
            out = []
            cur = last_month
            for _ in range(3):
                if cur.month == 12:
                    cur = datetime.date(cur.year + 1, 1, 1)
                else:
                    cur = datetime.date(cur.year, cur.month + 1, 1)
                out.append({'month': cur.isoformat(), key: round(float(avg), 2)})
            return out

        shipments_total = exp_current_qs.count()
        shipments_prev = exp_prev_qs.count()
        shipments_growth = _growth_rate(shipments_total, shipments_prev)

        delivered = exp_current_qs.filter(statut='Livré').count()
        failed = exp_current_qs.filter(statut='Échec de livraison').count()
        delayed = exp_current_qs.filter(incidents__type_incident='RETARD').distinct().count()

        denom = delivered + failed
        success_rate = round((delivered / denom) * 100.0, 2) if denom else None
        failed_rate = round((failed / denom) * 100.0, 2) if denom else None
        delayed_rate = round((delayed / shipments_total) * 100.0, 2) if shipments_total else None

        shipments_by_month_rows = (
            exp_current_qs.annotate(month=TruncMonth('date_creation'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        shipments_series = _fill_month_series(shipments_by_month_rows, start_dt, end_dt, key='count')
        shipments_forecast = _forecast(shipments_series, 'count')

        revenue_total = fac_current_qs.aggregate(v=Sum('total_ttc'))['v'] or 0
        revenue_prev = fac_prev_qs.aggregate(v=Sum('total_ttc'))['v'] or 0
        revenue_growth = _growth_rate(revenue_total, revenue_prev)

        revenue_by_month_rows = (
            fac_current_qs.annotate(month=TruncMonth('date_facture'))
            .values('month')
            .annotate(total=Sum('total_ttc'))
            .order_by('month')
        )
        revenue_series = _fill_month_series(revenue_by_month_rows, start_dt, end_dt, key='total')
        revenue_forecast = _forecast(revenue_series, 'total')

        routes_completed_total = tour_current_qs.filter(statut='Terminée').count()
        routes_completed_prev = tour_prev_qs.filter(statut='Terminée').count()
        routes_growth = _growth_rate(routes_completed_total, routes_completed_prev)

        routes_by_month_rows = (
            tour_current_qs.filter(statut='Terminée')
            .annotate(month=TruncMonth('date_tournee'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        routes_series = _fill_month_series(routes_by_month_rows, start_dt, end_dt, key='count')
        routes_forecast = _forecast(routes_series, 'count')

        fuel_by_month_rows = (
            tour_current_qs.filter(statut='Terminée')
            .annotate(month=TruncMonth('date_tournee'))
            .values('month')
            .annotate(total=Sum('consommation_litres'))
            .order_by('month')
        )
        fuel_series = _fill_month_series(fuel_by_month_rows, start_dt, end_dt, key='total')
        fuel_forecast = _forecast(fuel_series, 'total')

        total_distance = tour_current_qs.filter(statut='Terminée').aggregate(v=Sum('distance_km'))['v'] or 0
        total_fuel = tour_current_qs.filter(statut='Terminée').aggregate(v=Sum('consommation_litres'))['v'] or 0
        fuel_per_100km = round((float(total_fuel) / float(total_distance)) * 100.0, 2) if total_distance else None

        incidents_total = incident_current_qs.count()
        incidents_prev = incident_prev_qs.count()
        incidents_growth = _growth_rate(incidents_total, incidents_prev)

        incidents_by_month_rows = (
            incident_current_qs.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        incidents_series = _fill_month_series(incidents_by_month_rows, start_dt, end_dt, key='count')
        incidents_forecast = _forecast(incidents_series, 'count')

        # Incidents by zone
        incident_zones = (
            incident_current_qs.filter(expedition__isnull=False)
            .values('expedition__destination__zone_geographique')
            .annotate(incidents=Count('id'))
            .order_by('-incidents')
        )
        incident_zones = [
            {'zone': r['expedition__destination__zone_geographique'] or 'N/A', 'incidents': r['incidents']}
            for r in incident_zones
        ]

        top_zones_by_shipments = (
            exp_current_qs.values('destination__zone_geographique')
            .annotate(shipments=Count('id'))
            .order_by('-shipments')[:10]
        )
        top_zones_by_shipments = [
            {'zone': r['destination__zone_geographique'] or 'N/A', 'shipments': r['shipments']}
            for r in top_zones_by_shipments
        ]

        top_zones_by_incidents = incident_zones[:10]

        # Peak periods
        peak_months = sorted(shipments_series, key=lambda x: x['count'], reverse=True)[:6]

        # Top customers by volume
        top_customers_volume = (
            exp_current_qs.values('client_id', 'client__nom', 'client__prenom')
            .annotate(shipments=Count('id'))
            .order_by('-shipments')[:10]
        )
        top_customers_volume = [
            {
                'client_id': r['client_id'],
                'client_name': (f"{r['client__nom']} {r['client__prenom']}".strip() if r['client__prenom'] else r['client__nom']),
                'shipments': r['shipments'],
            }
            for r in top_customers_volume
            if r['client_id'] is not None
        ]

        # Top customers by revenue
        top_customers_revenue = (
            fac_current_qs.values('client_id', 'client__nom', 'client__prenom')
            .annotate(revenue=Sum('total_ttc'))
            .order_by('-revenue')[:10]
        )
        top_customers_revenue = [
            {
                'client_id': r['client_id'],
                'client_name': (f"{r['client__nom']} {r['client__prenom']}".strip() if r['client__prenom'] else r['client__nom']),
                'revenue': float(r['revenue'] or 0),
            }
            for r in top_customers_revenue
            if r['client_id'] is not None
        ]

        # Top destinations
        top_destinations = (
            exp_current_qs.values(
                'destination_id',
                'destination__ville',
                'destination__pays',
                'destination__zone_geographique',
                'destination__latitude',
                'destination__longitude',
            )
            .annotate(shipments=Count('id'))
            .order_by('-shipments')[:10]
        )
        top_destinations = [
            {
                'destination_id': r['destination_id'],
                'label': f"{r['destination__ville']}, {r['destination__pays']}",
                'zone': r['destination__zone_geographique'],
                'shipments': r['shipments'],
                'latitude': r['destination__latitude'],
                'longitude': r['destination__longitude'],
            }
            for r in top_destinations
            if r['destination_id'] is not None
        ]

        # Top drivers
        driver_rows = (
            tour_current_qs.filter(statut='Terminée', chauffeur__isnull=False)
            .values('chauffeur_id', 'chauffeur__nom', 'chauffeur__prenom')
            .annotate(
                tournees=Count('id'),
                distance=Sum('distance_km'),
                fuel=Sum('consommation_litres'),
                duree=Sum('duree_minutes'),
                incidents=Count('incidents', distinct=True),
                delivered_shipments=Count('expeditions', filter=Q(expeditions__statut='Livré'), distinct=True),
                failed_shipments=Count('expeditions', filter=Q(expeditions__statut='Échec de livraison'), distinct=True),
                delayed_shipments=Count('expeditions', filter=Q(expeditions__incidents__type_incident='RETARD'), distinct=True),
            )
            .order_by('-tournees')[:20]
        )
        top_drivers = []
        for r in driver_rows:
            tours = float(r['tournees'] or 0)
            incidents = float(r['incidents'] or 0)
            distance = float(r['distance'] or 0)
            fuel = float(r['fuel'] or 0)
            duree_min = float(r['duree'] or 0)
            delivered_shipments = float(r['delivered_shipments'] or 0)
            failed_shipments = float(r['failed_shipments'] or 0)
            delayed_shipments = float(r['delayed_shipments'] or 0)

            speed_kmh = round((distance / (duree_min / 60.0)), 2) if duree_min else None
            deliveries_per_100km = round((delivered_shipments / distance) * 100.0, 2) if distance else None
            deliveries_per_liter = round((delivered_shipments / fuel), 2) if fuel else None
            punctuality_proxy = round((delivered_shipments / (delivered_shipments + delayed_shipments)) * 100.0, 2) if (delivered_shipments + delayed_shipments) else None
            quality_proxy = round((delivered_shipments / (delivered_shipments + failed_shipments)) * 100.0, 2) if (delivered_shipments + failed_shipments) else None

            score = (tours * 1.0) + (delivered_shipments * 0.2) - (incidents * 0.8) - (failed_shipments * 0.6) - (delayed_shipments * 0.3)
            top_drivers.append({
                'chauffeur_id': r['chauffeur_id'],
                'name': f"{r['chauffeur__nom']} {r['chauffeur__prenom']}",
                'tournees_completed': int(tours),
                'distance_km': distance,
                'fuel_l': fuel,
                'incidents': int(incidents),
                'delivered_shipments': int(delivered_shipments),
                'failed_shipments': int(failed_shipments),
                'delayed_shipments': int(delayed_shipments),
                'speed_kmh': speed_kmh,
                'deliveries_per_100km': deliveries_per_100km,
                'deliveries_per_liter': deliveries_per_liter,
                'punctuality_percent': punctuality_proxy,
                'quality_percent': quality_proxy,
                'score': round(float(score), 2),
            })
        top_drivers = sorted(top_drivers, key=lambda x: x['score'], reverse=True)[:10]

        # Profitability assumptions
        fuel_price_per_liter = float(request.query_params.get('fuel_price_per_liter', 1.5))
        driver_cost_per_hour = float(request.query_params.get('driver_cost_per_hour', 8.0))
        vehicle_cost_per_km = float(request.query_params.get('vehicle_cost_per_km', 0.3))

        # Cost estimation
        route_cost_total = 0.0
        for t in tour_current_qs.filter(statut='Terminée').only('distance_km', 'duree_minutes', 'consommation_litres'):
            dist = float(t.distance_km or 0)
            fuel_l = float(t.consommation_litres or 0)
            minutes = float(t.duree_minutes or 0)
            route_cost_total += (fuel_l * fuel_price_per_liter) + ((minutes / 60.0) * driver_cost_per_hour) + (dist * vehicle_cost_per_km)

        avg_cost_per_route = round((route_cost_total / routes_completed_total), 2) if routes_completed_total else None
        avg_shipments_per_route = round((shipments_total / routes_completed_total), 2) if routes_completed_total else None

        revenue_estimated = exp_current_qs.aggregate(v=Sum('montant_total'))['v'] or 0
        profit_estimated = round(float(revenue_estimated) - float(route_cost_total), 2)
        margin_percent = round((profit_estimated / float(revenue_estimated)) * 100.0, 2) if revenue_estimated else None

        # Profitability by service type
        revenue_by_service_rows = (
            exp_current_qs.values('type_service_id', 'type_service__libelle')
            .annotate(revenue=Sum('montant_total'), shipments=Count('id'))
            .order_by('-revenue')
        )
        profitability_by_service = []
        for r in revenue_by_service_rows:
            share = (float(r['revenue'] or 0) / float(revenue_estimated)) if revenue_estimated else 0
            cost_alloc = route_cost_total * share
            rev = float(r['revenue'] or 0)
            prof = rev - cost_alloc
            profitability_by_service.append({
                'type_service_id': r['type_service_id'],
                'type_service': r['type_service__libelle'] or 'N/A',
                'shipments': r['shipments'],
                'revenue_estimated': round(rev, 2),
                'cost_estimated': round(float(cost_alloc), 2),
                'profit_estimated': round(float(prof), 2),
                'margin_percent': round((prof / rev) * 100.0, 2) if rev else None,
            })

        # Staffing forecasts
        cap_shipments_per_vehicle_per_day = float(request.query_params.get('cap_shipments_per_vehicle_per_day', 30))
        cap_shipments_per_driver_per_day = float(request.query_params.get('cap_shipments_per_driver_per_day', 25))
        working_days_per_month = float(request.query_params.get('working_days_per_month', 22))

        def _staffing_from_monthly_shipments(monthly_shipments):
            denom_vehicle = cap_shipments_per_vehicle_per_day * working_days_per_month
            denom_driver = cap_shipments_per_driver_per_day * working_days_per_month
            vehicles = math.ceil(monthly_shipments / denom_vehicle) if denom_vehicle else None
            drivers = math.ceil(monthly_shipments / denom_driver) if denom_driver else None
            return vehicles, drivers

        staffing_forecast = []
        for row in shipments_forecast:
            m = row['month']
            vol = float(row['count'] or 0)
            vehicles, drivers = _staffing_from_monthly_shipments(vol)
            staffing_forecast.append({
                'month': m,
                'forecast_shipments': round(vol, 2),
                'required_vehicles': vehicles,
                'required_drivers': drivers,
            })

        # Map points
        destination_points = (
            exp_current_qs.values(
                'destination_id',
                'destination__ville',
                'destination__pays',
                'destination__zone_geographique',
                'destination__latitude',
                'destination__longitude',
            )
            .annotate(shipments=Count('id'), incidents=Count('incidents', distinct=True))
            .order_by('-shipments')
        )
        destination_points = [
            {
                'destination_id': r['destination_id'],
                'label': f"{r['destination__ville']}, {r['destination__pays']}",
                'zone': r['destination__zone_geographique'],
                'latitude': r['destination__latitude'],
                'longitude': r['destination__longitude'],
                'shipments': r['shipments'],
                'incidents': r['incidents'],
            }
            for r in destination_points
            if r['destination_id'] is not None and r['destination__latitude'] is not None and r['destination__longitude'] is not None
        ]

        return Response({
            'period': {'start': start_dt.isoformat(), 'end': end_dt.isoformat()},
            'shipments': {
                'total': shipments_total,
                'growth_rate_percent': shipments_growth,
                'delivered': delivered,
                'failed': failed,
                'delayed': delayed,
                'success_rate_percent': success_rate,
                'failed_rate_percent': failed_rate,
                'delayed_rate_percent': delayed_rate,
                'series': shipments_series,
                'forecast_next_3_months': shipments_forecast,
            },
            'revenue': {
                'total_ttc': round(float(revenue_total), 2),
                'growth_rate_percent': revenue_growth,
                'series': revenue_series,
                'forecast_next_3_months': revenue_forecast,
            },
            'routes': {
                'completed': routes_completed_total,
                'growth_rate_percent': routes_growth,
                'series': routes_series,
                'forecast_next_3_months': routes_forecast,
            },
            'fuel': {
                'total_liters': round(float(total_fuel), 2),
                'fuel_per_100km': fuel_per_100km,
                'series': fuel_series,
                'forecast_next_3_months': fuel_forecast,
            },
            'incidents': {
                'total': incidents_total,
                'growth_rate_percent': incidents_growth,
                'series': incidents_series,
                'forecast_next_3_months': incidents_forecast,
                'by_zone': incident_zones,
            },
            'operations': {
                'avg_cost_per_route_estimated': avg_cost_per_route,
                'avg_shipments_per_route': avg_shipments_per_route,
            },
            'profitability': {
                'assumptions': {
                    'fuel_price_per_liter': fuel_price_per_liter,
                    'driver_cost_per_hour': driver_cost_per_hour,
                    'vehicle_cost_per_km': vehicle_cost_per_km,
                },
                'revenue_estimated_from_shipments': round(float(revenue_estimated), 2),
                'cost_estimated_from_routes': round(float(route_cost_total), 2),
                'profit_estimated': profit_estimated,
                'margin_percent': margin_percent,
                'by_service_type': profitability_by_service,
            },
            'rankings': {
                'top_customers_by_volume': top_customers_volume,
                'top_customers_by_revenue': top_customers_revenue,
                'top_destinations': top_destinations,
                'top_drivers': top_drivers,
            },
            'staffing': {
                'assumptions': {
                    'cap_shipments_per_vehicle_per_day': cap_shipments_per_vehicle_per_day,
                    'cap_shipments_per_driver_per_day': cap_shipments_per_driver_per_day,
                    'working_days_per_month': working_days_per_month,
                },
                'forecast_next_3_months': staffing_forecast,
            },
            'map': {
                'destination_points': destination_points,
            },
            'zones': {
                'top_by_shipments': top_zones_by_shipments,
                'top_by_incidents': top_zones_by_incidents,
            },
            'peaks': {
                'months': peak_months,
            },
        })
    except Exception as e:
        print("[ANALYTICS ADVANCED ERROR]")
        traceback.print_exc()
        raise


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_roles(request):
    """
    Retourne la liste des rôles disponibles.
    """
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)


class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs.
    Accessible uniquement par l'Administrateur Système.
    """
    queryset = Utilisateur.objects.select_related('role').all()
    permission_classes = [IsAuthenticated, IsAdminSysteme]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UtilisateurCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UtilisateurUpdateSerializer
        return UtilisateurSerializer
    
    def create(self, request, *args, **kwargs):
        """Créer un nouvel utilisateur"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log de création
        create_audit_log(
            user=request.user_obj,
            action_type='USER_CREATED',
            request=request,
            details={
                'created_user_id': user.id,
                'created_username': user.username,
                'role_id': user.role_id
            }
        )
        
        return Response(
            UtilisateurSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Modifier un utilisateur"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_role_id = instance.role_id
        old_is_active = instance.is_active
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Log de modification
        details = {
            'modified_user_id': user.id,
            'modified_username': user.username
        }
        
        if old_role_id != user.role_id:
            details['old_role_id'] = old_role_id
            details['new_role_id'] = user.role_id
        
        if old_is_active != user.is_active:
            action_type = (
                'USER_ACTIVATED'
                if user.is_active
                else 'USER_DEACTIVATED'
            )
        else:
            action_type = 'USER_UPDATED'
        
        create_audit_log(
            user=request.user_obj,
            action_type=action_type,
            request=request,
            details=details
        )
        
        return Response(UtilisateurSerializer(user).data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Désactiver un utilisateur au lieu de le supprimer.
        La suppression complète n'est pas autorisée pour la traçabilité.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        
        # Log de désactivation
        create_audit_log(
            user=request.user_obj,
            action_type='USER_DEACTIVATED',
            request=request,
            details={
                'deactivated_user_id': instance.id,
                'deactivated_username': instance.username
            }
        )
        
        return Response(
            {'message': 'Utilisateur désactivé avec succès'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Réinitialiser le mot de passe d'un utilisateur"""
        user = self.get_object()
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.password = make_password(new_password)
            user.save()
            
            # Log de réinitialisation
            create_audit_log(
                user=request.user_obj,
                action_type='PASSWORD_RESET',
                request=request,
                details={
                    'target_user_id': user.id,
                    'target_username': user.username
                }
            )
            
            return Response({
                'message': 'Mot de passe réinitialisé avec succès'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activer un utilisateur"""
        user = self.get_object()
        user.is_active = True
        user.save()
        
        # Log d'activation
        create_audit_log(
            user=request.user_obj,
            action_type='USER_ACTIVATED',
            request=request,
            details={
                'activated_user_id': user.id,
                'activated_username': user.username
            }
        )
        
        return Response({
            'message': 'Utilisateur activé avec succès'
        })
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Désactiver un utilisateur"""
        user = self.get_object()
        user.is_active = False
        user.save()
        
        # Log de désactivation
        create_audit_log(
            user=request.user_obj,
            action_type='USER_DEACTIVATED',
            request=request,
            details={
                'deactivated_user_id': user.id,
                'deactivated_username': user.username
            }
        )
        
        return Response({
            'message': 'Utilisateur désactivé avec succès'
        })


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour consulter les logs d'audit.
    Accessible uniquement par l'Administrateur Système.
    Lecture seule.
    """
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdminSysteme]
    
    def get_queryset(self):
        """Filtrer les logs par utilisateur ou type d'action si spécifié"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        action_type = self.request.query_params.get('action_type', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        return queryset


class BaseAgentViewSet(viewsets.ModelViewSet):
    """Classe de base pour les vues accessibles aux agents"""
    permission_classes = [IsAuthenticated, IsAgentAdministratif | IsAdminSysteme]


class ClientViewSet(BaseAgentViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(nom__icontains=search) | 
                models.Q(prenom__icontains=search) | 
                models.Q(code_client__icontains=search)
            )
        return queryset


class ChauffeurViewSet(BaseAgentViewSet):
    queryset = Chauffeur.objects.all()
    serializer_class = ChauffeurSerializer


class VehiculeViewSet(BaseAgentViewSet):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer


class DestinationViewSet(BaseAgentViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class TypeServiceViewSet(BaseAgentViewSet):
    queryset = TypeService.objects.all()
    serializer_class = TypeServiceSerializer


class TarificationViewSet(BaseAgentViewSet):
    queryset = Tarification.objects.all()
    serializer_class = TarificationSerializer


class ExpeditionViewSet(BaseAgentViewSet):
    queryset = Expedition.objects.all().order_by('-date_creation')
    serializer_class = ExpeditionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        client = self.request.query_params.get('client_id', None)
        tournee_id = self.request.query_params.get('tournee_id', None)
        
        if status:
            # Tolérer les anciennes valeurs (ex: triggers SQL qui écrivaient 'enregistre')
            # pour éviter que l'UI ne "perde" des expéditions à cause d'un simple mismatch de statut.
            s = str(status).strip()
            variants = {s}
            if s in {'Enregistré', 'EnregistrÃ©', 'enregistre', 'enregistré'}:
                variants.update({'Enregistré', 'EnregistrÃ©', 'enregistre', 'enregistré'})
            queryset = queryset.filter(statut__in=list(variants))
        if client:
            queryset = queryset.filter(client_id=client)
        if tournee_id:
            queryset = queryset.filter(tournee_id=tournee_id)
            
        return queryset
        
    def perform_destroy(self, instance):
        # Vérifier si l'expédition est liée à une tournée
        if instance.tournee:
             from rest_framework.exceptions import ValidationError
             raise ValidationError("Impossible de supprimer une expédition liée à une tournée.")
             
        instance.delete()


class TourneeViewSet(BaseAgentViewSet):
    queryset = Tournee.objects.all().order_by('-date_tournee')
    serializer_class = TourneeSerializer


class TrackingExpeditionViewSet(BaseAgentViewSet):
    queryset = TrackingExpedition.objects.all().order_by('-date_statut')
    serializer_class = TrackingExpeditionSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        exp_id = self.request.query_params.get('expedition_id', None)
        if exp_id:
            queryset = queryset.filter(expedition_id=exp_id)
        return queryset


class IncidentViewSet(BaseAgentViewSet):
    queryset = (
        Incident.objects.select_related('expedition', 'tournee', 'created_by')
        .prefetch_related('attachments')
        .all()
    )
    serializer_class = IncidentSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        expedition_id = self.request.query_params.get('expedition_id')
        tournee_id = self.request.query_params.get('tournee_id')
        type_incident = self.request.query_params.get('type_incident')

        if expedition_id:
            queryset = queryset.filter(expedition_id=expedition_id)
        if tournee_id:
            queryset = queryset.filter(tournee_id=tournee_id)
        if type_incident:
            queryset = queryset.filter(type_incident=type_incident)

        return queryset

    def _apply_status_change(self, incident: Incident) -> str:
        now = timezone.now()

        if incident.expedition_id:
            expedition = incident.expedition
            expedition.statut = 'Échec de livraison'
            expedition.save(update_fields=['statut'])

            TrackingExpedition.objects.create(
                expedition=expedition,
                tournee=expedition.tournee,
                chauffeur=expedition.tournee.chauffeur if expedition.tournee else None,
                statut='Échec de livraison',
                lieu=f"Incident {incident.code_incident}",
                commentaire=(incident.commentaire or '').strip() or f"Incident ({incident.get_type_incident_display()})",
                date_statut=now,
            )

            return 'SET_ECHEC_LIVRAISON'

        if incident.tournee_id:
            tournee = incident.tournee
            tournee.statut = 'Annulée'
            tournee.save(update_fields=['statut'])

            for expedition in tournee.expeditions.exclude(statut='Livré').select_related('tournee'):
                expedition.statut = 'Échec de livraison'
                expedition.save(update_fields=['statut'])
                TrackingExpedition.objects.create(
                    expedition=expedition,
                    tournee=tournee,
                    chauffeur=tournee.chauffeur,
                    statut='Échec de livraison',
                    lieu=f"Tournée {tournee.code_tournee} (annulée)",
                    commentaire=(incident.commentaire or '').strip() or f"Incident tournée ({incident.get_type_incident_display()})",
                    date_statut=now,
                )

            return 'SET_ANNULEE'

        return 'NONE'

    def _generate_alertes(self, incident: Incident) -> None:
        exp_code = incident.expedition.code_expedition if incident.expedition_id else None
        trn_code = incident.tournee.code_tournee if incident.tournee_id else None

        ref = exp_code or trn_code or f"#{incident.id}"
        titre = f"Incident {incident.get_type_incident_display()} - {ref}"
        message = (incident.commentaire or '').strip() or "Un incident a été signalé."

        if incident.notify_direction:
            Alerte.objects.create(
                destination='DIRECTION',
                titre=titre,
                message=message,
                incident=incident,
                expedition=incident.expedition if incident.expedition_id else None,
                tournee=incident.tournee if incident.tournee_id else None,
            )

        if incident.notify_client and incident.expedition_id and incident.expedition.client_id:
            Alerte.objects.create(
                destination='CLIENT',
                titre=titre,
                message=message,
                incident=incident,
                expedition=incident.expedition,
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            incident = serializer.save(created_by=getattr(request, 'user_obj', None))

            for f in request.FILES.getlist('files'):
                IncidentAttachment.objects.create(
                    incident=incident,
                    file=f,
                    original_name=getattr(f, 'name', None),
                    uploaded_by=getattr(request, 'user_obj', None),
                )

            action_appliquee = self._apply_status_change(incident)
            if action_appliquee and action_appliquee != incident.action_appliquee:
                incident.action_appliquee = action_appliquee
                incident.save(update_fields=['action_appliquee', 'updated_at'])

            self._generate_alertes(incident)

        out = self.get_serializer(incident)
        headers = self.get_success_headers(out.data)
        return Response(out.data, status=status.HTTP_201_CREATED, headers=headers)


class AlerteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        destination = self.request.query_params.get('destination')
        is_read = self.request.query_params.get('is_read')
        incident_id = self.request.query_params.get('incident_id')

        if destination:
            queryset = queryset.filter(destination=destination)
        if is_read in ('true', 'false', '0', '1'):
            queryset = queryset.filter(is_read=is_read in ('true', '1'))
        if incident_id:
            queryset = queryset.filter(incident_id=incident_id)

        # Par défaut, restreindre les alertes client aux rôles internes.
        role_code = getattr(getattr(self.request, 'user_obj', None), 'role', None)
        role_code = getattr(role_code, 'code', None)
        if role_code == 'DIRECTION':
            queryset = queryset.filter(destination='DIRECTION')

        return queryset

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        alerte = self.get_object()
        alerte.is_read = True
        alerte.save(update_fields=['is_read'])
        return Response(self.get_serializer(alerte).data, status=status.HTTP_200_OK)


class ReclamationViewSet(BaseAgentViewSet):
    queryset = (
        Reclamation.objects.select_related('client', 'facture', 'type_service', 'traite_par', 'expedition')
        .prefetch_related('expeditions')
        .all()
    )
    serializer_class = ReclamationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        statut = self.request.query_params.get('statut')
        client_id = self.request.query_params.get('client_id')
        facture_id = self.request.query_params.get('facture_id')
        expedition_id = self.request.query_params.get('expedition_id')
        type_service_id = self.request.query_params.get('type_service_id')

        if statut:
            queryset = queryset.filter(statut=statut)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if facture_id:
            queryset = queryset.filter(facture_id=facture_id)
        if type_service_id:
            queryset = queryset.filter(type_service_id=type_service_id)
        if expedition_id:
            queryset = queryset.filter(models.Q(expedition_id=expedition_id) | models.Q(expeditions__id=expedition_id)).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(traite_par=getattr(self.request, 'user_obj', None))

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        reclamation = self.get_object()
        reclamation.statut = 'RESOLUE'
        reclamation.traite_par = getattr(request, 'user_obj', None)
        reclamation.save(update_fields=['statut', 'traite_par'])
        out = self.get_serializer(reclamation)
        return Response(out.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reclamation = self.get_object()
        reclamation.statut = 'ANNULEE'
        reclamation.traite_par = getattr(request, 'user_obj', None)
        reclamation.save(update_fields=['statut', 'traite_par'])
        out = self.get_serializer(reclamation)
        return Response(out.data, status=status.HTTP_200_OK)


class FactureViewSet(BaseAgentViewSet):
    queryset = Facture.objects.all().order_by('-date_facture', '-id')
    serializer_class = FactureSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id')
        statut = self.request.query_params.get('statut')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

    def perform_destroy(self, instance):
        from django.db import transaction
        with transaction.atomic():
            # 1. Libérer les expéditions
            links = FactureExpedition.objects.filter(facture=instance)
            for link in links:
                exp = link.expedition
                exp.est_facturee = False
                exp.save()
            
            # 2. Annuler les paiements et restaurer solde client
            paiements = Paiement.objects.filter(facture=instance)
            for p in paiements:
                if instance.client:
                    instance.client.solde += p.montant
                p.delete()
            
            if instance.client:
                # 3. Restaurer le solde (retirer le montant de la facture)
                instance.client.solde -= instance.total_ttc
                instance.client.save()

            instance.delete()


class PaiementViewSet(BaseAgentViewSet):
    queryset = Paiement.objects.all().order_by('-date_paiement', '-id')
    serializer_class = PaiementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id')
        facture_id = self.request.query_params.get('facture_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if facture_id:
            queryset = queryset.filter(facture_id=facture_id)
        return queryset

    def perform_destroy(self, instance):
        from django.db import transaction
        with transaction.atomic():
            # Restaurer le solde client
            if instance.client:
                instance.client.solde += instance.montant
                instance.client.save()
            
            # Maj statut facture si liée
            facture = instance.facture
            instance.delete()
            
            if facture:
                deja_paye = Paiement.objects.filter(facture=facture).aggregate(models.Sum('montant'))['montant__sum'] or 0
                if deja_paye >= facture.total_ttc:
                    facture.statut = 'Payée'
                elif deja_paye > 0:
                    facture.statut = 'Partiellement Payée'
                else:
                    facture.statut = 'Émise'
                facture.save()

