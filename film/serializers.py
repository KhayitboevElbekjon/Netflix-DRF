from rest_framework import serializers
from .models import *

class AkyorSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    ism=serializers.CharField(max_length=50)
    tugulgan_yil=serializers.DateField()
    jins=serializers.CharField(max_length=5)
    davlat=serializers.CharField(max_length=50)

    def validate_ism(self,qiymat):
        if len(qiymat)<3:
            raise serializers.ValidationError('Ism bunaqa kalta bo\'lmaydi')
        return qiymat
    def validate_jins(self,qiymat):
        if qiymat!='Erkak' and qiymat!='Ayol':
            raise serializers.ValidationError("Siz noto'g'ri jins kiritdingiz")
        return qiymat
class TarifSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nom=serializers.CharField(max_length=50)
    narx=serializers.IntegerField()
    muddat=serializers.CharField(max_length=30)

class KinoSerializer(serializers.ModelSerializer): # Bu esa put,patch uchun ishlashi mumkun
    aktyor_fk=AkyorSerializer(many=True)
    class Meta:
        model=Kino
        fields='__all__'

class KinoCreateSerializer(serializers.ModelSerializer):  # Bu qo'shish uchun serializer

    class Meta:
        model=Kino
        fields='__all__'

class IzohSerializer(serializers.ModelSerializer):
    class Meta:
        model=Izoh
        fields='__all__'