from . import serializers
from rest_framework import generics
from . import models
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.response import Response
from rest_framework import status, pagination
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .custom_permissions import IsSPUser
from .models import ProduitVenteClient
from .models import Produit
from rest_framework.views import APIView

# ----------------------------------------------SELLING POINT----------------------------------------------------------


class SellingPoitGetPost(generics.ListCreateAPIView):
    queryset = models.SellingPoint.objects.all()
    serializer_class = serializers.SellingPointSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.SellingPoint.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(vendeur=self.request.user.vendeur)
        return queryset

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        # if not request.user.is_superuser:
        #     queryset = queryset.filter(vendeur=request.user.vendeur)
        serializer = serializers.SellingPointSerializer(queryset, many=True)
        return Response(serializer.data)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def get_serializer_context(self):
    #     """
    #     Extra context provided to the serializer class.
    #     """
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }

    def post(self, request):
        serializer = serializers.SellingPointSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SellingPoitPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SellingPoint.objects.all()
    serializer_class = serializers.SellingPointSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.SellingPoint.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(vendeur=self.request.user.vendeur)
        return queryset

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        # if not request.user.is_superuser:
        #     queryset = queryset.filter(vendeur=request.user.vendeur)
        serializer = serializers.SellingPointSerializer(queryset)
        return Response(serializer.data)


class CaisseGetPost(generics.ListCreateAPIView):
    queryset = models.Caisse.objects.all()
    serializer_class = serializers.CaisseSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.Caisse.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.CaisseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CaisseSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CaissePk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Caisse.objects.all()
    serializer_class = serializers.CaisseSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Caisse.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


# class StandardResultsSetPagination(pagination.PageNumberPagination):
#     page_size = 1
#     page_size_query_param = 'page_size'
#     max_page_size = 1000


class ProduitGetPost(generics.ListCreateAPIView):
    queryset = models.Produit.objects.all()
    serializer_class = serializers.ProduitSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["famille", "marque"]

    def get_queryset(self):
        sp = self.request.query_params.get("selling_point")
        queryset = models.Produit.objects.filter(selling_point=sp)
        if not sp:
            queryset = models.Produit.objects.all()
        if not self.request.user.is_superuser:
            queryset = models.Produit.objects.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.ProduitSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ProduitSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProduitPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Produit.objects.all()
    serializer_class = serializers.ProduitSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Produit.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class MarqueProduitGetPost(generics.ListCreateAPIView):
    queryset = models.MarqueProduit.objects.all()
    serializer_class = serializers.MarqueProduitSerializer
    # permission_classes = [IsAuthenticated]


class MarqueProduitPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MarqueProduit.objects.all()
    serializer_class = serializers.MarqueProduitSerializer
    permission_classes = [
        # IsAuthenticated,
        # DjangoModelPermissionsOrAnonReadOnly,
        # IsSPUser,
    ]


class FamilleProduitGetPost(generics.ListCreateAPIView):
    queryset = models.FamilleProduit.objects.all()
    serializer_class = serializers.FamilleProduitSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]


class FamilleProduitPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FamilleProduit.objects.all()
    serializer_class = serializers.FamilleProduitSerializer
    # permission_classes = [
    #     IsAuthenticated,
    #     DjangoModelPermissionsOrAnonReadOnly,
    #     IsSPUser,
    # ]


