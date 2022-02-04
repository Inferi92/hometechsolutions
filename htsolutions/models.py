from django.db import models
from datetime import date
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
        Category, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return self.name


# TABELA DAS SUBFAMÍLIAS
class SubFamily(models.Model):
    name = models.CharField(max_length=55, null=False, blank=False)
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, null=False, blank=False
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


# TABELA DAS CORES
class Color(models.Model):
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
    name = models.CharField(max_length=255, null=False, blank=False)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=False, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False, blank=False)
    currency = models.CharField(max_length=5, choices=currency, default="€")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    # ESTADOS DE STOCK DO PRODUTO
    CONDITION_STATUS = (
        ("1", "Novo"),
        ("2", "Usado"),
        ("3", "Recondicionado"),
    )
    conditionStatus = models.CharField(
        max_length=1,
        validators=[
            RegexValidator(r"[1-3]"),
            MinLengthValidator(1),
            MaxLengthValidator(1),
        ],
        choices=CONDITION_STATUS,
        blank=False,
        null=False,
        default="1",
        help_text="Condição do produto",
    )

    # ESTADOS DE STOCK DO PRODUTO
    GRADE_STATUS = (
        ("1", "A - Como novo"),
        ("2", "B - Algumas marcas de uso"),
        ("3", "C - Bastantes marcas de uso"),
    )
    gradeStatus = models.CharField(
        max_length=1,
        validators=[
            RegexValidator(r"[1-3]"),
            MinLengthValidator(1),
            MaxLengthValidator(1),
        ],
        default="",
        choices=GRADE_STATUS,
        blank=True,
        null=True,
        help_text="Condição do produto",
    )
    subFamily = models.ForeignKey(
        SubFamily, on_delete=models.CASCADE, null=False, blank=False
    )
    createdDate = models.DateField(default=date.today, null=False, blank=False)

    # ESTADOS DE STOCK DO PRODUTO
    STOCK_STATUS = (
        ("1", "Em Stock"),
        ("2", "Por Encomenda"),
        ("3", "Sem Stock"),
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
        default="3",
        help_text="Disponibilidade do produto",
    )
    stock = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999),
        ],
        null=False,
        blank=False,
        help_text="Quantidade do produto em stock",
    )
    expectedAvailabilityDate = models.DateField(null=True, blank=True)
    expectedDeliveryDate = models.DateField(null=True, blank=True)
    attribute = models.ManyToManyField(Attribute, null=False, blank=False)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["brand"]
