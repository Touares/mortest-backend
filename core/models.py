import datetime
from django.conf import Settings
from django.db import models
from users.models import CustomUser as User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# ----------------------------------SELLING POINT----------------------------------------------


class SellingPoint(models.Model):
    name = models.CharField(max_length=100)
    societé = models.CharField(max_length=100)
    adress = models.CharField(max_length=200)
    wilaya = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    telephone = models.IntegerField()
    fax = models.IntegerField()
    email = models.EmailField()
    articles_dimposition = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} selling point"


class Caisse(models.Model):
    selling_point = models.ForeignKey(
        SellingPoint, on_delete=models.CASCADE, related_name="selling_point_caisse"
    )
    caisse_data = (("principale", "principale"), ("secondaire", "secondaire"))
    caisse = models.CharField(default=1, choices=caisse_data, max_length=20)
    nom = models.CharField(max_length=50)
    wilaya = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    solde = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    montant_achats_four = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )
    montant_retour_four = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )
    montant_pay_four = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    montant_vente_client = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )
    montant_retour_client = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )
    montant_credit = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    montant_pay_client = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    montant_debit = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    montant_frais_generales = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )

    def __str__(self) -> str:
        return f"{self.nom} caisse"

    def somme(self):
        somme = (
            self.montant_vente_client
            - self.montant_achats_four
            + self.montant_retour_four
            + self.montant_credit
            - self.montant_pay_four
            + self.montant_pay_client
            - self.montant_retour_client
            - self.montant_debit
            - self.montant_frais_generales
        )
        return somme


class FamilleProduit(models.Model):
    famille = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.famille


class MarqueProduit(models.Model):
    marque = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.marque


class Produit(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE, default=1)
    reference = models.CharField(max_length=200)
    article = models.TextField(max_length=200)
    img = models.ImageField(null=True, blank=True, upload_to="images/produits/")
    unit_data = (("m²", "m²"), ("m", "m"), ("L", "L"), ("Kg", "Kg"), ("g", "g"))
    unit = models.CharField(default=1, choices=unit_data, max_length=20)
    # famille_data = (('1',"1"),('2',"2"),('3',"3"), ('4',"4"), ('4',"5"))
    # famille = models.CharField(choices=famille_data,max_length=20, default=1)
    famille = models.ForeignKey(FamilleProduit, on_delete=models.CASCADE, default=1)
    # marque_data = (('1',"1"),('2',"2"),('3',"3"), ('4',"4"), ('5',"5"))
    # marque = models.CharField(choices=marque_data,max_length=20, default=1)

    marque = models.ForeignKey(MarqueProduit, on_delete=models.CASCADE, default=1)
    prix_U_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_detail = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente_gros = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente_revendeur = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    prix_vente_autre = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    stock_alerte = models.PositiveIntegerField(blank=True, null=True)
    qtte = models.PositiveIntegerField(blank=True, null=True, default=0)
    qtte_achete = models.PositiveIntegerField(blank=True, default=0)
    qtte_vendue = models.PositiveIntegerField(blank=True, default=0)
    qtte_retour_four = models.PositiveIntegerField(blank=True, default=0)
    qtte_retour_client = models.PositiveIntegerField(blank=True, default=0)
    qtte_avarie = models.PositiveIntegerField(blank=True, default=0)
    ancien_prix = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.article}"

    @property
    def qtteActuelStock(self):
        qtteact = (
            self.qtte
            + self.qtte_achete
            - self.qtte_retour_four
            - self.qtte_vendue
            + self.qtte_retour_client
            - self.qtte_avarie
        )
        return qtteact

    @property
    def margePprixDetail(self):
        marge = self.prix_detail - self.prix_U_achat
        pourcentage_marge = (marge * 100) / self.prix_U_achat
        return pourcentage_marge

    @property
    def margeVenteGrossiste(self):
        if not self.prix_vente_gros and self.prix_U_achat:
            return None
        marge = self.prix_vente_gros - self.prix_U_achat
        pourcentage_marge = (marge * 100) / self.prix_U_achat
        return pourcentage_marge

    @property
    def margeVenteRevendeur(self):
        if not self.prix_vente_revendeur and self.prix_U_achat:
            return None
        marge = self.prix_vente_revendeur - self.prix_U_achat
        pourcentage_marge = (marge * 100) / self.prix_U_achat
        return pourcentage_marge

    @property
    def margeVenteAutre(self):
        if not self.prix_vente_autre and self.prix_U_achat:
            return None
        marge = self.prix_vente_autre - self.prix_U_achat
        pourcentage_marge = (marge * 100) / self.prix_U_achat
        return pourcentage_marge