class AvariesGetPost(generics.ListCreateAPIView):
    queryset = models.Avaries.objects.all()
    serializer_class = serializers.AvariesSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["produit", "depot"]

    def get_queryset(self):
        # date1 = self.request.query_params.get("date1")
        # if not date1:
        #     if models.Vendeur.objects.all().first():
        #         date1 = models.Vendeur.objects.all().first().date
        #     else:
        #         date1 = datetime.today().strftime("%Y-%m-%d")
        # date2 = self.request.query_params.get("date2")
        # if not date2:
        #     date2 = datetime.today().strftime("%Y-%m-%d")

        # sp = self.request.query_params.get("selling_point")
        queryset = models.Avaries.objects.all(
            # selling_point=sp, date__range=[date1, date2]
        )
        if not self.request.user.is_superuser:
            queryset = models.Avaries.objects.filter(
                selling_point=self.request.user.vendeur.selling_point,
                # date__range=[date1, date2],
            )
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.AvariesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AvariesSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            proddepot = models.ProduitDepot.objects.get(
                produit=serializer.instance.produit, depot=serializer.instance.depot
            )
            proddepot.quantite -= serializer.instance.qtte
            serializer.instance.produit.qtte_avarie += serializer.instance.qtte
            serializer.instance.produit.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class AvariesPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Avaries.objects.all()
    serializer_class = serializers.AvariesSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Avaries.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class DepotGetPost(generics.ListCreateAPIView):
    queryset = models.Depot.objects.all()
    serializer_class = serializers.DepotSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.Depot.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.DepotSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CaisseSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DepotPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Depot.objects.all()
    serializer_class = serializers.DepotSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Depot.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class ProduitDepotPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProduitDepot.objects.all()
    serializer_class = serializers.ProduitDepotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.ProduitDepot.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class FicheCreditGetPost(generics.ListCreateAPIView):
    queryset = models.FicheCredit.objects.all()
    serializer_class = serializers.FicheCreditSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["reglement", "caisse"]

    def get_queryset(self):
        date1 = self.request.query_params.get("date1")
        if not date1:
            if models.FicheCredit.objects.all().first():
                date1 = models.FicheCredit.objects.all().first().date
            else:
                date1 = datetime.today().strftime("%Y-%m-%d")
        date2 = self.request.query_params.get("date2")
        if not date2:
            date2 = datetime.today().strftime("%Y-%m-%d")

        sp = self.request.query_params.get("selling_point")
        queryset = models.FicheCredit.objects.filter(
            selling_point=sp, date__range=[date1, date2]
        )
        if not self.request.user.is_superuser:
            queryset = models.FicheCredit.objects.filter(
                selling_point=self.request.user.vendeur.selling_point,
                date__range=[date1, date2],
            )
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.FicheCreditSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.FicheCreditSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            fiche = serializer.instance
            caisse = fiche.caisse
            caisse.montant_credit += fiche.total
            caisse.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class FicheCreditPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FicheCredit.objects.all()
    serializer_class = serializers.FicheCreditSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.FicheCredit.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance = self.get_object()

        # Access the original instance information before modifications
        original_instance_data = serializers.FicheCreditSerializer(instance).data
        original_montant = original_instance_data.get("total")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modifie_par=request.user)
            # serializer.instance.reste_a_payer = (
            #     serializer.instance.total - serializer.instance.montant_reg_client
            # )
            # serializer.instance.save()

            caisse = serializer.instance.caisse
            caisse.montant_credit += original_montant - serializer.instance.total
            caisse.save()
            # serializer.save(saisie_par=request.user)
            serializer.instance.save()

        return Response(serializer.data)


class FicheDebitGetPost(generics.ListCreateAPIView):
    queryset = models.FicheDebit.objects.all()
    serializer_class = serializers.FicheDebitSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["reglement", "caisse"]

    def get_queryset(self):
        date1 = self.request.query_params.get("date1")
        if not date1:
            if models.FicheDebit.objects.all().first():
                date1 = models.FicheDebit.objects.all().first().date
            else:
                date1 = datetime.today().strftime("%Y-%m-%d")
        date2 = self.request.query_params.get("date2")
        if not date2:
            date2 = datetime.today().strftime("%Y-%m-%d")

        sp = self.request.query_params.get("selling_point")

        queryset = models.FicheDebit.objects.filter(
            selling_point=sp, date__range=[date1, date2]
        )
        if not self.request.user.is_superuser:
            queryset = models.FicheDebit.objects.filter(
                selling_point=self.request.user.vendeur.selling_point,
                date__range=[date1, date2],
            )
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.FicheDebitSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.FicheDebitSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            fiche = serializer.instance
            fiche = serializer.instance
            caisse = fiche.caisse
            caisse.montant_debit += fiche.total
            caisse.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class FicheDebitPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FicheDebit.objects.all()
    serializer_class = serializers.FicheDebitSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.FicheDebit.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance = self.get_object()

        # Access the original instance information before modifications
        original_instance_data = serializers.FicheDebitSerializer(instance).data
        original_montant = original_instance_data.get("total")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modifie_par=request.user)
            # serializer.instance.reste_a_payer = (
            #     serializer.instance.total - serializer.instance.montant_reg_client
            # )
            # serializer.instance.save()

            caisse = serializer.instance.caisse
            caisse.montant_debit += original_montant - serializer.instance.total
            caisse.save()
            # serializer.save(saisie_par=request.user)
            serializer.instance.save()

        return Response(serializer.data)


