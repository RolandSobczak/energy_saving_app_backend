from django.contrib.auth import get_user_model
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from djoser.views import UserViewSet as DjoserUserViewSet
from text_chat.models import Invite

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=True, methods=('post',), permission_classes=(IsAuthenticated,))
    def invite(self, request, *args, **kwargs):
        recipient_user = self.get_object()
        object = Invite.objects.filter(from_user=request.user, recipient_user=recipient_user)
        object.all()
        if object.exists() and object.last().accepted is None:
            return Response({'error': 'You already sent invite to this user'}, status=HTTP_403_FORBIDDEN)
        Invite.objects.create(from_user=request.user, recipient_user=recipient_user)
        return Response({'details': 'Invite sent'}, status=HTTP_201_CREATED)



