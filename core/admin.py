from django.contrib import admin
from .models import (Avaries, ProduitVenteClient, ProduitsRetourClient, SellingPoint, Caisse, Produit, Depot, FicheCredit,
 FicheDebit, Vendeur, Fournisseur, FicheAchatCommandeFournisseur,
 PayementFournisseur,  RetoursFournisseur, FraisGenerales, FamilleProduit, MarqueProduit,
 Client, FicheVenteClient, PayementClient, RetoursClient, ProduitAchatCommandeFournisseur, ProduitsRetourFournisseur,
 Transporteur, Clarque)

admin.site.register(SellingPoint)
admin.site.register(Caisse)
admin.site.register(Produit)
admin.site.register(Depot)
admin.site.register(Vendeur)
admin.site.register(Fournisseur)
admin.site.register(FamilleProduit)
admin.site.register(MarqueProduit)
class PACFInline(admin.StackedInline):
    model = ProduitAchatCommandeFournisseur

class FicheAchatCommandeFournisseurAdmin(admin.ModelAdmin):
     inlines = [PACFInline,]

admin.site.register(FicheAchatCommandeFournisseur, FicheAchatCommandeFournisseurAdmin)
class PRFInline(admin.StackedInline):
    model = ProduitsRetourFournisseur

class RetourAdmin(admin.ModelAdmin):
     inlines = [PRFInline,]

admin.site.register(RetoursFournisseur, RetourAdmin)

class PVCInline(admin.StackedInline):
    model = ProduitVenteClient
class VenteClientAdmin(admin.ModelAdmin):
     inlines = [PVCInline,]

admin.site.register(FicheVenteClient, VenteClientAdmin)

class PRCInline(admin.StackedInline):
    model = ProduitsRetourClient

class RetourAdmin(admin.ModelAdmin):
     inlines = [PRCInline,]

admin.site.register(RetoursClient, RetourAdmin)

admin.site.register(PayementFournisseur)
admin.site.register(Client)
admin.site.register(PayementClient)
admin.site.register(FraisGenerales)
admin.site.register(FicheDebit)
admin.site.register(FicheCredit)
admin.site.register(Avaries)
admin.site.register(Transporteur)
admin.site.register(Clarque)





# Register your models here.
