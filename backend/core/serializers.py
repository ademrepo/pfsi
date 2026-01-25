from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from .models import (
    Utilisateur, Role, AuditLog,
    Client, Chauffeur, Vehicule, Destination, TypeService, Tarification,
    Expedition, TrackingExpedition, Tournee,
    Incident, IncidentAttachment, Alerte,
    Reclamation, ReclamationExpedition,
    Facture, FactureExpedition, Paiement
)


class LoginSerializer(serializers.Serializer):
    """Serializer pour la connexion utilisateur"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            try:
                if '@' in username:
                    user = Utilisateur.objects.select_related('role').get(email__iexact=username)
                else:
                    user = Utilisateur.objects.select_related('role').get(username=username)
            except Utilisateur.DoesNotExist:
                raise serializers.ValidationError(
                    "Nom d'utilisateur ou mot de passe incorrect."
                )
            
            # Vérifier le mot de passe (hashé ou non selon les données existantes)
            if user.password.startswith('pbkdf2_'):
                # Mot de passe hashé
                if not check_password(password, user.password):
                    raise serializers.ValidationError(
                        "Nom d'utilisateur ou mot de passe incorrect."
                    )
            else:
                # Mot de passe en clair (données de test)
                if user.password != password:
                    raise serializers.ValidationError(
                        "Nom d'utilisateur ou mot de passe incorrect."
                    )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    "Ce compte a été désactivé."
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "Le nom d'utilisateur et le mot de passe sont requis."
            )


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': "Les mots de passe ne correspondent pas."
            })
        return attrs


class RoleSerializer(serializers.ModelSerializer):
    """Serializer pour les rôles"""
    class Meta:
        model = Role
        fields = ['id', 'code', 'libelle']


class UtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour les informations utilisateur"""
    role_display = serializers.CharField(source='role.libelle', read_only=True)
    role_code = serializers.CharField(source='role.code', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'username', 'email', 'nom', 'prenom', 'telephone',
            'role', 'role_display', 'role_code', 'full_name',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UtilisateurCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'utilisateur (admin uniquement)"""
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)
    role_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Utilisateur
        fields = [
            'username', 'email', 'nom', 'prenom', 'telephone',
            'role_id', 'password', 'password_confirm', 'is_active'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def validate_role_id(self, value):
        """Valider que le rôle existe"""
        try:
            Role.objects.get(id=value)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Rôle invalide.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        role_id = validated_data.pop('role_id')
        
        # Hasher le mot de passe
        validated_data['password'] = make_password(password)
        
        # Créer l'utilisateur
        user = Utilisateur.objects.create(**validated_data, role_id=role_id)
        return user


class UtilisateurUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la modification d'utilisateur"""
    role_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prenom', 'telephone', 'role_id', 'is_active']
    
    def validate_role_id(self, value):
        """Valider que le rôle existe"""
        if value:
            try:
                Role.objects.get(id=value)
            except Role.DoesNotExist:
                raise serializers.ValidationError("Rôle invalide.")
        return value
    
    def update(self, instance, validated_data):
        role_id = validated_data.pop('role_id', None)
        if role_id:
            instance.role_id = role_id
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    """Serializer pour la réinitialisation de mot de passe"""
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "Les mots de passe ne correspondent pas."
            })
        return attrs


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer pour les logs d'audit"""
    user_display = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_type_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_display', 'username', 'action_type',
            'action_display', 'ip_address', 'user_agent', 'details', 'timestamp'
        ]
        read_only_fields = fields
    
    def get_user_display(self, obj):
        if obj.user:
            return f"{obj.user.get_full_name()} ({obj.user.username})"
        return obj.username


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ChauffeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chauffeur
        fields = '__all__'


class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
        fields = '__all__'


class TarificationSerializer(serializers.ModelSerializer):
    type_service_details = TypeServiceSerializer(source='type_service', read_only=True)
    destination_details = DestinationSerializer(source='destination', read_only=True)

    class Meta:
        model = Tarification
        fields = '__all__'


class TrackingExpeditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingExpedition
        fields = '__all__'


class IncidentAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = IncidentAttachment
        fields = ['id', 'file', 'file_url', 'original_name', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['uploaded_by', 'uploaded_at']

    def get_file_url(self, obj):
        if obj.file and hasattr(obj.file, 'url'):
            return obj.file.url
        return None


class IncidentSerializer(serializers.ModelSerializer):
    attachments = IncidentAttachmentSerializer(many=True, read_only=True)
    expedition_code = serializers.CharField(source='expedition.code_expedition', read_only=True)
    tournee_code = serializers.CharField(source='tournee.code_tournee', read_only=True)

    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ('code_incident', 'action_appliquee', 'created_by', 'created_at', 'updated_at')

    def validate(self, attrs):
        expedition = attrs.get('expedition') if 'expedition' in attrs else getattr(self.instance, 'expedition', None)
        tournee = attrs.get('tournee') if 'tournee' in attrs else getattr(self.instance, 'tournee', None)

        if bool(expedition) == bool(tournee):
            raise serializers.ValidationError("Vous devez renseigner soit une expédition soit une tournée (pas les deux).")

        # notify_client n'a de sens que pour une expédition (client)
        notify_client = attrs.get('notify_client') if 'notify_client' in attrs else getattr(self.instance, 'notify_client', False)
        if notify_client and not expedition:
            raise serializers.ValidationError({'notify_client': "Disponible uniquement pour un incident lié à une expédition."})

        return attrs


class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = '__all__'
        read_only_fields = ('created_at',)


class ReclamationSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    facture_details = serializers.SerializerMethodField()
    type_service_details = TypeServiceSerializer(source='type_service', read_only=True)

    expedition_codes = serializers.SerializerMethodField()
    expedition_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Reclamation
        fields = '__all__'

    def get_expedition_codes(self, obj):
        codes = []
        if obj.expedition_id and obj.expedition and obj.expedition.code_expedition:
            codes.append(obj.expedition.code_expedition)
        # M2M
        try:
            for exp in obj.expeditions.all():
                if exp and exp.code_expedition and exp.code_expedition not in codes:
                    codes.append(exp.code_expedition)
        except Exception:
            pass
        return codes

    def get_facture_details(self, obj):
        facture = getattr(obj, 'facture', None)
        if not facture:
            return None
        serializer_cls = globals().get('FactureSerializer')
        if serializer_cls is None:
            # Fallback minimal
            return {'id': facture.id, 'numero_facture': getattr(facture, 'numero_facture', None)}
        return serializer_cls(facture).data

    def validate(self, attrs):
        expedition = attrs.get('expedition') if 'expedition' in attrs else getattr(self.instance, 'expedition', None)
        expedition_ids = attrs.get('expedition_ids', None)
        facture = attrs.get('facture') if 'facture' in attrs else getattr(self.instance, 'facture', None)
        type_service = attrs.get('type_service') if 'type_service' in attrs else getattr(self.instance, 'type_service', None)

        has_colis = bool(expedition) or bool(expedition_ids and len(expedition_ids) > 0)
        if not (has_colis or facture or type_service):
            raise serializers.ValidationError(
                "Une réclamation doit être liée à au moins un colis (expédition), une facture ou un service."
            )

        return attrs

    def _sync_expeditions(self, reclamation: Reclamation, expedition_ids):
        if expedition_ids is None:
            return

        expedition_ids = [int(x) for x in expedition_ids]
        expedition_ids = list(dict.fromkeys(expedition_ids))  # dedupe keep order

        # Set "expedition" main link to first one (legacy column)
        if expedition_ids:
            reclamation.expedition_id = expedition_ids[0]
            reclamation.save(update_fields=['expedition_id'])

        # Ensure M2M links match list
        ReclamationExpedition.objects.filter(reclamation=reclamation).exclude(expedition_id__in=expedition_ids).delete()
        existing = set(ReclamationExpedition.objects.filter(reclamation=reclamation).values_list('expedition_id', flat=True))
        to_create = [ReclamationExpedition(reclamation=reclamation, expedition_id=eid) for eid in expedition_ids if eid not in existing]
        if to_create:
            ReclamationExpedition.objects.bulk_create(to_create)

        # If no ids provided, do not touch legacy expedition unless explicitly set to null by caller.

    def create(self, validated_data):
        expedition_ids = validated_data.pop('expedition_ids', None)
        reclamation = super().create(validated_data)

        # If legacy expedition is set but M2M empty, mirror it for "1 colis" cases
        if expedition_ids is None and reclamation.expedition_id:
            expedition_ids = [reclamation.expedition_id]

        self._sync_expeditions(reclamation, expedition_ids)
        return reclamation

    def update(self, instance, validated_data):
        expedition_ids = validated_data.pop('expedition_ids', None)

        statut_before = instance.statut
        instance = super().update(instance, validated_data)

        # Auto-set resolution date when moving to RESOLUE
        from django.utils import timezone
        if instance.statut == 'RESOLUE' and not instance.date_resolution:
            instance.date_resolution = timezone.now().date()
            instance.save(update_fields=['date_resolution'])
        if statut_before == 'RESOLUE' and instance.statut != 'RESOLUE':
            # keep date_resolution as history (do not clear)
            pass

        # Keep M2M in sync
        if expedition_ids is None and instance.expedition_id and instance.expeditions.count() == 0:
            expedition_ids = [instance.expedition_id]
        self._sync_expeditions(instance, expedition_ids)

        return instance


class ExpeditionSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    destination_details = DestinationSerializer(source='destination', read_only=True)
    type_service_details = TypeServiceSerializer(source='type_service', read_only=True)
    tracking_history = TrackingExpeditionSerializer(many=True, read_only=True)

    class Meta:
        model = Expedition
        fields = '__all__'
        read_only_fields = ('code_expedition', 'montant_total', 'date_creation', 'updated_at', 'created_by')

    def validate_statut(self, value):
        valid_statuses = [
            'Enregistré', 'Validé', 'En transit', 'En centre de tri', 
            'En cours de livraison', 'Livré', 'Échec de livraison'
        ]
        if value and value not in valid_statuses:
            raise serializers.ValidationError(f"Statut invalide. Les statuts possibles sont: {', '.join(valid_statuses)}")
        return value

    def update(self, instance, validated_data):
        # Bloquer la modification si l'expédition est déjà associée à une tournée
        # (Sauf si on est en train de modifier le statut uniquement, à voir selon les besoins)
        if instance.tournee and any(k not in ['statut'] for k in validated_data.keys()):
             raise serializers.ValidationError("Impossible de modifier une expédition déjà associée à une tournée.")
        
        # Recalculer le montant si les dimensions changent
        if 'poids_kg' in validated_data or 'volume_m3' in validated_data or 'destination' in validated_data or 'type_service' in validated_data:
             # Logique de calcul similaire au create
             pass # Pour l'instant on garde simple ou on extrait dans une méthode
             
        return super().update(instance, validated_data)

    def create(self, validated_data):
        # Génération du code expédition (EXP-YYYYMMDD-XXXX)
        import datetime
        from django.db.models import Max
        from django.db import transaction
        
        today_str = datetime.date.today().strftime('%Y%m%d')
        prefix = f"EXP-{today_str}"
        
        last_exp = Expedition.objects.filter(code_expedition__startswith=prefix).aggregate(Max('code_expedition'))
        last_code = last_exp['code_expedition__max']
        
        if last_code:
            seq = int(last_code.split('-')[-1]) + 1
        else:
            seq = 1
            
        validated_data['code_expedition'] = f"{prefix}-{seq:04d}"
        validated_data['statut'] = 'Enregistré'
        
        # Calcul du montant
        destination = validated_data.get('destination')
        type_service = validated_data.get('type_service')
        poids = validated_data.get('poids_kg')
        volume = validated_data.get('volume_m3')
        client = validated_data.get('client')
        
        # Recherche tarification en vigueur
        today = datetime.date.today()
        tarifs = Tarification.objects.filter(
            destination=destination,
            type_service=type_service,
            date_debut__lte=today
        ).filter(
            models.Q(date_fin__gte=today) | models.Q(date_fin__isnull=True)
        ).first()
        
        montant = 0
        if tarifs:
            montant = (
                (tarifs.tarif_base or 0) +
                (poids * (tarifs.tarif_poids_kg or 0)) +
                (volume * (tarifs.tarif_volume_m3 or 0))
            )
        elif destination:
            # Fallback sur tarif par défaut de la destination
            montant = destination.tarif_base_defaut
            
        validated_data['montant_total'] = round(montant, 2)
        
        request = self.context.get('request')
        if request and hasattr(request, 'user_obj'):
            validated_data['created_by'] = request.user_obj
            
        with transaction.atomic():
            expedition = super().create(validated_data)
            return expedition


class TourneeSerializer(serializers.ModelSerializer):
    chauffeur_details = ChauffeurSerializer(source='chauffeur', read_only=True)
    vehicule_details = VehiculeSerializer(source='vehicule', read_only=True)
    expeditions_count = serializers.SerializerMethodField()
    expeditions = ExpeditionSerializer(many=True, read_only=True)
    expedition_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Tournee
        fields = '__all__'
        read_only_fields = ('code_tournee', 'created_by', 'created_at')

    def get_expeditions_count(self, obj):
        return obj.expeditions.count()

    def validate(self, attrs):
        """
        Les données de trajet (km/durée/consommation) ne doivent être renseignées
        que lorsque la tournée est marquée 'Terminée'.
        """
        from rest_framework.exceptions import ValidationError
        from decimal import Decimal, InvalidOperation

        trip_fields = [
            'kilometrage_depart',
            'kilometrage_retour',
            'distance_km',
            'duree_minutes',
            'consommation_litres',
        ]

        # Statut cible (celui qui sera persisté)
        target_status = attrs.get('statut')
        if not target_status and self.instance is not None:
            target_status = getattr(self.instance, 'statut', None)
        if target_status is not None:
            import unicodedata
            raw = str(target_status).strip()

            # Tolérer les problèmes d'encodage historiques (ex: 'TerminÃ©e') et les remplacements '?' (ex: 'Termin?e').
            # Canonicaliser pour comparaison: enlever accents, normaliser casse.
            def _canon(x: str) -> str:
                x = x.replace('?', 'e')
                x = unicodedata.normalize('NFKD', x)
                x = ''.join(ch for ch in x if not unicodedata.combining(ch))
                return x.strip().lower()

            canon = _canon(raw)
            if canon == 'terminee':
                target_status = 'Terminée'
            elif canon == 'preparee':
                target_status = 'Préparée'
            elif canon == 'annulee':
                target_status = 'Annulée'
            else:
                target_status = raw
            # Si l'appelant envoie un statut, persister la version normalisée.
            if 'statut' in attrs:
                attrs['statut'] = target_status

        # Si on envoie une valeur non vide pour un champ trajet, bloquer hors "Terminée"
        provided_trip = False
        for f in trip_fields:
            if f in attrs:
                v = attrs.get(f)
                if v not in (None, ''):
                    provided_trip = True
                    break

        if provided_trip and target_status != 'Terminée':
            raise ValidationError("Les données du trajet ne peuvent être renseignées que lorsque la tournée est 'Terminée'.")

        def _resolved(field_name):
            # En PATCH, des champs requis peuvent déjà exister sur l'instance.
            if field_name in attrs:
                return attrs.get(field_name)
            if self.instance is not None:
                return getattr(self.instance, field_name, None)
            return None

        def _to_decimal(v, field_name):
            if v in (None, ''):
                return None
            try:
                return Decimal(str(v))
            except (InvalidOperation, ValueError):
                raise ValidationError({field_name: "Valeur numérique invalide."})

        # Si la tournée est (ou devient) "Terminée", exiger les données trajet + cohérence
        if target_status == 'Terminée':
            # distance_km est dérivée automatiquement de (kilometrage_retour - kilometrage_depart)
            required = ['kilometrage_depart', 'kilometrage_retour', 'consommation_litres']
            missing = [f for f in required if _resolved(f) in (None, '')]
            if missing:
                raise ValidationError({f: "Champ requis pour clôturer la tournée." for f in missing})

            km_depart = _to_decimal(_resolved('kilometrage_depart'), 'kilometrage_depart')
            km_retour = _to_decimal(_resolved('kilometrage_retour'), 'kilometrage_retour')
            consommation_litres = _to_decimal(_resolved('consommation_litres'), 'consommation_litres')
            duree_minutes = _resolved('duree_minutes')
            date_depart = _resolved('date_depart')
            date_retour = _resolved('date_retour')

            # Sanity: non-négatifs / positifs
            if km_depart is not None and km_depart < 0:
                raise ValidationError({'kilometrage_depart': "Le kilométrage ne peut pas être négatif."})
            if km_retour is not None and km_retour < 0:
                raise ValidationError({'kilometrage_retour': "Le kilométrage ne peut pas être négatif."})
            if consommation_litres is not None and consommation_litres < 0:
                raise ValidationError({'consommation_litres': "La consommation ne peut pas être négative."})

            # La durée est informative: seulement vérifier que ce n'est pas négatif.
            try:
                duree_minutes_int = int(duree_minutes) if duree_minutes not in (None, '') else None
            except (TypeError, ValueError):
                raise ValidationError({'duree_minutes': "Valeur numérique invalide."})

            if duree_minutes_int is not None and duree_minutes_int < 0:
                raise ValidationError({'duree_minutes': "La durée ne peut pas être négative."})

            if km_retour < km_depart:
                raise ValidationError({'kilometrage_retour': "Le kilométrage de retour doit être >= au kilométrage de départ."})

            km_diff = km_retour - km_depart
            if km_diff <= 0:
                raise ValidationError({'kilometrage_retour': "Le kilométrage de retour doit être strictement supérieur au kilométrage de départ."})

            # Toujours recalculer et persister la distance dérivée.
            attrs['distance_km'] = float(km_diff)
            distance_km = km_diff

            # Date depart/retour: coherence + accord avec duree_minutes (si dates presentes)
            if date_depart and date_retour:
                if date_retour <= date_depart:
                    raise ValidationError({'date_retour': "La date/heure de retour doit être après la date/heure de départ."})
                # La durée est informative: pas de contrainte de concordance avec les dates.

            # Consommation: uniquement contrainte non-négative (aucune cohérence imposée).

        return attrs

    def _finalize_expeditions(self, tournee, expedition_ids):
        if expedition_ids is None:
            return

        Expedition.objects.filter(tournee=tournee).exclude(id__in=expedition_ids).update(tournee=None, statut='Enregistré')
        Expedition.objects.filter(id__in=expedition_ids).update(tournee=tournee, statut='Validé')

    def _handle_tournee_completion(self, tournee):
        from django.utils import timezone
        delivered = tournee.expeditions.exclude(statut='Livré').select_related('client', 'tournee')
        now = timezone.now()
        for exp in delivered:
            exp.statut = 'Livré'
            exp.save(update_fields=['statut'])
            TrackingExpedition.objects.create(
                expedition=exp,
                tournee=tournee,
                chauffeur=tournee.chauffeur,
                statut='Livré',
                lieu=f'Tournée {tournee.code_tournee}',
                commentaire='Tournée terminée, expédition livrée',
                date_statut=now
            )

    def create(self, validated_data):
        import datetime
        from django.db.models import Max
        from django.db import transaction

        expedition_ids = validated_data.pop('expedition_ids', [])

        today_str = datetime.date.today().strftime('%Y%m%d')
        prefix = f"TRN-{today_str}"

        last_item = Tournee.objects.filter(code_tournee__startswith=prefix).aggregate(Max('code_tournee'))
        last_code = last_item['code_tournee__max']

        seq = int(last_code.split('-')[-1]) + 1 if last_code else 1
        validated_data['code_tournee'] = f"{prefix}-{seq:04d}"
        validated_data.setdefault('statut', 'Préparée')

        request = self.context.get('request')
        if request and hasattr(request, 'user_obj'):
            validated_data['created_by'] = request.user_obj

        with transaction.atomic():
            tournee = super().create(validated_data)
            self._finalize_expeditions(tournee, expedition_ids)

            if tournee.statut == 'Terminée':
                self._handle_tournee_completion(tournee)

            return tournee

    def update(self, instance, validated_data):
        from django.db import transaction
        expedition_ids = validated_data.pop('expedition_ids', None)

        previous_status = instance.statut
        with transaction.atomic():
            tournee = super().update(instance, validated_data)
            self._finalize_expeditions(tournee, expedition_ids)

            if tournee.statut == 'Terminée' and previous_status != 'Terminée':
                self._handle_tournee_completion(tournee)

            return tournee


class FactureExpeditionSerializer(serializers.ModelSerializer):
    expedition_details = ExpeditionSerializer(source='expedition', read_only=True)
    
    class Meta:
        model = FactureExpedition
        fields = '__all__'


class FactureSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    expeditions = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    expedition_details = serializers.SerializerMethodField()
    paiements = serializers.SerializerMethodField()
    reste_a_payer = serializers.SerializerMethodField()

    class Meta:
        model = Facture
        fields = '__all__'
        read_only_fields = ('numero_facture', 'total_ht', 'total_ttc', 'montant_tva', 'updated_at')

    def get_expedition_details(self, obj):
        links = FactureExpedition.objects.filter(facture=obj)
        return ExpeditionSerializer([l.expedition for l in links], many=True).data

    def get_paiements(self, obj):
        paiements = Paiement.objects.filter(facture=obj)
        return PaiementSerializer(paiements, many=True).data

    def get_reste_a_payer(self, obj):
        deja_paye = Paiement.objects.filter(facture=obj).aggregate(models.Sum('montant'))['montant__sum'] or 0
        total_ttc = obj.total_ttc or 0
        return round(total_ttc - deja_paye, 2)

    def create(self, validated_data):
        import datetime
        from django.db.models import Max
        from django.db import transaction

        expedition_ids = validated_data.pop('expeditions', [])
        client = validated_data.get('client')

        with transaction.atomic():
            # 1. Génération numéro facture (FAC-YYYY-XXXX)
            year = datetime.date.today().year
            prefix = f"FAC-{year}"
            last_fac = Facture.objects.filter(numero_facture__startswith=prefix).aggregate(Max('numero_facture'))
            last_code = last_fac['numero_facture__max']
            seq = int(last_code.split('-')[-1]) + 1 if last_code else 1
            validated_data['numero_facture'] = f"{prefix}-{seq:04d}"
            validated_data['date_facture'] = datetime.date.today()
            validated_data['statut'] = 'Émise'

            # 2. Calcul des montants
            expeditions = Expedition.objects.filter(id__in=expedition_ids)
            total_ht = sum((e.montant_total or 0) for e in expeditions)
            tva_rate = 0.20 # 20% TVA par défaut
            montant_tva = total_ht * tva_rate
            total_ttc = total_ht + montant_tva

            validated_data['total_ht'] = round(total_ht, 2)
            validated_data['montant_tva'] = round(montant_tva, 2)
            validated_data['total_ttc'] = round(total_ttc, 2)

            facture = Facture.objects.create(**validated_data)

            # 3. Lier les expéditions
            for exp in expeditions:
                FactureExpedition.objects.create(facture=facture, expedition=exp)
                exp.est_facturee = True
                # La base peut avoir un trigger (trg_expedition_mark_facturee) qui met Ã  jour est_facturee.
                # Ã‰viter un UPDATE supplÃ©mentaire qui peut provoquer des conflits avec les triggers.

            # 4. Impact sur le solde client (Dette augmente)
            if client:
                client.solde += total_ttc
                client.save()

            return facture


class PaiementSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    facture = serializers.PrimaryKeyRelatedField(queryset=Facture.objects.all())
    facture_numero = serializers.CharField(source='facture.numero_facture', read_only=True)

    class Meta:
        model = Paiement
        fields = [
            'id', 'facture', 'facture_numero', 'client', 'client_details',
            'date_paiement', 'mode_paiement', 'montant', 'statut', 'updated_at'
        ]
        read_only_fields = ('id', 'client', 'client_details', 'updated_at')

    def create(self, validated_data):
        from django.db import transaction
        facture = validated_data['facture']
        montant = validated_data.get('montant', 0)

        with transaction.atomic():
            client = facture.client
            validated_data['client'] = client
            paiement = Paiement.objects.create(**validated_data)

            if client:
                client.solde = (client.solde or 0) - montant
                client.save(update_fields=['solde'])

            deja_paye = Paiement.objects.filter(facture=facture).aggregate(models.Sum('montant'))['montant__sum'] or 0
            total_ttc = facture.total_ttc or 0
            if deja_paye >= total_ttc:
                facture.statut = 'Payée'
            elif deja_paye > 0:
                facture.statut = 'Partiellement Payée'
            facture.save(update_fields=['statut'])

            return paiement
