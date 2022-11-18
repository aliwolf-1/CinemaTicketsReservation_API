from rest_framework import serializers
from tickets.models import Guest, Movie, Reservation

class MovieSerilalizer(serializers.ModelSerializer):
    class Meta:
        model   = Movie
        fields  = '__all__'

class ReservationSerilalizer(serializers.ModelSerializer):
    class Meta:
        model   = Reservation
        fields  = '__all__'
class GusetSerilalizer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk', 'reservation', 'name' , 'mobile']