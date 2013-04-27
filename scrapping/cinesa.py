#!/usr/bin/python 
# -*- coding: UTF-8 -*-
import urllib2
import json
from datetime import date
from bs4 import BeautifulSoup 
URL="http://www.cinesa.es/Cines/horariosPorDia/234/0"



def listing(day=False, verbose=False):
  def v(str):
    if verbose:
      print str       
      
  soup = BeautifulSoup(urllib2.urlopen(URL)) 
  
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
        v("----"+room_name)
        for hour in room.find("ul", "horas").find_all("li", recursive=False):
          v("......"+hour.getText())
          session['times'].append({'room' : room_name, 'time' : hour.getText()})
      result['sessions'].append(session)
    results.append(result)
  
  return results

if __name__ == "__main__":
  l = listing()
  print json.dumps(l, indent=2)
