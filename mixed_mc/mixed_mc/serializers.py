from django.db.models import fields
from django.db.models import query
from django.db.models.query import QuerySet
from django.db.models import Q
from rest_framework import serializers, viewsets, routers
from rest_framework.response import Response

from model.models import System, Alter, Account, Message, ChatRoom, ChatRoomMembers, People

router = routers.DefaultRouter()

def router_register(route, basename=None):
    def set_in_router(cls):
        router.register(route, cls, basename=basename)
        return cls
    return set_in_router



class AlterSerializer_Solo(serializers.ModelSerializer):
    class Meta:
        model = Alter
        fields = ["id", "system", "name", "age", "profile_picture"]

class AlterSerializer_asMember(serializers.ModelSerializer):
    class Meta:
        model = Alter
        fields = ["id","name", "age", "profile_picture"]

class SystemSerializer(serializers.ModelSerializer):
    alters = AlterSerializer_asMember(many=True, read_only=True, source="alter_set")
    class Meta:
        model = System
        fields = ["name", "alters", "account"]

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "display_name", "user", "profile_picture"]

class ChatRoomMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoomMembers
        fields = ["account", "chatroom"]


class ChatRoomMembersSerializer_asMember(serializers.ModelSerializer):
    account = AccountSerializer(many=False, read_only=True)
    class Meta:
        model = ChatRoomMembers
        fields = ["account"]

class ChatRoomSerializer(serializers.ModelSerializer):
    members = ChatRoomMembersSerializer_asMember(many=True, read_only=True, source="chatroommembers_set")
    class Meta:
        model = ChatRoom
        fields = ["id", "name", "members"]

class PeopleSerializer(serializers.ModelSerializer):
    # account = AccountSerializer()
    # alter   = AlterSerializer_asMember()
    class Meta:
        model = People
        fields = ["id", "account", "alter"]

class PeopleSerializer_full(serializers.ModelSerializer):
    account = AccountSerializer()
    alter   = AlterSerializer_asMember()
    class Meta:
        model = People
        fields = ["id", "account", "alter"]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chatroom", "author", "created_at", "body"]


class GetMessageSerializer(serializers.ModelSerializer):
    read_only = True
    author = PeopleSerializer_full(many=False, read_only=True)
    class Meta:
        model = Message
        fields = ["id", "chatroom", "author", "created_at", "body"]


@router_register(r"chatroom-members")
class ChatRoomViewset(viewsets.ModelViewSet):
    queryset = ChatRoomMembers.objects.all()
    serializer_class = ChatRoomMembersSerializer

@router_register(r"chatroom")
class ChatRoomViewset(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


@router_register(r"get_message", basename="get_message")
class GetMessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = GetMessageSerializer

    def list(self, request, *args, **kwargs):
        query = Message.objects.all()
        if "chatroom" in request._request.GET:
            chatroom_id = request._request.GET["chatroom"]
            query = Message.objects.filter(chatroom_id=chatroom_id).all()
        ret = self.get_serializer(query, many=True)
        return Response(data=ret.data)


@router_register(r"people")
class PeopleViewset(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    def list(self, request, *args, **kwargs):
        query = People.objects.all()
        if "accounts" in request._request.GET:
            accounts = request._request.GET["accounts"].split(',')
            accounts = list(map(int, accounts))
            fltr = Q(account_id=accounts[0])
            for i in range(1, len(accounts)):
                fltr = fltr | Q(account_id=accounts[i])
            query = People.objects.filter(fltr).all()
        ret = self.get_serializer(query, many=True)
        return Response(data=ret.data)

@router_register(r"get_people")
class GetPeopleViewset(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer_full
    def list(self, request, *args, **kwargs):
        query = People.objects.all()
        if "accounts" in request._request.GET:
            accounts = request._request.GET["accounts"].split(',')
            accounts = list(map(int, accounts))
            fltr = Q(account_id=accounts[0])
            for i in range(1, len(accounts)):
                fltr = fltr | Q(account_id=accounts[i])
            query = People.objects.filter(fltr).all()
        ret = self.get_serializer(query, many=True)
        return Response(data=ret.data)

@router_register(r"message")
class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

@router_register(r"accounts")
class AccountViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

@router_register(r"alters")
class AlterViewset(viewsets.ModelViewSet):
    queryset = Alter.objects.all()
    serializer_class = AlterSerializer_Solo

@router_register(r"systems")
class SystemViewset(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
