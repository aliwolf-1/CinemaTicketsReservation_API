from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GusetSerilalizer, MovieSerilalizer, ReservationSerilalizer
from rest_framework import status , filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics , mixins , viewsets

# Create your views here.

#1
def no_rest_no_model(requset):
    guests = [
        {
            'id' : 1,
            'name' : 'ali',
            'mobile' : 927738783,
        },
        {
            'id' : 2,
            'name' : 'kado',
            'mobile' : 454390934,
        }
    ]
    return JsonResponse (guests, safe=False)

#2
def no_rest_from_model(requset):
    date = Guest.objects.all()
    response = {
        'guests': list(date.values('name', 'mobile'))
    }
    return JsonResponse(response)
#__________________________________________________________

#3 Function based views
#3.1 GET POST
@api_view(['GET','POST'])
def FBV_List(requset):
    #GET
    if requset.method == 'GET':
        guests = Guest.objects.all()
        serializer = GusetSerilalizer(guests , many=True)
        return Response(serializer.data)
    #POST
    elif requset.method == 'POST':
        serializer = GusetSerilalizer(data= requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_PK(requset , pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #GET
    if requset.method == 'GET':
        serializer = GusetSerilalizer(guest)
        return Response(serializer.data)
    #PUT
    elif requset.method == 'PUT':
        serializer = GusetSerilalizer(data= requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    #DELETE
    if requset.method == 'DELETE':
        guest.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
       
#___________________________________________________________

# CVB Class based views
#4.1 List and Create == GET and POST
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GusetSerilalizer(guests, many = True)
        return Response(serializer.data)
    def post(self, requset):
        serializer = GusetSerilalizer(data = requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
            status=status.HTTP_201_CREATED
            )
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
#4.2 GET PUT DELETE 
class CBV_PK(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self , request , pk):
        guest = self.get_object(pk)
        serializer = GusetSerilalizer(guest)
        return Response(serializer.data)
    def put(self , request , pk):
        guest = self.get_object(pk)
        serializer = GusetSerilalizer(guest , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 
        status= status.HTTP_400_BAD_REQUEST
        )
    def delete(self , request , pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      
#____________________________________________________________

#5.1 mixins list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerilalizer
    def get(self , request):
        return self.list(request)
    def post(self , request):
        return self.create(request)
#5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerilalizer
    def get(self , request , pk):
        return self.retrieve(request)
    def put(self , request , pk):
        return self.update(request)
    def delete(self , request , pk):
        return self.destroy(request)

#_____________________________________________________________

#GENERICS
#6.1 GET and POST Generics
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerilalizer
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GusetSerilalizer

#______________________________________________________________

#ViewSets
#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GusetSerilalizer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerilalizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_res(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerilalizer

@api_view(['GET'])
def find_movie(requset):
    movies = Movie.objects.filter(
        hall = requset.data['hall'],
        movies = requset.data['movie'],
        dates = requset.data['date'], 
    )
    serializer = MovieSerilalizer(movies , many=True)
    return Response(serializer.data)