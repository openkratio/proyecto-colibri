from mongoengine import *

class Diputado(Document):
       nombre = StringField(max_length=50, required=True)
       apellidos = StringFIeld(max_length=100, required=True)
       ficha = URLField()
       correo = EmailField(required=True)
       baja = DateTimeField()
       sustituto = StrinField()
       web = URLField()
       twitter = URLFIeld()
       partido = StringField()
       circunscripcion = StringField()
       asiento = StringField()