class Depot(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.PROTECT)
    nom = models.CharField(max_length=100)
    adresse = models.TextField(max_length=500)
    produits = models.ManyToManyField(Produit, related_name="produits", blank=True)

    def __str__(self) -> str:
        return f"{self.nom} dépot"


class Avaries(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)

    qtte = models.PositiveBigIntegerField()
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)

    @property
    def depot(self):
        depot = self.produit.depot
        return depot

    @property
    def montant(self):
        prix = self.produit.prix_U_achat * self.qtte
        return prix

    def __str__(self) -> str:
        return f"{self.produit.article} avarié"


class FicheCredit(models.Model):
    selling_point = models.ForeignKey(
        SellingPoint, on_delete=models.CASCADE, related_name="selling_point_fc"
    )
    date = models.DateField(auto_now=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    TVA = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=5,
        decimal_places=2,
    )
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    reglement = models.CharField(
        default="Espece", choices=reglement_data, max_length=20
    )
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observ = models.TextField(max_length=500)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saisie_par_cr"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modifie_par_cr", null=True
    )

    @property
    def montantTVA(self):
        montant = (self.TVA * self.montant) / 100
        return montant

    @property
    def prixTTC(self):
        montant = self.montant + self.montantTVA
        return montant

    def __str__(self) -> str:
        return f"fiche crédit de la caisse {self.caisse.nom}"


class FicheDebit(models.Model):
    selling_point = models.ForeignKey(
        SellingPoint,
        on_delete=models.CASCADE,
        related_name="selling_point_fd",
        default=1,
    )
    date = models.DateField(auto_now=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    TVA = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=5,
        decimal_places=2,
    )
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    reglement = models.CharField(
        default="Espece", choices=reglement_data, max_length=20
    )
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observ = models.TextField(max_length=500)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saisie_par_deb"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modifie_par_deb", null=True
    )

    @property
    def montantTVA(self):
        montant = (self.TVA * self.montant) / 100
        return montant

    @property
    def prixTTC(self):
        montant = self.montant - self.montantTVA
        return montant

    def __str__(self):
        return f"fiche débit de la caisse {self.caisse.nom}"


class Vendeur(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50, null=True, blank=True)
    # last_name = models.CharField(max_length=50, null=True, blank=True)
    # img = models.ImageField(null=True, blank=True, upload_to="images/produits/")
    # adress = models.CharField(max_length=100, null=True, blank=True)
    # identity_num = models.PositiveBigIntegerField(null=True, blank=True, unique=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    # phone_number_1 = models.PositiveBigIntegerField(null=True, blank=True)
    # phone_number_2 = models.PositiveBigIntegerField(blank=True, null=True)
    # family_situation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.admin.username}"


class TypeFG(models.Model):
    type = models.CharField(max_length=100)


class FraisGenerales(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE, default=1)
    date = models.DateField(auto_now=True)
    # number = models.CharField(max_length = 20, default = self.increment_booking_number, editable=False)    date = models.DateField()
    # type_data=(('1',"type1"),('2',"type2"),('3',"type3"), ('4',"type4"),)
    type = models.ForeignKey(TypeFG, on_delete=models.PROTECT)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    TVA = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=10,
        decimal_places=2,
    )

    timbre = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    reglement = models.CharField(
        default="Espece", choices=reglement_data, max_length=20
    )
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saisie_par_fg"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modifie_par_fg", null=True
    )
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observation = models.TextField(max_length=500)

    @property
    def montantTVA(self):
        montant = (self.TVA * self.montant) / 100
        return montant

    @property
    def prixTTC(self):
        montant = self.montant - self.montantTVA - self.timbre
        return montant

    def __str__(self) -> str:
        return f"frais {self.number} de la caisse {self.caisse.nom}"

    @property
    def increment_number(self):
        last = self.objects.all().order_by("id").last()
        if not last:
            # return 'RNH' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '0000'
            return 1

        booking_id = last.number
        # booking_int = int(booking_id[9:13])
        new_booking_id = booking_id + 1
        # new_booking_id = 'RNH' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_booking_int).zfill(4)
        return new_booking_id

        # -----------------------------------------FOURNISSEURS---------------------------------------------


