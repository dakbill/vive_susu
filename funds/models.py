from django.contrib import admin
from django.db import models


class Account(models.Model):
    acc_num = models.CharField(max_length=60, unique=True)
    next_of_kin = models.CharField(max_length=150, blank=True)
    next_of_kin_phone = models.CharField(max_length=60, blank=True)
    balance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.acc_num


class Voucher(models.Model):
    num = models.CharField(max_length=60, unique=True)
    value = models.IntegerField(default=0)
    used = models.BooleanField(default=False)
    account = models.ForeignKey(Account, related_name='voucher_account', null=True, blank=True, default=None)

    def __unicode__(self):
        return self.num


class Member(models.Model):
    username = models.CharField(primary_key=True, max_length=10)
    password = models.CharField(max_length=8)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=70, blank=True)
    phone = models.CharField(max_length=60, null=False, blank=False)
    nationality = models.CharField(max_length=90, null=True, blank=True)
    address = models.CharField(max_length=150, blank=True)
    account = models.ForeignKey(Account, related_name='member_account', null=True, blank=True, default=None)
    mem_types = (
        ('m', 'manager'),
        ('a', 'agent'),
        ('c', 'client')
    )
    role = models.CharField(max_length=1, choices=mem_types)

    def __unicode__(self):
        return self.username


admin.site.register(Member)
admin.site.register(Account)
admin.site.register(Voucher)



