from email.policy import default
from rest_framework import serializers
from users.models import CustomUser
from core.models import Vendeur
from core.models import SellingPoint
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from core.serializers import VendeurSerializer


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission

        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    # user_type_data = (('1',"Directeur"),('2',"Vendeur"),('3',"Autre"))
    # user_type = serializers.ChoiceField(default='2',choices=user_type_data)

    permissions_data = (
        ("Can add avaries", "Can add avaries"),
        ("Can delete avaries", "Can delete avaries"),
        ("Can change avaries", "Can change avaries"),
        ("Can view avaries", "Can view avaries"),
        ("Can add caisse", "Can add caisse"),
        ("Can delete caisse", "Can delete caisse"),
        ("Can change caisse", "Can change caisse"),
        ("Can view caisse", "Can view caisse"),
        ("Can add client", "Can add client"),
        ("Can delete client", "Can delete client"),
        ("Can change client", "Can change client"),
        ("Can view client", "Can view client"),
        ("Can add depot", "Can add depot"),
        ("Can delete depot", "Can delete depot"),
        ("Can change depot", "Can change depot"),
        ("Can view depot", "Can view depot"),
        ("Can add famille produit", "Can add famille produit"),
        ("Can delete famille produit", "Can delete famille produit"),
        ("Can change famille produit", "Can change famille produit"),
        ("Can view famille produit", "Can view famille produit"),
        (
            "Can add fiche achat commande fournisseur",
            "Can add fiche achat commande fournisseur",
        ),
        (
            "Can delete fiche achat commande fournisseur",
            "Can delete fiche achat commande fournisseur",
        ),
        (
            "Can change fiche achat commande fournisseur",
            "Can change fiche achat commande fournisseur",
        ),
        (
            "Can view fiche achat commande fournisseur",
            "Can view fiche achat commande fournisseur",
        ),
        ("Can add fiche credit", "Can add fiche credit"),
        ("Can delete fiche credit", "Can delete fiche credit"),
        ("Can change fiche credit", "Can change fiche credit"),
        ("Can view fiche credit", "Can view fiche credit"),
        ("Can add fiche debit", "Can add fiche debit"),
        ("Can delete fiche debit", "Can delete fiche debit"),
        ("Can change fiche debit", "Can change fiche debit"),
        ("Can view fiche debit", "Can view fiche debit"),
        ("Can add fiche vente client", "Can add fiche vente client"),
        ("Can delete fiche vente client", "Can delete fiche vente client"),
        ("Can change fiche vente client", "Can change fiche vente client"),
        ("Can view fiche vente client", "Can view fiche vente client"),
        ("Can add fournisseur", "Can add fournisseur"),
        ("Can delete fournisseur", "Can delete fournisseur"),
        ("Can change fournisseur", "Can change fournisseur"),
        ("Can view fournisseur", "Can view fournisseur"),
        ("Can add frais generales", "Can add frais generales"),
        ("Can delete frais generales", "Can delete frais generales"),
        ("Can change frais generales", "Can change frais generales"),
        ("Can view frais generales", "Can view frais generales"),
        ("Can add marque produit", "Can add marque produit"),
        ("Can delete marque produit", "Can delete marque produit"),
        ("Can change marque produit", "Can change marque produit"),
        ("Can view marque produit", "Can view marque produit"),
        ("Can add payement client", "Can add payement client"),
        ("Can delete payement client", "Can delete payement client"),
        ("Can change payement client", "Can change payement client"),
        ("Can view payement client", "Can view payement client"),
        ("Can add payement fournisseur", "Can add payement fournisseur"),
        ("Can delete payement fournisseur", "Can delete payement fournisseur"),
        ("Can change payement fournisseur", "Can change payement fournisseur"),
        ("Can view payement fournisseur", "Can view payement fournisseur"),
        ("Can add produit", "Can add produit"),
        ("Can delete produit", "Can delete produit"),
        ("Can change produit", "Can change produit"),
        ("Can view produit", "Can view produit"),
        (
            "Can add produit achat commande fournisseur",
            "Can add produit achat commande fournisseur",
        ),
        (
            "Can delete produit achat commande fournisseur",
            "Can delete produit achat commande fournisseur",
        ),
        (
            "Can change produit achat commande fournisseur",
            "Can change produit achat commande fournisseur",
        ),
        (
            "Can view produit achat commande fournisseur",
            "Can view produit achat commande fournisseur",
        ),
        ("Can add produits retour fournisseur", "Can add produits retour fournisseur"),
        (
            "Can delete produits retour fournisseur",
            "Can delete produits retour fournisseur",
        ),
        (
            "Can change produits retour fournisseur ",
            "Can change produits retour fournisseur",
        ),
        (
            "Can view produits retour fournisseur",
            "Can view produits retour fournisseur",
        ),
        ("Can add produit vente client", "Can add produit vente client"),
        ("Can delete produit vente client", "Can delete produit vente client"),
        ("Can change produit vente client", "Can change produit vente client"),
        ("Can view produit vente client", "Can view produit vente client"),
        ("Can add retours client", "Can add retours client"),
        ("Can delete retours client", "Can delete retours client"),
        ("Can change retours client", "Can change retours client"),
        ("Can view retours client", "Can view retours client"),
        ("Can add retours fournisseur", "Can add retours fournisseur"),
        ("Can delete retours fournisseur", "Can delete retours fournisseur"),
        ("Can change retours fournisseur", "Can change retours fournisseur"),
        ("Can view retours fournisseur", "Can view retours fournisseur"),
        ("Can add selling point", "Can add selling point"),
        ("Can delete selling point", "Can delete selling point"),
        ("Can change selling point", "Can change selling point"),
        ("Can view selling point", "Can view selling point"),
        ("Can add vendeur", "Can add vendeur"),
        ("Can delete vendeur", "Can delete vendeur"),
        ("Can change vendeur", "Can change vendeur"),
        ("Can view vendeur", "Can view vendeur"),
    )

    permissions = serializers.MultipleChoiceField(
        choices=permissions_data, write_only=True, default=[]
    )
    user_permissions = PermissionSerializer(read_only=True, many=True)
    # user_permissions = serializers.SerializerMethodField()
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    # password2 = serializers.CharField(write_only=True, required=True)
    vendeur = VendeurSerializer()
    user_selling_point = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "user_permissions",
            "password",
            "vendeur",
            "permissions",
            "is_staff",
            "is_superuser",
            "user_selling_point",
        ]
        # extra_kwargs = {
        #     'permissions': {'write_only': True}
        #     }
        read_only_fields = [
            "user_permissions",
            "user_selling_point",
            "vendeur",
        ]

    def get_user_selling_point(self, obj):
        if obj.is_superuser == False:
            sp_id = obj.vendeur.selling_point.id
            user_sp = SellingPoint.objects.get(id=sp_id)
            return sp_id
        return

        # prod_fiches = obj.produits.all()
        # montant = 0
        # for prod in prod_fiches:
        #     prix_retour_prod = prod.quantite_retour * prod.produit.prix_U_achat
        #     montant += prix_retour_prod
        # return montant

    def create(self, validated_data):
        vendeur_data = validated_data.pop("vendeur")
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_staff=validated_data["is_staff"],
            is_superuser=validated_data["is_superuser"],
        )
        # user.set_password(validated_data['password'])
        # user.user_permissions.set(validated_data['permissions'])
        user.save()

        if validated_data["permissions"]:
            permissions = validated_data["permissions"]
            perm_list = []
            for perm in permissions:
                try:
                    permission = Permission.objects.get(name=perm)
                except Permission.DoesNotExist:
                    raise serializers.ValidationError(
                        {"permission": "permission does not exist"}
                    )
                perm_list.append(permission)
            user.user_permissions.set(perm_list)
        Vendeur.objects.create(admin=user, **vendeur_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_superuser = validated_data.get(
            "is_superuser", instance.is_superuser
        )

        permissions = validated_data["permissions"]
        perm_list = []
        for perm in permissions:
            try:
                permission = Permission.objects.get(name=perm)
            except Permission.DoesNotExist:
                raise serializers.ValidationError(
                    {"permission": "permission does not exist"}
                )
            perm_list.append(permission)
        instance.user_permissions.set(perm_list)

        return instance

    # def get_user_permissions(self, obj):
    #     obj.user_permissions.all()
    #     return


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
