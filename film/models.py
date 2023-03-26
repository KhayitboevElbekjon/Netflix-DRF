from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,ValidationError
from django.db import models
def validate_davlat(qiymat):
    davlatlar=["O'zbekiston",'AQSH','Xitoy','Yaponiya','Rossiya','Angliya',"Qozog'iston"]
    if qiymat not in davlatlar:
        raise ValidationError("Bu davlatlardan aktyor kiritish mumkun emas!")
class Aktyor(models.Model):
    ism=models.CharField(max_length=50)
    tugulgan_yil=models.DateField()
    jins=models.CharField(max_length=5)
    davlat=models.CharField(max_length=50,validators=[validate_davlat])
    def __str__(self):
        return self.ism
class Kino(models.Model):
    nom=models.CharField(max_length=50)
    yil=models.DateField()
    janr=models.CharField(max_length=70)
    aktyor_fk=models.ManyToManyField(Aktyor)
    def __str__(self):
        return self.nom
class Tarif(models.Model):
    nom=models.CharField(max_length=50)
    narx=models.IntegerField(validators=[MinValueValidator(3)])
    muddat=models.CharField(max_length=30)
    def __str__(self):
        return self.nom
class Izoh(models.Model):
    user_fk=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    kino_fk=models.ForeignKey(Kino,on_delete=models.CASCADE)
    vaqt=models.DateField()
    matn=models.TextField()
    def __str__(self):
        return f"{self.user_fk},{self.kino_fk}"
