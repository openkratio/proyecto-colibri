from mongoengine import *

class Grupo(EmbeddedDocument):
    nombre = StringField()

class Partido(EmbeddedDocument):
    nombre = StringField()
    color = StringField()
    grupo = EmbeddedDocumentField('Grupo')
