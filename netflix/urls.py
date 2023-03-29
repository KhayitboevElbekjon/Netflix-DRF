
from django.contrib import admin
from django.urls import path,include
from film.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('kinolar',KinoModelViewset)
router.register('izohlar',IzohModelViewSet)
router.register('aktyorlar',AktyorAPIView)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',HelloAPIView.as_view()),
    # path('akyorlar/',AktyorAPIView.as_view()),
    # path('detal/<int:son>',AktyorDetailView.as_view()),
    path('tarif/',TarifAPIView.as_view()),
    path('tarif_det/<int:pk>',TaifDetailView.as_view()),
    path('get_token/', obtain_auth_token),
    path('',include(router.urls))
    # path('kinolar/',KinoAPIView.as_view()),
    # path('kinolar/<int:pk>',KinoDetailView.as_view()),
]
