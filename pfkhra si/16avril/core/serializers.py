from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from .models import (
    Utilisateur, Role, AuditLog,
    Client, Chauffeur, Vehicule, Destination, TypeService, Tarification,
    Expedition, TrackingExpedition, Tournee, Facture, FactureExpedition, Paiement
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
            montant = tarifs.tarif_base + (poids * tarifs.tarif_poids_kg) + (volume * tarifs.tarif_volume_m3)
        elif destination:
            # Fallback sur tarif par défaut de la destination
            montant = destination.tarif_base_defaut
            
        validated_data['montant_total'] = round(montant, 2)
        
        request = self.context.get('request')
        if request and hasattr(request, 'user_obj'):
            validated_data['created_by'] = request.user_obj
            
        with transaction.atomic():
            # 1. Créer l'expédition
            print("DEBUG: Creating expedition...")
            expedition = super().create(validated_data)
            print(f"DEBUG: Expedition created. ID={expedition.id}, est_facturee={expedition.est_facturee}")
            
            # 2. Générer automatiquement une facture
            year = datetime.date.today().year
            fac_prefix = f"FAC-{year}"
            last_fac = Facture.objects.filter(numero_facture__startswith=fac_prefix).aggregate(Max('numero_facture'))
            last_fac_code = last_fac['numero_facture__max']
            fac_seq = int(last_fac_code.split('-')[-1]) + 1 if last_fac_code else 1
            
            total_ht = round(expedition.montant_total, 2)
            tva_rate = 0.20
            montant_tva = round(total_ht * tva_rate, 2)
            total_ttc = round(total_ht + montant_tva, 2)
            
            print("DEBUG: Creating facture...")
            facture = Facture.objects.create(
                numero_facture=f"{fac_prefix}-{fac_seq:04d}",
                client=client,
                date_facture=datetime.date.today(),
                total_ht=total_ht,
                montant_tva=montant_tva,
                total_ttc=total_ttc,
                statut='Émise'
            )
            print(f"DEBUG: Facture created. ID={facture.id}")
            
            # 3. Lier l'expédition
            print("DEBUG: Linking facture and expedition...")
            FactureExpedition.objects.create(facture=facture, expedition=expedition)
            print("DEBUG: Link created.")
            
            # Le trigger mets déjà à jour le statut en base
            expedition.est_facturee = True
            
            # 4. Mettre à jour le solde client
            if client:
                client.solde += total_ttc
                client.save()
            
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

    def create(self, validated_data):
        import datetime
        from django.db.models import Max
        from django.db import transaction
        
        expedition_ids = validated_data.pop('expedition_ids', [])
        
        today_str = datetime.date.today().strftime('%Y%m%d')
        prefix = f"TRN-{today_str}"
        
        last_item = Tournee.objects.filter(code_tournee__startswith=prefix).aggregate(Max('code_tournee'))
        last_code = last_item['code_tournee__max']
        
        if last_code:
            seq = int(last_code.split('-')[-1]) + 1
        else:
            seq = 1
            
        validated_data['code_tournee'] = f"{prefix}-{seq:04d}"
        if 'statut' not in validated_data:
            validated_data['statut'] = 'Préparée'
        
        request = self.context.get('request')
        if request and hasattr(request, 'user_obj'):
            validated_data['created_by'] = request.user_obj
            
        with transaction.atomic():
            tournee = super().create(validated_data)
            
            # Lier les expéditions
            if expedition_ids:
                Expedition.objects.filter(id__in=expedition_ids).update(tournee=tournee, statut='Validé')
            
            return tournee

    def update(self, instance, validated_data):
        from django.db import transaction
        expedition_ids = validated_data.pop('expedition_ids', None)
        
        with transaction.atomic():
            # Avant la mise à jour, on identifie les expéditions qui vont être retirées
            if expedition_ids is not None:
                # Celles qui étaient liées mais ne le sont plus
                instance.expeditions.exclude(id__in=expedition_ids).update(tournee=None, statut='Enregistré')
                # Celles qui ne l'étaient pas mais vont l'être
                Expedition.objects.filter(id__in=expedition_ids).update(tournee=instance, statut='Validé')
            
            return super().update(instance, validated_data)


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
        return round(obj.total_ttc - deja_paye, 2)

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
            total_ht = sum(e.montant_total for e in expeditions)
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
                exp.save()

            # 4. Impact sur le solde client (Dette augmente)
            if client:
                client.solde += total_ttc
                client.save()

            return facture


class PaiementSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    facture_numero = serializers.CharField(source='facture.numero_facture', read_only=True)

    class Meta:
        model = Paiement
        fields = '__all__'
        read_only_fields = ('updated_at',)

    def create(self, validated_data):
        from django.db import transaction
        client = validated_data.get('client')
        facture = validated_data.get('facture')
        montant = validated_data.get('montant', 0)

        with transaction.atomic():
            if facture and not client:
                client = facture.client
                validated_data['client'] = client

            paiement = Paiement.objects.create(**validated_data)

            # Impact sur le solde client (Dette diminue)
            if client:
                client.solde -= montant
                client.save()

            # Maj statut facture
            if facture:
                deja_paye = Paiement.objects.filter(facture=facture).aggregate(models.Sum('montant'))['montant__sum'] or 0
                if deja_paye >= facture.total_ttc:
                    facture.statut = 'Payée'
                elif deja_paye > 0:
                    facture.statut = 'Partiellement Payée'
                facture.save()

            return paiement
