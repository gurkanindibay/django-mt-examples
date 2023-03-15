from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from tutorial.quickstart.serializers import (
    UserSerializer,
    GroupSerializer,
    AccountSerializer,
    ProjectSerializer,
)
from .models import Account, Project


from django_multitenant import views
from django_multitenant.views import TenantModelViewSet




def tenant_func(request):
    return Account.objects.filter(user=request.user).first()


views.get_tenant = tenant_func

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    print("UserViewSet executed")
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    print("GroupViewSet executed")
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



class AccountViewSet(TenantModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    model_class = Account
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(TenantModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    model_class = Project
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]



from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST"])
def account_list(request):
    """
    List all Accounts, or create a new account.
    """
    if request.method == "GET":
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
