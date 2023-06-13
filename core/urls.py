from os import name
from django.contrib import admin
from django.urls import path, include

from . import cbv
from . import views

urlpatterns = [

#--------------------------------------------SELLING POINT--------------------------------------------

    path('sp_get_post', cbv.SellingPoitGetPost.as_view(), name='sp_get_post'),
    path('famille_get_post', views.familleProduitGETPOST, name='famille_get_post'),
    path('marque_get_post', views.marqueProduitGETPOST, name='marque_get_post'),
    path('sp_pk/<int:pk>', cbv.SellingPoitPk.as_view(), name='sp_pk'),
    path('caisse_get_post', cbv.CaisseGetPost.as_view(), name='caisse_get_post'),
    path('caisse_pk/<int:pk>', cbv.CaissePk.as_view(), name='caisse_pk'),
    path('produit_get_post', cbv.ProduitGetPost.as_view(), name='produit_get_post'),
    path('produit_pk/<int:pk>', cbv.ProduitPk.as_view(), name='produit_pk'),
    path('marqueproduit_get_post', cbv.MarqueProduitGetPost.as_view(), name='marqueproduit_get_post'),
    path('marqueproduit_pk/<int:pk>', cbv.MarqueProduitPk.as_view(), name='marqueproduit_pk'),
    path('Familleproduit_get_post', cbv.FamilleProduitGetPost.as_view(), name='Familleproduit_get_post'),
    path('Familleproduit_pk/<int:pk>', cbv.FamilleProduitPk.as_view(), name='Familleproduit_pk'),
    path('depot_get_post', cbv.DepotGetPost.as_view(), name='depot_get_post'),
    path('depot_pk/<int:pk>', cbv.DepotPk.as_view(), name='depot_pk'),
    path('fiche_credit_get_post', cbv.FicheCreditGetPost.as_view(), name='fiche_credit_get_post'),
    path('fiche_credit_pk/<int:pk>', cbv.FicheCreditPk.as_view(), name='fiche_credit_pk'),
    path('fiche_debit_get_post', cbv.FicheDebitGetPost.as_view(), name='fiche_debit_get_post'),
    path('fiche_debit_pk/<int:pk>', cbv.FicheDebitPk.as_view(), name='fiche_debit_pk'),
    path('vendeur_get_post', cbv.VendeurGetPost.as_view(), name='vendeur_post'),
    path('vendeur_pk/<int:pk>', cbv.VendeurPk.as_view(), name='vendeur_pk'),

#---------------------------------------------FOURNISSEUR----------------------------------------------------

    path('fournisseur_get_post', cbv.FournisseurGetPost.as_view(), name='fournisseur_get_post'),
    path('fournisseur_pk/<int:pk>', cbv.FournisseurPk.as_view(), name='fournisseur_pk'),
    path('ficheachatfournisseur_get_post', cbv.FicheAchatFournisseurGetPost.as_view(), name='ficheAchatfournisseur_get_post'),
    path('ficheachatfournisseur_pk/<int:pk>', cbv.FicheAchatFournisseurPk.as_view(), name='ficheAchatfournisseur_pk'),
    path('fichecommandefournisseur_get_post', cbv.FicheCommandeFournisseurGetPost.as_view(), name='fichecommandefournisseur_get_post'),
    path('fichecommanfournisseur_pk/<int:pk>', cbv.FicheCommandeFournisseurPk.as_view(), name='fichecommanfournisseur_pk'),
    path('payementfournisseur_get_post', cbv.PayementFournisseurGetPost.as_view(), name='payementfournisseur_get_post'),
    path('payementfournisseur_pk/<int:pk>', cbv.PayementFournisseurPk.as_view(), name='payementfournisseur_pk'),
    path('fraisgenerales_get_post', cbv.FraisGeneralesGetPost.as_view(), name='fraisgenerales_get_post'),
    path('fraisgenerales_pk/<int:pk>', cbv.FraisGeneralesPk.as_view(), name='raisgenerales_pk'),
    path('retourfournisseur_get_post', cbv.RetourFournisseurGetPost.as_view(), name='retourfournisseur_get_post'),
    path('retourfournisseur_pk/<int:pk>', cbv.RetoursFournisseurPk.as_view(), name='retourfournisseur_pk'),

#--------------------------------------------------CLIENT--------------------------------------------------

    path('client_pk/<int:pk>', cbv.ClientPk.as_view(), name='client_pk'),
    path('client_get_post', cbv.ClientGetPost.as_view(), name='client_get_post'),
    path('avaries_get_post', cbv.AvariesGetPost.as_view(), name='avaries_get_post'),
    path('avaries_pk/<int:pk>', cbv.AvariesPk.as_view(), name='avaries_pk'),
    path('venteclient_get_post', cbv.FicheVenteClientGetPost.as_view(), name='venteclient_get_post'),
    path('venteclient_pk/<int:pk>', cbv.FicheVenteClientPk.as_view(), name='venteclient_pk'),
    path('payementclient_get_post', cbv.PayementClientGetPost.as_view(), name='payementclient_get_post'),
    path('payementclient_pk/<int:pk>', cbv.PayementClientPk.as_view(), name='payementclient_pk'),
    path('retourclient_get_post', cbv.RetourClientGetPost.as_view(), name='retourclient_get_post'),
    path('retourclient_pk/<int:pk>', cbv.RetoursClientPk.as_view(), name='retourclient_pk'),

#------------------------------------------------TRANSPORT--------------------------------------------------

    path('transporteur_get_post', cbv.TransporteurGetPost.as_view(), name='transporteur_get_post'),
    path('transporteur_pk/<int:pk>', cbv.TransporteurPk.as_view(), name='transporteur_pk'),
    path('clarque_get_post', cbv.ClarqueGetPost.as_view(), name='clarque_get_post'),
    path('clrque_pk/<int:pk>', cbv.ClarquePk.as_view(), name='clrque_pk'),
    path('situationgle', views.situationGle, name='situationgle')
]