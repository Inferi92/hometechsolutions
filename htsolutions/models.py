from ast import Sub
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)

# TABELA DAS CATEGORIAS
class Category(models.Model):
    name = models.CharField(max_length=55, null=False, blank=False)

    def __str__(self):
        return self.name


# TABELA DAS FAMÍLIAS
class Family(models.Model):
    name = models.CharField(max_length=55, null=False, blank=False)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return self.name


# TABELA DAS SUBFAMÍLIAS
class SubFamily(models.Model):
    name = models.CharField(max_length=55, null=False, blank=False)
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return self.name


# TABELA DAS MARCAS
class Brand(models.Model):
    name = models.CharField(max_length=55, null=False, blank=False)

    def __str__(self):
        return self.name


# TABELA DOS ATRIBUTOS
class Attribute(models.Model):
    name = models.CharField(max_length=55, null=False, blank=False)

    def __str__(self):
        return self.name


# TABELA DOS PRODUTOS
class Product(models.Model):
    currency = [
        ("€", "EUROS (€)"),
        ("$", "US DOLARS ($)"),
        ("£", "LIBRAS (£)"),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    currency = models.CharField(max_length=5, choices=currency, default="€")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    brand = models.ForeignKey(
        "Brand", on_delete=models.CASCADE, null=False, blank=False
    )
    subFamily = models.ForeignKey(
        "SubFamily", on_delete=models.CASCADE, null=False, blank=False
    )
    image = models.ImageField(default="not_found.jpg")
    attribute = models.ManyToManyField(Attribute, null=False, blank=False)
    ean = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(r"[1-9]\d*"),
            MinLengthValidator(13),
            MaxLengthValidator(13),
        ],
        default="0000000000001",
        unique=True,
        null=False,
        blank=False,
    )
    createdDate = models.DateField(default=date.today, null=False, blank=False)
    expectedAvailabilityDate = models.DateField(null=True, blank=True)
    expectedDeliveryDate = models.DateField(null=True, blank=True)
    stock = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999),
        ],
        default=0,
        null=False,
        blank=False,
    )

    # ESTADOS DE STOCK DO PRODUTO
    STOCK_STATUS = (
        ("0", "Sem Stock"),
        ("1", "Em Stock"),
        ("2", "Por Encomenda"),
    )

    stockStatus = models.CharField(
        max_length=1,
        validators=[
            RegexValidator(r"[1-3]"),
            MinLengthValidator(1),
            MaxLengthValidator(1),
        ],
        choices=STOCK_STATUS,
        blank=False,
        null=False,
        default="0",
        help_text="Stock do produto",
    )

    def __str__(self):
        return self.name
