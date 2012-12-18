import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.partido import Partido
from mongoengine import *

class Asiento(EmbeddedDocument):
    imagen = StringField()

class Diputado(Document):
    nombre = StringField()
    apellidos = StringField()
    ficha = URLField()
    correo = EmailField()
    baja = DateTimeField()
    sustituto = StringField()
    web = URLField()
    twitter = URLField()
    partido = EmbeddedDocumentField('Partido')
    circunscripcion = StringField()
    asiento = EmbeddedDocumentField('Asiento')
