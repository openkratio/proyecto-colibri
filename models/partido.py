from mongoengine import *

class Grupo(EmbeddedDocument):
    nombre = StringField()
    acronimo = StringField()

class Partido(EmbeddedDocument):
    nombre = StringField()
    color = StringField()
    logo = StringField()
    web = URLField()
    grupo = EmbeddedDocumentField('Grupo')