class Fournisseur(models.Model):
    etat_civile_data = (
        ("M.", "M."),
        ("Mme", "Mme"),
        ("SARL", "SARL"),
        ("EURL", "EURL"),
        ("ETS", "ETS"),
        ("autre", "autre"),
    )
    etat_civile = models.CharField(
        default="M.", choices=etat_civile_data, max_length=20
    )
    name = models.CharField(max_length=50)
    telephone = models.IntegerField(blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    fax = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    NRC = models.CharField(max_length=50, blank=True, null=True)
    NIS = models.CharField(max_length=50, blank=True, null=True)
    RIB = models.CharField(max_length=50, blank=True, null=True)
    solde = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    wilaya = models.CharField(max_length=50, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.CharField(max_length=100, blank=True, null=True)
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.etat_civile} {self.name}"


class FicheAchatCommandeFournisseur(models.Model):
    type_fiche_data = (("Achat", "Achat"), ("Commande", "Commande"))
    type_fiche = models.CharField(default=1, choices=type_fiche_data, max_length=10)
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.PROTECT, default=1)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT, default=1)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saisie_par_fac"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="modifie_par_fac"
    )
    action_data = (
        ("facture", "facture"),
        ("bon", "bon"),
        ("bon de commande", "bon de commande"),
    )
    action = models.CharField(default=1, choices=action_data, max_length=30)
    numero = models.PositiveIntegerField(default=1)
    # code = models.IntegerField()
    date = models.DateField(auto_now=True)
    # prix = models.DecimalField(max_digits=10, decimal_places=2)
    # qtt_stock_actuel = models.DecimalField(max_digits=5, decimal_places=2)

    # Reglement fournisseur
    montantregfour = models.DecimalField(max_digits=10, decimal_places=2)
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    mode_reglement = models.CharField(
        default="Espece", choices=reglement_data, max_length=20
    )
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observation = models.TextField(max_length=500)

    # montant de fournisseur
    # prixHT = models.DecimalField(max_digits=10, decimal_places=2)
    # montant de fournisseur
    # prixHT = models.DecimalField(max_digits=10, decimal_places=2)
    TVA = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=10,
        decimal_places=2,
    )
    timbre = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    remise = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=10,
        decimal_places=2,
    )

    # def save(self, *args, **kwargs):
    #     last = self.objects.all().order_by('id').last()
    #     if not last:
    #         # return 'RNH' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '0000'
    #         self.numero = 1

    #     last_numero = last.numero
    #     # booking_int = int(booking_id[9:13])
    #     self.numero = last_numero + 1
    #     # new_booking_id = 'RNH' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_booking_int).zfill(4)
    #     super(FicheAchatCommandeFournisseur, self).save()

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = self.__class__.objects.all().aggregate(
                largest=models.Max("numero")
            )["largest"]

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.numero = last_id + 1

        super(FicheAchatCommandeFournisseur, self).save(*args, **kwargs)

    @property
    def total(self):
        prix = 0
        for prod in self.produits.all():
            prix += prod.produit.prix_U_achat * prod.quantite

        return prix

    @property
    def montantTVA(self):
        prix = self.total
        montant = (self.TVA * prix) / 100
        return montant

    @property
    def montantRemise(self):
        prix = self.total
        montant = (self.remise * prix) / 100
        return montant

    @property
    def prixTTC(self):
        prix = self.total
        montant = prix + self.montantTVA - self.montantRemise + self.timbre
        return montant

    def __str__(self) -> str:
        return f"{self.type_fiche} {self.fournisseur.name} {self.numero}"