class VendeurGetPost(generics.ListCreateAPIView):
    queryset = models.Vendeur.objects.all()
    serializer_class = serializers.VendeurSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        sp = self.request.query_params.get("selling_point")
        queryset = models.Vendeur.objects.filter(selling_point=sp)
        if not sp:
            queryset = models.Vendeur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.VendeurSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.VendeurSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class VendeurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendeur.objects.all()
    serializer_class = serializers.VendeurSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = models.Vendeur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class TypeFgGetPost(generics.ListCreateAPIView):
    queryset = models.TypeFG.objects.all()
    serializer_class = serializers.TypeFGSerializer


class FraisGeneralesGetPost(generics.ListCreateAPIView):
    queryset = models.FraisGenerales.objects.all()
    serializer_class = serializers.FraisGeneralesSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["reglement", "caisse", "type"]

    def get_queryset(self):
        # date1 = self.request.query_params.get("date1")
        # if not date1:
        #     if models.FraisGenerales.objects.all().first():
        #         date1 = models.FraisGenerales.objects.all().first().date
        #     else:
        #         date1 = datetime.today().strftime("%Y-%m-%d")
        # date2 = self.request.query_params.get("date2")
        # if not date2:
        #     date2 = datetime.today().strftime("%Y-%m-%d")

        # sp = self.request.query_params.get("selling_point")
        queryset = models.FraisGenerales.objects.all(
            # selling_point=sp, date__range=[date1, date2]
        )
        if not self.request.user.is_superuser:
            queryset = models.FraisGenerales.objects.filter(
                selling_point=self.request.user.vendeur.selling_point,
                # date__range=[date1, date2],
            )
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.FraisGeneralesSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.FraisGeneralesSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            frais = serializer.instance
            caisse = frais.caisse
            caisse.montant_frais_generales += frais.montant
            caisse.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FraisGeneralesPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FraisGenerales.objects.all()
    serializer_class = serializers.FraisGeneralesSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.FraisGenerales.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance = self.get_object()

        # Access the original instance information before modifications
        original_instance_data = serializers.FraisGeneralesSerializer(instance).data
        original_montant = original_instance_data.get("montant")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modifie_par=request.user)
            # serializer.instance.reste_a_payer = (
            #     serializer.instance.total - serializer.instance.montant_reg_client
            # )
            # serializer.instance.save()

            caisse = serializer.instance.caisse
            caisse.montant_frais_generales += (
                original_montant - serializer.instance.montant
            )
            caisse.save()
            # serializer.save(saisie_par=request.user)
            serializer.instance.save()

        return Response(serializer.data)


# -----------------------------------------------FOURNISSEUR------------------------------------------------


class FournisseurGetPost(generics.ListCreateAPIView):
    queryset = models.Fournisseur.objects.all()
    serializer_class = serializers.FournisseurSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.Fournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.FournisseurSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.FournisseurSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FournisseurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Fournisseur.objects.all()
    serializer_class = serializers.FournisseurSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Fournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class FicheACFournisseurGetPost(generics.ListAPIView):
    queryset = models.FicheAchatCommandeFournisseur.objects.all()
    serializer_class = serializers.FicheACFournisseurSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fournisseur", "action", "mode_reglement"]

    def get_queryset(self):
        # date1 = self.request.query_params.get("date1")
        # if not date1:
        #     date1 = (
        #         models.FicheAchatCommandeFournisseur.objects.filter(type_fiche="Achat")
        #         .first()
        #         .date
        #     )
        # date2 = self.request.query_params.get("date2")
        # if not date2:
        #     date2 = datetime.today().strftime("%Y-%m-%d")

        sp = self.request.query_params.get("selling_point")

        queryset = models.FicheAchatCommandeFournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = models.FicheAchatCommandeFournisseur.objects.filter(
                selling_point=self.request.user.vendeur.selling_point,
                # type_fiche="Achat",
                # date__range=[date1, date2],
            )
        return queryset


class FicheACFournisseurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FicheAchatCommandeFournisseur.objects.all()
    serializer_class = serializers.FicheACFournisseurSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.FicheAchatCommandeFournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.FicheACFournisseurSerializer(queryset, many=True)
        return Response(serializer.data)


class FicheAchatFournisseurGetPost(generics.ListCreateAPIView):
    queryset = models.FicheAchatCommandeFournisseur.objects.filter(type_fiche="Achat")
    serializer_class = serializers.FicheACFournisseurSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fournisseur", "action", "mode_reglement"]

    def get_queryset(self):
        # date1 = self.request.query_params.get("date1")
        # if not date1:
        #     date1 = (
        #         models.FicheAchatCommandeFournisseur.objects.filter(type_fiche="Achat")
        #         .first()
        #         .date
        #     )
        # date2 = self.request.query_params.get("date2")
        # if not date2:
        #     date2 = datetime.today().strftime("%Y-%m-%d")

        sp = self.request.query_params.get("selling_point")

        queryset = models.FicheAchatCommandeFournisseur.objects.filter(
            type_fiche="Achat"
            # , date__range=[date1, date2]
            ,
            # selling_point=sp,
        )
        if not self.request.user.is_superuser:
            queryset = models.FicheAchatCommandeFournisseur.objects.filter(
                selling_point=self.request.user.vendeur.selling_point,
                type_fiche="Achat",
                # date__range=[date1, date2],
            )
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.FicheACFournisseurSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.FicheACFournisseurSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user, type_fiche="Achat")
            for prod in serializer.instance.produits.all():
                prod.produit.qtte_achete += prod.quantite
                prod.produit.save()
                deptProd, created = models.ProduitDepot.objects.get_or_create(
                    produit=prod.produit,
                    depot=prod.depot,
                    selling_point=prod.depot.selling_point,
                )
                if created:
                    # Object was just created, perform actions for newly created objects
                    # For example, you can send a success message
                    deptProd.quantite = prod.quantite
                    deptProd.total_prix = prod.produit.prix_detail * deptProd.quantite
                    deptProd.prix_detail_produit = prod.produit.prix_detail
                    deptProd.prix_gros_produit = prod.produit.prix_vente_gros
                    deptProd.prix_autre_produit = prod.produit.prix_vente_autre
                    deptProd.produit_reference = prod.produit.reference
                    deptProd.produit_article = prod.produit.article
                    deptProd.produit_unite = prod.produit.unit
                    deptProd.save()
                else:
                    # Object already exists, augment its quantity
                    deptProd.quantite += prod.quantite
                    deptProd.save()

                    # serializer = self.get_serializer(obj)
                    # return Response({'message': 'Object created successfully'}, status=status.HTTP_201_CREATED)
            caisse = serializer.instance.caisse
            caisse.montant_achats_four -= serializer.instance.montantregfour
            caisse.save()
            serializer.instance.fournisseur.solde += (
                serializer.instance.total - serializer.instance.montantregfour
            )
            serializer.instance.fournisseur.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FicheAchatFournisseurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FicheAchatCommandeFournisseur.objects.all()
    serializer_class = serializers.FicheACFournisseurSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.FicheAchatCommandeFournisseur.objects.filter(
            type_fiche="Achat"
        )
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user, type_fiche="Achat")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance = self.get_object()

        # Access the original instance information before modifications
        original_instance_data = serializers.FicheACFournisseurSerializer(instance).data
        original_montantregfour = original_instance_data.get("montantregfour")
        original_produits = original_instance_data.get("produits")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modifie_par=request.user)
            # serializer.instance.reste_a_payer = (
            #     serializer.instance.total - serializer.instance.montant_reg_client
            # )
            # serializer.instance.save()
            # serializer.instance
            # Updating the Caisse

            instanceCisse = serializer.instance.caisse

            # Updating the clients Solde
            fournisseur = serializer.instance.fournisseur
            fournisseur.solde += (
                original_montantregfour - serializer.instance.montantregfour
            )
            fournisseur.save()
            caisse = serializer.instance.caisse
            caisse.montant_achats_four += (
                original_montantregfour - serializer.instance.montantregfour
            )
            caisse.save()
            # serializer.save(saisie_par=request.user)
            # serializer.instance.reste_a_payer = (
            #     serializer.instance.total - serializer.instance.montant_reg_client
            # )
            # serializer.instance.save()

            produits = serializer.instance.produits.all()
            for produit in produits:
                if produit.produit:
                    old_prod = {}
                    for prod in original_produits:
                        if prod["produit"] == produit.produit.id:
                            old_prod = prod

                    filterProd = Produit.objects.get(id=produit.produit.id)
                    filterProd.qtte_vendue += produit.quantite - old_prod["quantite"]
                    filterProd.save()
                produit.prix_achat_produit = old_prod["prix_achat_produit"]
                produit.produit_article = old_prod["produit_article"]
                produit.prix_detail_produit = old_prod["prix_detail_produit"]
                produit.prix_gros_produit = old_prod["prix_gros_produit"]
                produit.prix_autre_produit = old_prod["prix_autre_produit"]
                produit.produit_unite = old_prod["produit_unite"]
                produit.total_prix = old_prod["total_prix"]
                produit.save()
                print(produit)

                # totalAchete = 0
                # if produit.produit:
                #     filterProd = Produit.objects.get(id=produit.produit.id)
                #     # prod = Produit.objects.get(id=filterProd.id)
                #     produitVente = ProduitVenteClient.objects.filter(
                #         produit__id=filterProd.id
                #     )
                #     # filterProd.qtte_vendue = 0
                #     for pV in produitVente:
                #         totalAchete = totalAchete + pV.quantite
                #         # filterProd.qtte_vendue += pV.quantite
                #         # print(pV.quantite)
                #     # print(totalAchete)
                #     filterProd.qtte_vendue = totalAchete
                #     filterProd.save()
                # print(prod.qtte_vendue)

        return Response(serializer.data)


