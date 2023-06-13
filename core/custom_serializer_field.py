from rest_framework import serializers
from .models import Caisse, FicheVenteClient, Depot, FicheAchatCommandeFournisseur, Produit, SellingPoint, Client


class SellingPointCustomRelationQueryset(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = SellingPoint.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(vendeur=request.user.vendeur)
        return queryset


class ProduitCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Produit.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset


class CaisseCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Caisse.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset


class ClientCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Client.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset


class DepotCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Depot.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset


class AchatCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = FicheAchatCommandeFournisseur.objects.filter(type_fiche=1)
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset


class AchatCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = FicheAchatCommandeFournisseur.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset


class VenteCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = FicheVenteClient.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset


class ClientCustomRelationField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Client.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=request.user.vendeur.selling_point)
        return queryset

# class CaisseSerializer(serializers.Serializer):
#     selling_point = serializers.CharField()
#     nom = serializers.CharField(max_length=200)
#     caisse = serializers.CharField(max_length=200)
#     wilaya = serializers.CharField(max_length=200)
#     ville = serializers.CharField(max_length=200)
#     solde = serializers.IntegerField()


#     def create(self, validated_data):
#         selling_point = SellingPoint.objects.get(id=int(validated_data["selling_point"]))
#         nom = validated_data["nom"]
#         caisse = validated_data["caisse"]
#         wilaya = validated_data["wilaya"]
#         ville = validated_data["ville"]
#         solde = validated_data["solde"]
#         return Caisse.objects.create(selling_point=selling_point, nom=nom, caisse=caisse,
#         wilaya=wilaya, ville=ville, solde=solde)

#     def update(self, instance, validated_data):
#         instance.nom = validated_data.get('nom', instance.nom)
#         instance.caisse = validated_data.get('caisse', instance.caisse)
#         instance.wilaya = validated_data.get('wilaya', instance.wilaya)
#         instance.ville = validated_data.get('ville', instance.ville)
#         instance.solde = validated_data.get('solde', instance.solde)

#         instance.save()
#         return instance