class ProduitAchatCommandeFournisseur(models.Model):
    achat = models.ForeignKey(
        FicheAchatCommandeFournisseur, related_name="produits", on_delete=models.CASCADE
    )
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    produit = models.ForeignKey(
        Produit, related_name="produit_achat_fournisseur", on_delete=models.CASCADE
    )
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    numero_lot = models.IntegerField()
    date_de_fabrication = models.DateField()
    date_dexpiration = models.DateField()
    unit_choices = (("m²", "m²"), ("m", "m"), ("L", "L"), ("Kg", "Kg"), ("g", "g"))
    unit = models.CharField(choices=unit_choices, max_length=20, default="Kg")
    # ajouter qtt stock actuel

    @property
    def prixProduit(self):
        prix = self.produit.prix_U_achat
        return prix

    @property
    def qtteActProduit(self):
        qtte = self.produit.qtteActuelStock
        return qtte


class PayementFournisseur(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saisie_par_pf"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="modifie_par_pf"
    )

    achat = models.ForeignKey(FicheAchatCommandeFournisseur, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    reglement = models.CharField(default=1, choices=reglement_data, max_length=20)
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observation = models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"fiche payement {self.fournisseur.name}"


class RetoursFournisseur(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE, default=1)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    date = models.DateField()
    achat = models.ForeignKey(FicheAchatCommandeFournisseur, on_delete=models.CASCADE)
    # produit = models.ManyToManyField(Produit, related_name="produit_fournisseur")
    # qtte_achetée = models.DecimalField(max_digits=10, decimal_places=2)
    # qtte_retour = models.DecimalField(max_digits=10, decimal_places=2)
    # depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    # montant = models.DecimalField(max_digits=10, decimal_places=2) becomes a function
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    reglement = models.CharField(default=1, choices=reglement_data, max_length=20)
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observation = models.TextField(max_length=500)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1111, related_name="saisie_par_rf"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modifie_par_rf", null=True
    )

    def produits(self):
        produits = Produit.objects.filter(
            ficheachatcommandefournisseur_id=self.achat.id
        )
        return produits

    @property
    def montant(self):
        mont = 0
        for prod in self.produits.all():
            prix = prod.produit.prix_U_achat
            mont += prix
        return mont

    def __str__(self) -> str:
        return f"fiche retour {self.fournisseur.name}, achat numéro {self.achat.numero}"


class ProduitsRetourFournisseur(models.Model):
    retour = models.ForeignKey(
        RetoursFournisseur, related_name="produits", on_delete=models.CASCADE
    )
    # depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    produit = models.ForeignKey(
        Produit, related_name="produit_retour_fournisseur", on_delete=models.CASCADE
    )
    # quantite = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_retour = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ---------------------------------- CLIENTS ----------------------------------------


