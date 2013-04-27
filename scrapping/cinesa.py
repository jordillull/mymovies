#!/usr/bin/python 
# -*- coding: UTF-8 -*-
import urllib2
import json
from datetime import date
from bs4 import BeautifulSoup 
ARTEA = 260
AS_CANCELAS = 1200 
AUGUSTA = 200
BAHIA_SANTANDER = 270
BARNASUD = 1037
BONAIRE = 721
CAPITOL = 1027
DIAGONAL = 120
DIAGONAL_MAR = 232
EL_FORO =  250
EL_MUELLE = 761
EQUINOCCIO = 631
FESTIVAL_PARK = 234
GRANCASA = 611
HERON_CITY_BARCELONA = 291
LA_CANADA = 280
LA_FARGA = 113
LA_GAVIA = 1039
LA_MAQUINISTA = 661
LA_MORALEJA = 601
LAS_ROSAS = 196
LAS_ROZAS_HERON_CITY = 236
LORANCA = 192
LOS_BARRIOS = 1054
MANOTERAS = 1052
MAREMAGNUM = 112
MARINEDA_CITY = 1047
MATARO_PARC = 275
MAX_OCIO = 1056
MENDEZ_ALVARO = 1050 
NASSICA = 1051
NUEVA_CONDOMINA = 1033
PARC_VALLES = 231
PARQUE_PRINCIPADO = 701
PARQUESUR = 190
PLAZA_DE_ARMAS = 651
PRINCIPE_PIO = 781
PROYECCIONES = 331
PUERTO_VENECIA = 1100
SANT_CUGAT = 110
SIETE_PALMAS = 741
XANADU = 311
ZARATAN = 1053
ZUBIARTE = 1055

URL="http://www.cinesa.es/Cines/horariosPorDia/"



def listing(area=FESTIVAL_PARK, day=False, verbose=False):
  def v(str):
    if verbose:
      print str       
      
  soup = BeautifulSoup(urllib2.urlopen(URL+str(area))) 
  
  if not day:
    day = date.today().strftime("%d/%m")
    
  for row in soup.find_all(id="parrilla_horarios"):
    if day in row.parent()[0].contents[0]:
      listing = row
      break 
    
  results = []
  for movie in listing.find_all("li", "n_peli"):
    result = {}
    result['title'] = movie.find("div","wrapper_peli").getText()
    result['sessions'] = []
    v(result['title'])
    for type in movie.find("ul","t_session").find_all("li", recursive=False):
      type_name = type.find("div","t_nombre").getText()
      session = {}
      session['type'] = type_name
      session['times'] = []
      v("##"+type_name)
      for room in type.find("ul", "n_sala").find_all("li", recursive=False): 
        room_name = room.find("div","wrapper_sala").getText()
        times = []
        v("----"+room_name)
        for hour in room.find("ul", "horas").find_all("li", recursive=False):
          v("......"+hour.getText())
          times.append(hour.getText())
        session['times'].append({'room' : room_name, 'times' : times})
      result['sessions'].append(session)
    results.append(result)
  
  return results

if __name__ == "__main__":
  l = listing(FESTIVAL_PARK)
  print json.dumps(l, indent=2)
