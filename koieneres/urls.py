"""koieneres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from reservations import views
from users import views as userviews
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework_swagger.views import get_swagger_view

jwt_urlpatterns = [
    url(r'^token-auth/$', obtain_jwt_token, name='obtain_jwt_token'),
    url(r'^token-auth/refresh/$', refresh_jwt_token, name='refresh_jwt_token'),
    url(r'^token-auth/verify/$', verify_jwt_token, name='verify_jwt_token'),
]

authorization_urlpatterns = [
    url(r'', include((jwt_urlpatterns, 'jwt'), namespace='jwt')),
]

router = routers.DefaultRouter()
router.register(
    r'create-reservation',
    views.CreateReservationViewSet,
    base_name='create-reservation')
router.register(
    r'publicreservationdata',
    views.PublicReservationDataViewSet,
    base_name='publicresdata')
router.register(
    r'reservationdata', views.ReservationDataViewSet, base_name='resdata')
router.register(r'status', views.StatusViewSet, base_name='status')
router.register(
    r'reservation-period',
    views.ReservationPeriodViewSet,
    base_name='res-period')
router.register(
    r'current-user', userviews.CurrentUserViewSet, base_name='current-user')

router.register(
    r'cabin-closings', views.CabinClosingViewSet, base_name='cabin-closings')

urlpatterns = [
    url('^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^authorization/', include(authorization_urlpatterns)),
    url(r'^swagger/', get_swagger_view(title='Koieneres API'))
]
