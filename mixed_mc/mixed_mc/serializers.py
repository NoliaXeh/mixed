from django.db.models import fields
from rest_framework import serializers, viewsets, routers

from model.models import System, Alter

class AlterSerializer_Solo(serializers.ModelSerializer):
    class Meta:
        model = Alter
        fields = ["system", "name", "age"]


class AlterSerializer_asMember(serializers.ModelSerializer):
    class Meta:
        model = Alter
        fields = ["name", "age"]

class SystemSerializer(serializers.ModelSerializer):
    alters = AlterSerializer_asMember(many=True, read_only=True, source="alter_set")
    class Meta:
        model = System
        fields = ["name", "alters", "account"]




class AlterViewset(viewsets.ModelViewSet):
    queryset = Alter.objects.all()
    serializer_class = AlterSerializer_Solo

class SystemViewset(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer

router = routers.DefaultRouter()
router.register(r'systems', SystemViewset)
router.register(r'alters', AlterViewset)