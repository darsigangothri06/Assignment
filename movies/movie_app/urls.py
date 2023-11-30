#django imports
from django.urls import path

#rest framework imports
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

#local imports
from .api import RegisterApi, MovieView, CollectionsView

print('hello')

urlpatterns = [
    path('register', RegisterApi.as_view()),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('movie',MovieView.as_view(), name='movie'),
]

#default router
router = DefaultRouter()
router.register(r'collection', CollectionsView, basename='collection')
urlpatterns += router.urls