class FicheCommandeFournisseurGetPost(generics.ListCreateAPIView):
    queryset = models.FicheAchatCommandeFournisseur.objects.filter(
        type_fiche="commande"
    )
    serializer_class = serializers.FicheACFournisseurSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.FicheAchatCommandeFournisseur.objects.filter(
            type_fiche="commande"
        )
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.FicheACFournisseurSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.FicheACFournisseurSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user, type_fiche="commande")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FicheCommandeFournisseurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FicheAchatCommandeFournisseur.objects.all()
    serializer_class = serializers.FicheACFournisseurSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.FicheAchatCommandeFournisseur.objects.filter(
            type_fiche="commande"
        )
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user, type_fiche="commande")


class PayementFournisseurGetPost(generics.ListCreateAPIView):
    queryset = models.PayementFournisseur.objects.all()
    serializer_class = serializers.PayementFournisseurSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.PayementFournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.PayementFournisseurSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PayementFournisseurSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            pay = serializer.instance
            pay.caisse.montant_pay_four += pay.montant
            pay.caisse.save()
            pay.fournisseur.solde -= pay.montant
            pay.fournisseur.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayementFournisseurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PayementFournisseur.objects.all()
    serializer_class = serializers.PayementFournisseurSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.PayementFournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance = self.get_object()

        # Access the original instance information before modifications
        original_instance_data = serializers.PayementFournisseurSerializer(
            instance
        ).data
        original_montant = original_instance_data.get("montant")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modifie_par=request.user)
            # serializer.instance.reste_a_payer = (
            #     serializer.instance.total - serializer.instance.montant_reg_client
            # )
            serializer.instance.save()

            fournisseur = serializer.instance.fournisseur
            fournisseur.solde += original_montant - serializer.instance.montant
            fournisseur.save()
            caisse = serializer.instance.caisse
            caisse.montant_pay_four += original_montant - serializer.instance.montant
            caisse.save()
            # serializer.save(saisie_par=request.user)
            serializer.instance.save()

        return Response(serializer.data)


class RetourFournisseurGetPost(generics.ListCreateAPIView):
    queryset = models.RetoursFournisseur.objects.all()
    serializer_class = serializers.RetoursFournisseurSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.RetoursFournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.RetoursFournisseurSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.RetoursFournisseurSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            for prod in serializer.instance.produits.all():
                prod.produit.qtte_retour_four += prod.quantite_retour
                prod.produit.save()
            caisse = serializer.instance.caisse
            caisse.montant_pay_four += serializer.instance.montant
            caisse.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetoursFournisseurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.RetoursFournisseur.objects.all()
    serializer_class = serializers.RetoursFournisseurSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.RetoursFournisseur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)


