import random as rnd
from itertools import combinations

def seite_ermitteln(auf_waage):
  seite = {nr: 0 for nr in range(anz_kugeln)}
  mitte = len(auf_waage)//2
  for nr in auf_waage:
    seite[nr] = -1 if nr in auf_waage[:mitte] else 1
  return seite

def wiegen(gesucht, seite):
  return gesucht[1] * seite[gesucht[0]]  

def statusänderung(wiegung, seite):
  for nr, status in kugeln:
    if wiegung == 0 and seite[nr] == 0:
      continue
    if (wiegung == 0 and seite[nr] != 0) or (wiegung != 0 and seite[nr] == 0):
      kugeln[nr][1] = 9
    else:
      kugeln[nr][1] = stati[wiegung == seite[nr]][status]

def int2prt(nr, status):
  return f'{nr}{ausg[status]}'


def ausgabe(liste):
  text = ''
  for nr in liste:
    text += f'{int2prt(*kugeln[nr])} '
  return text


def prüfung(v1, v2m, v2lr):
  prüfergebnisse = []
  text = ''
  for nr in range(anz_kugeln):
    gesucht = (nr, rnd.choice((-1, 1)))
    text += f'Gesucht = {int2prt(*gesucht)}\n'
    for k in kugeln: k[1] = 0

    seite = seite_ermitteln(v1)
    wiegung = wiegen(gesucht, seite)
    statusänderung(wiegung, seite)
    text += f'{wieg[wiegung]} {ausgabe(v1)} ({ausgabe(set(range(anz_kugeln)) - set(v1))})\n'

    v2 = v2m if wiegung == 0 else v2lr
    seite = seite_ermitteln(v2)
    wiegung = wiegen(gesucht, seite)
    statusänderung(wiegung, seite)
    text += f'{wieg[wiegung]} {ausgabe(v2)} ({ausgabe(set(range(anz_kugeln)) - set(v2))})\n'

    kandidaten = [k for k in kugeln if k[1] != 9]
    anz_unbek = [k[1] for k in kandidaten].count(0)
    prüfergebnisse.append(len(kandidaten) < 4 and anz_unbek < 2)
    text += f'Kandidaten = {ausgabe([k[0] for k in kandidaten])}\n\n'
  return all(prüfergebnisse), text


def alle_varianten():
  anz_lösungen = 0
  for vanz in range(1, anz_kugeln//2+1):
    for v2l in combinations(range(anz_kugeln), vanz):
      for v2r in combinations(range(anz_kugeln), vanz):
        if set(v2l) & set(v2r):
          continue
        erg, text = prüfung(v1, v2m, v2l+v2r)
        if erg:
          anz_lösungen += 1
          print(f'    LÖSUNG Nr. {anz_lösungen}, {v2l} <-> {v2r}')
          print(text)
          return
  print(anz_lösungen//2)


stati = {True:  {0: 1,  1: 1, 9: 9, -1: 9},
         False: {0: -1, -1: -1, 9: 9, 1: 9}}

ausg = {0: '?', 1: '+', -1: '-', 9: '='}
wieg = {-1: 'l', 0: 'm', 1: 'r'}

anz_kugeln = 12
kugeln = [[nr, 0] for nr in range(anz_kugeln)]
v1 = range(8)
v2m = [8,9,10,0,1,2]
alle_varianten()