from time import perf_counter as pfc
import itertools as itt


def prüfe_machbarkeit(hinweise):
  return sum([sum(s) for s in hinweise[0]]) == sum([sum(z) for z in hinweise[1]])


def permutation(einträge, länge):
  permutationen = []
  anz_blöcke = len(einträge)
  anz_leer = länge-sum(einträge)-anz_blöcke+1
  for v in itt.combinations(range(anz_blöcke+anz_leer), anz_blöcke):
    v = [v[0]]+[b-a for a,b in zip(v,v[1:])]
    p= ''.join(['2'*pos+'1'*einträge[i] for i,pos in enumerate(v)])
    p+='2'*(anz_leer)
    permutationen.append(p[:länge])
  return permutationen
  

def prüfe_gültigkeit(perm, i, typ):
  vergleich = grid[i] if typ == 0 else [grid[y][i] for y in range(höhe)]
  if all(e == '0' for e in vergleich): return perm
  gültig = []
  for p in perm:
    if not all(vergleich[n] == '0' or vergleich[n] == e  
               for n, e in enumerate(p)):
      continue
    gültig.append(p)
  return gültig


def showGrid(grid):
  for zeile in grid:
    print(' '.join(['?# '[int(c)] for c in zeile]))
  print()


def probleme_einlesen(datei):
  probleme = []
  with open(datei) as f:
    for problem in f.read().split('\n\n'):
      probleme.append([[[ord(c)-64 for c in e] for e in hv.split()]
                       for hv in problem.split('\n')])
  return probleme


def solve(hinweise):
  verlauf = {}
  
  änderung = True
  while änderung:
    änderung = False
    for vh, h in enumerate(hinweise):
      größe = höhe if vh == 1 else breite
      for i, e in enumerate(h):
        permutations = verlauf[(vh,i)] if (vh,i) in verlauf else permutation(e,größe)
        gültig = prüfe_gültigkeit(permutations, i, vh)
        verlauf[(vh,i)] = gültig
        treffer = [all(e[0] == n for n in e) for e in zip(*gültig)]
        for i2, t in enumerate(treffer):
          if not t: continue
          if vh == 0:
            x, y = i2, i
          else:
            x, y = i, i2
          if grid[y][x] == '0':
            grid[y][x] = gültig[0][i2]
            änderung = True
  return grid

H, V = 0, 1
probleme = probleme_einlesen('Teil_xx_Nonogram_problems.txt')

for hinweise in probleme:
  start = pfc()
  breite, höhe = len(hinweise[V]), len(hinweise[H])
  print(f'Breite = {breite}, Höhe = {höhe}')
  grid = [['0']*breite for _ in range(höhe)]

  if not prüfe_machbarkeit(hinweise):
    print('Sorry. Dieses Nonogramm ist feherhaft und kann nicht gelöst werden')
    exit()

  showGrid(solve(hinweise))
  print(pfc()-start)