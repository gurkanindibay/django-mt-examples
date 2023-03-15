from django_multitenant.utils import set_current_tenant
from django_multitenant.models import TenantModel
from rest_framework import viewsets


def get_tenant(request):
    pass


class TenantModelViewSet(viewsets.ModelViewSet):
    model_class = TenantModel


    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.model_class.objects.none()
        account = get_tenant(self.request)
        set_current_tenant(account)
        return self.model_class.objects.all()