class Client(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField(blank=True, null=True)
    etat_civile_data = (
        ("M.", "M."),
        ("Mme", "Mme"),
        ("SARL", "SARL"),
        ("EURL", "EURL"),
        ("ETS", "ETS"),
        ("autre", "autre"),
    )
    etat_civile = models.CharField(default=1, choices=etat_civile_data, max_length=20)
    nom = models.CharField(max_length=100)
    type_data = (
        ("Détaillant", "Détaillant"),
        ("Grossiste", "Grossiste"),
        ("Revendeur", "Revendeur"),
        ("autre", "autre"),
    )
    type = models.CharField(default=1, choices=type_data, max_length=30)
    telephone = models.IntegerField(blank=True, null=True)
    phone_number = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    numero_rc = models.PositiveIntegerField(blank=True, null=True)
    NRC = models.CharField(max_length=50, blank=True, null=True)
    NIF = models.CharField(max_length=50, blank=True, null=True)
    Al = models.CharField(max_length=50, blank=True, null=True)
    NIS = models.CharField(max_length=50, blank=True, null=True)
    RIB = models.CharField(max_length=50, blank=True, null=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wilaya = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    adress = models.CharField(max_length=100)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(User, on_delete=models.CASCADE, default=1111)

    def __str__(self) -> str:
        return f"{self.etat_civile}.{self.nom}"


class FicheVenteClient(models.Model):
    type_fiche_data = (
        ("Bon de livraison", "Bon de livraison"),
        ("Facture", "Facture"),
        ("BL sans montant", "BL sans montant"),
        ("Facture proformat", "Facture proformat"),
    )
    type_fiche = models.CharField(default=1, choices=type_fiche_data, max_length=30)
    type_client_data = (
        ("Détaillant", "Détaillant"),
        ("Grossiste", "Grossiste"),
        ("Revendeur", "Revendeur"),
        ("Autre", "Autre"),
    )
    type_client = models.CharField(default=1, choices=type_client_data, max_length=30)
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.PROTECT)
    numero = models.CharField(
        default="1", max_length=30
    )  # numero = models.BigAutoField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    # depot = models.ForeignKey(Depot, on_delete=models.PROTECT)
    # quantite = models.DecimalField(max_digits=10, decimal_places=2)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1111, related_name="saisie_par_vc"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modifie_par_vc", null=True
    )
    reste_a_payer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # code = models.IntegerField()
    # produit = models.ManyToManyField(Produit, related_name="produit_vente_client")
    date = models.DateField(auto_now=True)
    # prix = models.DecimalField(max_digits=10, decimal_places=2)

    # Reglement client
    montant_reg_client = models.DecimalField(max_digits=10, decimal_places=2)
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    mode_reglement = models.CharField(default=1, choices=reglement_data, max_length=20)
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observation = models.TextField(max_length=500, blank=True, null=True)

    # montant de fournisseur
    # prixHT = models.DecimalField(max_digits=10, decimal_places=2)
    TVA = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=10,
        decimal_places=2,
    )
    timbre = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    remise = models.DecimalField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=10,
        decimal_places=2,
    )

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        current_year = timezone.now().year
        # last_instance = (
        #     self.__class__.objects.filter(numero__icontains=f"{current_year}/")
        #     .order_by("-id")
        #     .first()
        # )
        last_instance = self.__class__.objects.all().order_by("-id").first()
        if self._state.adding:
            # Get the maximum display_id value from the database
            if last_instance:
                last_number = int(last_instance.numero.split("/")[0])
                last_year = int(last_instance.numero.split("/")[1])
                # last_year = "2023"
                # last_number = int(last_instance.numero.split('/')[0])
                if last_year == current_year:
                    self.numero = f"{last_number + 1}/{current_year}"
                else:
                    self.numero = f"1/{current_year}"
            else:
                self.numero = f"1/{current_year}"

            # last_id = self.__class__.objects.all().aggregate(
            #     largest=models.Max("numero")
            # )["largest"]

            # # aggregate can return None! Check it first.
            # # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            # if last_id is not None:
            #     self.numero = last_id + 1

        super(FicheVenteClient, self).save(*args, **kwargs)

    # @property
    # def total(self):
    #     prix = 0
    #     for prod in self.produits.all():
    #         if self.type_client == "Détaillant":
    #             prix += prod.produit.prix_detail * prod.quantite
    #         elif self.type_client == "Grossiste":
    #             prix += prod.produit.prix_vente_gros * prod.quantite
    #         elif self.type_client == "Revendeur":
    #             prix += prod.produit.prix_vente_revendeur * prod.quantite
    #         else:
    #             prix += prod.produit.prix_vente_autre * prod.quantite

    #     return prix

    @property
    def montantTVA(self):
        prix = self.subtotal
        montant = (self.TVA * prix) / 100
        return montant

    @property
    def montantRemise(self):
        prix = self.subtotal
        montant = (self.remise * prix) / 100
        return montant

    @property
    def montantTimbre(self):
        prix = self.subtotal
        montant = (self.timbre * prix) / 100
        return montant

    # @property
    # def prixTTC(self):
    #     prix = self.total
    #     montant = prix + self.montantTVA - self.montantRemise + self.timbre
    #     return montant

    def __str__(self) -> str:
        return f"{self.type_fiche} {self.client.nom}"


