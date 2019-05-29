from django.db import models
from jsonfield import JSONField

# Create your models here.



class Provider(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone= models.CharField(max_length=50)
    language= models.CharField(max_length=100)
    currency=models.CharField(max_length=10)


    def __str__(self):
        values= self.name + " " + str(self.email) +  " " + str(self.phone) + " " + self.language +  " " + self. currency +  " " + str(self.id)
        return (values) 

    def setattr (self,field, value):
    	self.field= value 





class Polygon(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price=models.FloatField()
    geojson=JSONField()

    def setattr (self,field, value):
    	self.field= value 
    
    def __str__(self):
        return self.name