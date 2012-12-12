from mongoengine import *

class Diputado(Document):
       nombre = StringField()
       apellidos = StringField()
       ficha = URLField()
       correo = EmailField()
       baja = DateTimeField()
       sustituto = StringField()
       web = URLField()
       twitter = URLField()
       partido = StringField()
       circunscripcion = StringField()
       asiento = StringField()