class ProduitVenteClient(models.Model):
    vente = models.ForeignKey(
        FicheVenteClient, related_name="produits", on_delete=models.CASCADE
    )
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    produit = models.ForeignKey(
        Produit,
        related_name="produit_vente_client",
        on_delete=models.SET_NULL,
        null=True,
    )
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    numero_lot = models.IntegerField(blank=True, null=True)
    total_prix = models.IntegerField(blank=True, null=True)
    prix_detail_produit = models.IntegerField(blank=True, null=True)
    prix_gros_produit = models.IntegerField(blank=True, null=True)
    prix_autre_produit = models.IntegerField(blank=True, null=True)
    produit_reference = models.CharField(max_length=200, null=True, blank=True)
    # produit_reference = models.CharField(max_length=200, null=True, blank=True)
    produit_article = models.CharField(max_length=200, null=True, blank=True)
    produit_unite = models.CharField(max_length=200, null=True, blank=True)

    @property
    def qtteActProduit(self):
        if self.produit:
            qtte = self.produit.qtteActuelStock
        if self.produit:
            return qtte
        return "deleted"

    @property
    def numeroVente(self):
        vente = self.vente.numero
        return vente


class PayementClient(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE, default=1)
    # date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    modilfie_par = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # blank=True
        null=True,
        related_name="modifie_par_pc",
    )

    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saisie_par_pc"
    )
    # achat = models.ForeignKey(FicheAchatCommandeFournisseur, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    reglement = models.CharField(default=1, choices=reglement_data, max_length=20)
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observation = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        return f"payement {self.client.nom}"


class RetoursClient(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE, default=1)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    vente = models.ForeignKey(
        FicheVenteClient,
        on_delete=models.CASCADE,
        default=1,
        related_name="retours_client",
    )
    # depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    # montant = models.DecimalField(max_digits=10, decimal_places=2)
    reglement_data = (
        ("A terme", "A terme"),
        ("Espece", "Espece"),
        ("Virement", "Virement"),
        ("chèque", "chèque"),
    )
    reglement = models.CharField(default=1, choices=reglement_data, max_length=20)
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE)
    observation = models.TextField(max_length=500)
    saisie_le = models.DateField(auto_now_add=True)
    modilfié_le = models.DateField(auto_now=True)
    saisie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1111, related_name="saisie_par_rc"
    )
    modifie_par = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modifie_par_rc", null=True
    )

    def __str__(self) -> str:
        return f"retour {self.client.nom}"

    def produits(self):
        produits = Produit.objects.filter(ficheventeclient_id=self.vente.id)
        return produits

    @property
    def montant(self):
        prix = 0
        for prod in self.produits.all():
            if self.vente.type_client == "détaillant":
                prix += prod.produit.prix_detail
            elif self.vente.type_client == "grossiste":
                prix += prod.produit.prix_vente_gros
            elif self.vente.type_client == "revendeur":
                prix += prod.produit.prix_vente_revendeur
            else:
                prix += prod.produit.prix_vente_autre

        return prix


class ProduitsRetourClient(models.Model):
    retour = models.ForeignKey(
        RetoursClient, related_name="produits", on_delete=models.CASCADE
    )
    # depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    produit = models.ForeignKey(
        Produit, related_name="produit_retour_client", on_delete=models.CASCADE
    )
    # quantite = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_retour = models.DecimalField(max_digits=10, decimal_places=2, default=0)


# ---------------------------------------------TRANSPORT--------------------------------------------


class Transporteur(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    vehicule = models.CharField(max_length=100)
    poids = models.PositiveIntegerField()
    id_num = models.PositiveBigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.vehicule} - {self.poids} kg"


class Clarque(models.Model):
    selling_point = models.ForeignKey(SellingPoint, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    vehicule = models.CharField(max_length=100)
    poids = models.PositiveIntegerField()
    id_num = models.PositiveBigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.vehicule} - {self.poids} kg"
