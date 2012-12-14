import sys
import xml.etree.ElementTree as ET

def main(file):
	tree = ET.parse(file)
	root = tree.getroot()
	
	resumen = root.find('Informacion')
	print 'Sesion:', resumen.find('Sesion').text
	print 'Numero de votacion:', resumen.find('NumeroVotacion').text
	print 'Fecha:', resumen.find('Fecha').text
	print 'Titulo:', resumen.find('Titulo').text
	print 'Texto Expediente:', resumen.find('TextoExpediente').text
	print 'Titulo SubGrupo:', resumen.find('TituloSubGrupo').text
	print 'Texto SubGrupo:', resumen.find('TextoSubGrupo').text
	
	totales = root.find('Totales')
	asentimiento = totales.find('Asentimiento').text
	if asentimiento == 'No':
		print 'SE VOTA:'
		print '--------------'
		print 'Presentes:', totales.find('Presentes').text
		print 'A favor:', totales.find('AFavor').text
		print 'En contra:', totales.find('EnContra').text
		print 'No votan:', totales.find('NoVotan').text
		votaciones = root.find('Votaciones')
		for voto in votaciones:
			print '\t', voto.find('Asiento').text, voto.find('Diputado').text, voto.find('Voto').text
		print 'Numero de votaciones', len(votaciones)
	else:
		print 'SE ASIENTE'



if __name__ == '__main__':
	main(sys.argv[1])