# -------------------------------------------------CLIENT------------------------------------------------


class ClientGetPost(generics.ListCreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.Client.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ClientSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Client.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class FicheVenteClientGetPost(generics.ListCreateAPIView):
    queryset = models.FicheVenteClient.objects.all()
    serializer_class = serializers.FicheVenteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.FicheVenteClient.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.FicheVenteSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.FicheVenteSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            serializer.instance.reste_a_payer = (
                serializer.instance.total - serializer.instance.montant_reg_client
            )
            serializer.instance.save()
            for prod in serializer.instance.produits.all():
                proddepot = models.ProduitDepot.objects.get(
                    produit=prod.produit, depot=prod.depot
                )
                proddepot.quantite -= prod.quantite
                proddepot.save()
                prod.produit.qtte_vendue += prod.quantite
                prod.produit.save()

            caisse = serializer.instance.caisse
            caisse.montant_vente_client += serializer.instance.montant_reg_client
            caisse.save()
            client = serializer.instance.client
            client.solde += (
                serializer.instance.total - serializer.instance.montant_reg_client
            )
            client.save()
            print("posted successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FicheVenteClientPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FicheVenteClient.objects.all()
    serializer_class = serializers.FicheVenteSerializer
    permission_classes = [
        IsAuthenticated,
        # DjangoModelPermissionsOrAnonReadOnly,
        # IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.FicheVenteClient.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance = self.get_object()

        # Access the original instance information before modifications
        original_instance_data = serializers.FicheVenteSerializer(instance).data
        original_montant_reg_client = original_instance_data.get("montant_reg_client")
        original_produits = original_instance_data.get("produits")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modifie_par=request.user)
            serializer.instance.reste_a_payer = (
                serializer.instance.total - serializer.instance.montant_reg_client
            )
            serializer.instance.save()
            # serializer.instance
            # Updating the Caisse

            instanceCisse = serializer.instance.caisse

            # Updating the clients Solde
            client = serializer.instance.client
            client.solde += (
                original_montant_reg_client - serializer.instance.montant_reg_client
            )
            client.save()
            caisse = serializer.instance.caisse
            caisse.montant_vente_client += (
                original_montant_reg_client - serializer.instance.montant_reg_client
            )
            caisse.save()
            # serializer.save(saisie_par=request.user)
            serializer.instance.reste_a_payer = (
                serializer.instance.total - serializer.instance.montant_reg_client
            )
            serializer.instance.save()

            produits = serializer.instance.produits.all()
            for produit in produits:
                if produit.produit:
                    old_prod = {}
                    for prod in original_produits:
                        if prod["produit"] == produit.produit.id:
                            old_prod = prod
                    proddepot = models.ProduitDepot.objects.get(
                        produit=produit.produit, depot=produit.depot
                    )
                    proddepot.quantite -= produit.quantite - old_prod["quantite"]
                    proddepot.save()
                    filterProd = Produit.objects.get(id=produit.produit.id)
                    filterProd.qtte_vendue += produit.quantite - old_prod["quantite"]
                    filterProd.save()
                produit.prix_achat_produit = old_prod["prix_achat_produit"]
                produit.produit_article = old_prod["produit_article"]
                produit.prix_detail_produit = old_prod["prix_detail_produit"]
                produit.prix_gros_produit = old_prod["prix_gros_produit"]
                produit.prix_autre_produit = old_prod["prix_autre_produit"]
                produit.produit_unite = old_prod["produit_unite"]
                produit.total_prix = old_prod["total_prix"]
                produit.save()
                # print(produit)

                # totalAchete = 0
                # if produit.produit:
                #     filterProd = Produit.objects.get(id=produit.produit.id)
                #     # prod = Produit.objects.get(id=filterProd.id)
                #     produitVente = ProduitVenteClient.objects.filter(
                #         produit__id=filterProd.id
                #     )
                #     # filterProd.qtte_vendue = 0
                #     for pV in produitVente:
                #         totalAchete = totalAchete + pV.quantite
                #         # filterProd.qtte_vendue += pV.quantite
                #         # print(pV.quantite)
                #     # print(totalAchete)
                #     filterProd.qtte_vendue = totalAchete
                #     filterProd.save()
                # print(prod.qtte_vendue)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)


class PayementClientGetPost(generics.ListCreateAPIView):
    queryset = models.PayementClient.objects.all()
    serializer_class = serializers.PayementClientSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.PayementClient.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.PayementClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PayementClientSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            pay = serializer.instance
            pay.client.solde -= pay.montant
            pay.client.save()
            caisse = serializer.instance.caisse
            caisse.montant_pay_client += serializer.instance.montant
            caisse.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayementClientPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PayementClient.objects.all()
    serializer_class = serializers.PayementClientSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.PayementClient.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance = self.get_object()

        # Access the original instance information before modifications
        original_instance_data = serializers.PayementClientSerializer(instance).data
        original_montant = original_instance_data.get("montant")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(modifie_par=request.user)
            # serializer.instance.reste_a_payer = (
            #     serializer.instance.total - serializer.instance.montant_reg_client
            # )
            serializer.instance.save()

            client = serializer.instance.client
            client.solde += original_montant - serializer.instance.montant
            client.save()
            caisse = serializer.instance.caisse
            caisse.montant_pay_client += original_montant - serializer.instance.montant
            caisse.save()
            # serializer.save(saisie_par=request.user)
            serializer.instance.save()

        return Response(serializer.data)


class RetourClientGetPost(generics.ListCreateAPIView):
    queryset = models.RetoursClient.objects.all()
    serializer_class = serializers.RetoursClientSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.RetoursClient.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.RetoursClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.RetoursClientSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(saisie_par=request.user)
            for prod in serializer.instance.produits.all():
                prod.produit.qtte_retour_client += prod.quantite_retour
                prod.produit.save()
            caisse = serializer.instance.caisse
            caisse.montant_retour_client += serializer.instance.montant
            caisse.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class RetoursClientPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.RetoursClient.objects.all()
    serializer_class = serializers.RetoursClientSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.RetoursClient.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def perform_update(self, serializer):
        serializer.save(modifie_par=self.request.user)


# ------------------------------------------------TRANSPORT-------------------------------------------------


class TransporteurGetPost(generics.ListCreateAPIView):
    queryset = models.Transporteur.objects.all()
    serializer_class = serializers.TransporteurSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.Transporteur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.TransporteurSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.TransporteurSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransporteurPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Transporteur.objects.all()
    serializer_class = serializers.TransporteurSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Transporteur.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class ClarqueGetPost(generics.ListCreateAPIView):
    queryset = models.Clarque.objects.all()
    serializer_class = serializers.ClarqueSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = models.Clarque.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ClarqueSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ClarqueSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClarquePk(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Clarque.objects.all()
    serializer_class = serializers.ClarqueSerializer
    permission_classes = [
        IsAuthenticated,
        DjangoModelPermissionsOrAnonReadOnly,
        IsSPUser,
    ]

    def get_queryset(self):
        queryset = models.Clarque.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                selling_point=self.request.user.vendeur.selling_point
            )
        return queryset


class SituationGleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        ventes = models.FicheVenteClient.objects.all()
        total_ventes = 0
        total_remises = 0
        for vente in ventes:
            total_ventes += vente.total
            total_remises += vente.remise

        total_achats = 0
        achats = models.FicheAchatCommandeFournisseur.objects.filter(type_fiche="1")
        for achat in achats:
            total_achats += achat.prixTTC

        benefice_ventes_achats = total_ventes - total_achats

        retours_clients = models.RetoursClient.objects.all()
        total_retours_clients = 0
        for retour in retours_clients:
            total_retours_clients += retour.montant

        retours_four = models.RetoursFournisseur.objects.all()
        tatal_retour_four = 0
        for retour in retours_four:
            tatal_retour_four += retour.montant

        avaries = models.Avaries.objects.all()
        total_avaries = 0
        for ava in avaries:
            total_avaries += ava.montant

        total_benefice = (
            total_ventes
            - total_achats
            + tatal_retour_four
            - total_retours_clients
            - total_avaries
        )

        context = {
            "total_achats": total_achats,
            "total_ventes": total_ventes,
            "total_retours_clients": total_retours_clients,
            "tatal_retour_four": tatal_retour_four,
            "total_avaries": total_avaries,
            "total_benefice": total_benefice,
        }
        return Response(context)
