from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Class Client


class Customer(models.Model):
    """
    Name: Customer model definition
    """

    SEX_TYPES =(
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=12)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)  

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return self.name


# Class Facture

class Invoice(models.Model):
    INVOICE_TYPES = ( 
        ('R', 'RECU'),
        ('P', 'PROFORMA FACTURE'),
        ('F', 'FACTURE')
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10000, decimal_places=2)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPES)
    comments = models.TextField(max_length=1000, blank=True)  # ✅

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f"{self.customer.name} {self.invoice_date_time}"
    
    @property
    def get_total(self):
        articles = self.article_set.all()
        return sum(article.get_total for article in articles)
    
    

class Article(models.Model):
    """
    Name: Article model definition
    Description:
    Author: firstmanu25@yahoo.fr
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=1000, decimal_places=2)
    total = models.DecimalField(max_digits=1000, decimal_places=2)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural ="Articles"
    
    @property
    def get_total(self):
        total = self.quantity * self.unit_price
