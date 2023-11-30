#django imports
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
import requests

#rest framework imports
from rest_framework import viewsets, status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated

#local imports
from .serializer import RegisterSerializer, GETRetriveCollectionSerializer, POSTPUTCollectionSerializer
from movie_app.models import Collections

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        tokenRequest = TokenObtainPairSerializer().get_token(user)  
        tokenAccess = AccessToken().for_user(user)
        return Response({
            "access_token" : str(tokenAccess)
        })


class MovieView(APIView):
    print('hey movies')
    def get(self, request, *args, **kwargs):
        page_number = request.GET['page'] if 'page' in request.GET else None
        url = settings.MOVIE_API_URL if not page_number else "{}?page={}".format(settings.MOVIE_API_URL, page_number)
        user = settings.MOVIE_API_USER
        password = settings.MOVIE_USER_PASS
        movie_data = requests.get( url, auth = (user, password)).json()
        if movie_data.get('next') : movie_data['next'] = movie_data['next'].replace(url, request.build_absolute_uri((reverse('movie'))))
        if movie_data.get('previous') : movie_data['previous'] = movie_data['previous'].replace(url, request.build_absolute_uri((reverse('movie'))))
        return Response(movie_data)
    
class CollectionsView(viewsets.ViewSet):
    serializer_class = GETRetriveCollectionSerializer
    def list(self, request):
        data = Collections.objects.filter(created_by = request.user)
        serializer = self.serializer_class(data, many = True)
        return Response(serializer.data)

    def create(self, request):
        request.data['created_by'] = request.user
        serializer = POSTPUTCollectionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            resp = {"collection_uuid": serializer.data['uuid']}
            return Response(resp, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = Collections.objects.get(uuid = pk)
        serializer = self.serializer_class(data)
        return Response(serializer.data)

    def update(self, request, pk = None):
        obj = Collections.objects.get(uuid = pk)
        serializer = POSTPUTCollectionSerializer(obj, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            resp = {"message": "Record updated successfully"}
            return Response(resp, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None):
        try:
            data = Collections.objects.get(uuid = pk)
            data.delete()
            resp = {"message": "Record deleted successfully"}
            return Response(resp, status = status.HTTP_200_OK)
        except:
            resp = {"message": "No such records found.."}
        return Response(resp, status = status.HTTP_204_NO_CONTENT)


