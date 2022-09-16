from django.contrib.auth import get_user_model
from rest_framework import filters
from djoser.views import UserViewSet as DjoserUserViewSet

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)



