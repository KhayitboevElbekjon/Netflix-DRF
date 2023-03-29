from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# status codda xatolik kodini chiqarib beradi
from .serializers import *
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import status,filters
class HelloAPIView(APIView):
    def get(self,request):
        content={
            "xabar":"Salom dunyo"
        }
        return Response(content)
    def post(self,request):
        data=request.data
        content={
            'xabar':"Ma'lumot qo'shildi",
            'malumot':data
        }
        return Response(content)
class AktyorAPIView(ModelViewSet):
    queryset=Aktyor.objects.all()
    serializer_class=AkyorSerializer
    def get_queryset(self):
        name=self.request.query_params.get('qidirish')
        if name is None or name =='':
            natija=Aktyor.objects.all()
        else:
            natija=Aktyor.objects.filter(ism__contains=name)
        return natija

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ('tugulgan_yil', )
#     def get(self,request):
#         akyorlar=Aktyor.objects.all()
#         serializer=AkyorSerializer(akyorlar,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         aktyor=request.data
#         seralizer=AkyorSerializer(data=aktyor)
#         if seralizer.is_valid():
#             Aktyor.objects.create(
#                 ism=seralizer.validated_data.get('ism'),
#                 tugulgan_yil=seralizer.validated_data.get('tugulgan_yil'),
#                 jins=seralizer.validated_data.get('jins'),
#                 davlat=seralizer.validated_data.get('davlat')
#             )
#             return Response(seralizer.data,status=status.HTTP_201_CREATED)
#         return Response(seralizer.errors,status=status.HTTP_400_BAD_REQUEST)  # agar kiritilgan data xato bolsa xatoni korsatadi
#
# class AktyorDetailView(APIView):
#     def get(self,request,son):
#         akyorlar = Aktyor.objects.get(id=son)
#         serializer=AkyorSerializer(akyorlar)
#         return Response(serializer.data)
#     def put(self,request,son):
#         aktyor=Aktyor.objects.get(id=son)
#         serializer=AkyorSerializer(aktyor,data=request.data)  # data=request.data yangi malumoti
#         if serializer.is_valid():
#             aktyor.ism=serializer.validated_data.get('ism')
#             aktyor.davlat=serializer.validated_data.get('davlat')
#             aktyor.save()
#             return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class TarifAPIView(APIView):
    def get(self,request):
        tarif=Tarif.objects.all()
        seralizer=TarifSerializer(tarif,many=True)
        return Response(seralizer.data)
    def post(self,request):
        tarif=request.data
        serializers=TarifSerializer(data=tarif)
        if serializers.is_valid():
            Tarif.objects.create(
                nom=serializers.validated_data.get('nom'),
                narx=serializers.validated_data.get('narx'),
                muddat=serializers.validated_data.get('muddat'),
            )
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_CREATED)

class TaifDetailView(APIView):
    def delete(self,request,pk):
        tt=Tarif.objects.filter(id=pk)
        tt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put(self,request,pk):
        tarif=Tarif.objects.get(id=pk)
        serializers=TarifSerializer(tarif,data=request.data)
        if serializers.is_valid():
            tarif.nom=serializers.validated_data.get('nom')
            tarif.narx=serializers.validated_data.get('narx')
            tarif.muddat=serializers.validated_data.get('muddat')
            tarif.save()
            return Response(serializers.data,status.HTTP_202_ACCEPTED)
        return Response(serializers.errors,status.HTTP_400_BAD_REQUEST)

# class KinoAPIView(APIView):
#     def get(self,request):
#         kino=Kino.objects.all()
#         serializer = KinoSerializer(kino, many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         kino=request.data
#         serializer=KinoCreateSerializer(data=kino)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
# class KinoDetailView(APIView):
#     def put(self,request,pk):
#         kino=Kino.objects.get(id=pk)
#         serializer=KinoCreateSerializer(kino,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class KinoModelViewset(ModelViewSet):
    queryset=Kino.objects.all()
    serializer_class=KinoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ('yil', )
    search_fields=('nom',)

    # @action(detail=True)
    # def aktyorlar(self,request,pk):  # kinolar/3/aktyorlar
    #     aktor=Kino.objects.get(id=pk).aktyor_fk.all()
    #     serializer=AkyorSerializer(aktor,many=True)
    #     return Response(serializer.data)

class IzohModelViewSet(ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Izoh.objects.all()
    serializer_class=IzohSerializer

    def perform_create(self,serializer):
        serializer.save(user=self.request.uzer)
        return Response(serializer.data)

    def perform_destroy(self,instance):
        if instance.uzer==self.request.user:
            serializer=self.get_serializer(instance)
            if serializer.is_valid():
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)