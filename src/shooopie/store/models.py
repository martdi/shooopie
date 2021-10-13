from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()

class ProductQueryset(models.QuerySet):
    def by_status(self, status_id):
        return self.filter(status_id=status_id)

    def in_catalog(self):
        return self.filter(status__show_in_catalog=True)
    
    def by_tag_name(self, tag_name):
        return self.filter(tags__name=tag_name)

    def exclude_by_tag_name(self, tag_name):
        return self.exclude(tags__name=tag_name)

    def by_category_name(self, category_name):
        return self.filter(categories__name=category_name)

    def exclude_by_category_name(self, category_name):
        return self.exclude(categories__name=category_name)

    def delete(self):
        for obj in self:
            obj.delete()

class ProductStatus(models.Model):
    DRAFT = 0
    PUBLISHED = 1
    DISCONTINUED = 2

    name = models.CharField(max_length=100)
    show_in_catalog = models.BooleanField(verbose_name=_('Show in product catalog'))

class Tax(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(verbose_name=_('Tax rate'), decimal_places=6, max_digits=10)

class Product(models.Model):
    objects = ProductQueryset.as_manager()
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField(max_length=100, verbose_name=_('Slug'))
    description = models.TextField(verbose_name=_('Description'))
    price = models.DecimalField(verbose_name=_('Price'), decimal_places=2, max_digits=8)
    status = models.ForeignKey(ProductStatus, on_delete=models.PROTECT, verbose_name=_('Status'))
    applicable_taxes = models.ManyToManyField(Tax, verbose_name=_('Applicable taxes'))

    def delete(self):
        self.status_id = ProductStatus.DISCONTINUED
        self.save()


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartDetails')

class CartDetails(models.Model):
    cart = models.ForeignKey('cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='categories')

class Tag(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='tags')

class InvoiceLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    tax_rate = models.DecimalField(decimal_places=2, max_digits=8)

class ShippingMethod(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    e_mail = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    postal_code_or_zip = models.CharField(max_length=7)

class InvoiceStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Status'))

class Invoice(models.Model):
    number = models.CharField(max_length=8)
    products = ManyToManyField(Product, related_name='invoices', through=InvoiceLine)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.ForeignKey(InvoiceStatus, on_delete=models.PROTECT)