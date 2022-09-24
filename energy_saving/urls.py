from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('organisations', views.OrganisationViewSet, 'organisations')
router.register('localisations', views.LocalisationViewSet, 'localisations')
router.register('rooms', views.RoomViewSet, 'rooms')
router.register('device-types', views.DeviceTypeViewSet, 'device-types')
router.register('devices', views.DeviceViewSet, 'devices')
# router.register('devices/<pk>/month/<date>', views.MonthViewSet, 'months')
# router.register('days', views.DayViewSet, 'days')

month_router = routers.NestedDefaultRouter(router, r'devices', lookup='device')
month_router.register(r'month', views.MonthViewSet, basename='device-month')
month_router.register(r'day', views.DayViewSet, basename='device-day')


app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(month_router.urls)),
    path('specs/<str:url>/', views.SpecsFetchView.as_view()),
]