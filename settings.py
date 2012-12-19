import os
#configure applications vars

#Scraper

DIPUTADOS_URL = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DiputadosLegFechas"
VOTACIONES_URL = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Actualidad/Votaciones?_piref73_9564074_73_9536063_9536063.next_page=/wc/accesoHistoricoVotaciones&fechaSeleccionada="
DATABASE = "colibri_db"


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
