from rest_framework.permissions import BasePermission, SAFE_METHODS


HTTP_METHODS = ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE',)


class IsOwner(BasePermission):
    def __init__(self, admin_methods: tuple = HTTP_METHODS, attrs: tuple = ('author',), other_can_read: bool = True, all_attrs: bool = True):
        self.admin_methods = admin_methods
        self.attrs = attrs
        self.other_can_read = other_can_read
        self.all_attrs = all_attrs

    def __call__(self, *args, **kwargs):
        return self

    def has_object_permission(self, request, view, obj):
        attrs = [getattr(obj, attr) == request.user for attr in self.attrs]
        attrs_bool = all(attrs) if self.all_attrs else any(attrs)
        return bool(
            (request.method in SAFE_METHODS if self.other_can_read else False) or
            (attrs_bool if self.attrs else obj == request.user) or
            (request.user.is_staff and request.method in self.admin_methods)
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )