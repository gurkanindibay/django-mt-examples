from django.db import models

# Create your models here.
from django.contrib.auth.models import User

import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


from django_multitenant.mixins import TenantModelMixin, TenantManagerMixin
from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey


class Country(models.Model):
    name = models.CharField(max_length=255)


class Account(TenantModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    tenant_id = "id"

    def __str__(self):
        return "{}".format(self.name)



class Manager(TenantModel):
    name = models.CharField(max_length=255)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="managers"
    )
    tenant_id = "account_id"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id', 'account_id'], name='unique_manager_account')
        ]


class Project(TenantModel):
    name = models.CharField(max_length=255)
    account = models.ForeignKey(
        Account, related_name="projects", on_delete=models.CASCADE
    )
    managers = models.ManyToManyField(Manager, through="ProjectManager")
    tenant_id = "account_id"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id', 'account_id'], name='unique_project_account')
        ]


    def __str__(self):
        return "{} ({})".format(self.name, self.account)


class ProjectManager(TenantModel):
    project = TenantForeignKey(
        Project, on_delete=models.CASCADE, related_name="projectmanagers"
    )
    manager = TenantForeignKey(Manager, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    tenant_id = "account_id"
