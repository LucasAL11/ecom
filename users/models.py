from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.db import models
from django.core.mail import send_mail
from localflavor.br.models import BRStateField,BRPostalCodeField

from uuid import uuid4


class AccounteManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'a conta não tem os requisitos necessarios.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'a conta não tem os requisitos necessarios.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser,PermissionsMixin):
        
    email = models.EmailField(_('email addres'), unique=True)
    user_name = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100,blank=False)
    last_name = models.CharField(max_length=100,blank=False)
    
    phone_types = [
        ('P','pessoal'),
        ('R','Residencial'),
        ('C','Comercial')
    ]
    phone_type = models.CharField(max_length=1, choices=phone_types, blank=False, null=False)
    phone_number = models.CharField(_('Phone number'), max_length=20, blank=True)

    #status da conta do usuario

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AccounteManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'user_name'
    ]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )
    
    def __str__(self):
        return self.user_name    


class Distribuitor(models.Model):
    email = models.EmailField(_('email addres'), unique=True)
    name = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100,blank=False)
    last_name = models.CharField(max_length=100,blank=False)





class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    custumer = models.ForeignKey(UserBase, verbose_name = _('first_name' +' '+ 'last_name'),
    on_delete=models.CASCADE 
    )
    address_choices = [
        ('R', 'Residencial'),
        ('P', 'Pessoal'),
        ('C', 'Comercial'),
        ('O', 'Outros')
    ]
    address_type = models.CharField(max_length=100, choices=address_choices, blank=False, null=False)
    name = models.CharField("Nome Completo", max_length=250)
    email = models.EmailField()
    postal_code = BRPostalCodeField("CEP")
    state = BRStateField("Estado")
    district = models.CharField("Bairro", max_length=250)
    street = models.CharField("Rua", max_length=250)
    number = models.CharField("Número", max_length=250)
    complement = models.CharField("Complemento", max_length=250, blank=True)
    
    city = models.CharField("Cidade", max_length=250)

    class Meta:
        ordering = ['custumer']

class Phone(models.CharField):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE )
    phone =  models.CharField(_('phone'),max_length=20)
    phone_type_choices = (
        ('R','Residencial'),
        ('C', 'Comercial'),
        ('O', 'Outros')
    )
    phone_type = models.CharField(max_length=1,choices=phone_type_choices)