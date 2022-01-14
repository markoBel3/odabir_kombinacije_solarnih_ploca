import constraint
import sys
import math

problem = constraint.Problem()
# ulazni argumenti: 45 0 tip_1 tip_2 tip_3 170 335.39 930 10 40 180 0.089 0.33 0.98
# krov je 45m2
# solarna ploca A: 170kn, 10W, 0.089m2
# solarna ploca B: 335.49kn, 40W, 0.33m2
# solarna ploca C: 930kn, 180W, 0.98m2
krov = 0.0
max_cijena = 0.0
lista_imena = []
dict_cijena = {}
dict_watta = {}
dict_velicine = {}

def obradi_ulaz():
    broj_ploca = int((len(sys.argv)-3)/4)
    global krov
    global max_cijena
    krov = float(sys.argv[1])
    max_cijena = float(sys.argv[2])
    for i in range(3,broj_ploca+3):
        lista_imena.append(sys.argv[i])
        dict_cijena[sys.argv[i]] = float(sys.argv[i+broj_ploca])
        dict_watta[sys.argv[i]] = float(sys.argv[i+(broj_ploca*2)])
        dict_velicine[sys.argv[i]] = float(sys.argv[i+(broj_ploca*3)])

def izracunaj_ogranicenja(kljuc):
    if max_cijena != 0:
        return math.floor(min([max_cijena/dict_cijena[kljuc],krov/dict_velicine[kljuc]]))
    else:
        return math.floor(krov/dict_velicine[kljuc])

def dodaj_varijable():
    for ploca in lista_imena:
        # print("ploca: ", ploca, " , max: ", izracunaj_ogranicenja(ploca))
        problem.addVariable(ploca, range(izracunaj_ogranicenja(ploca)))

def ogranicenje_velicine(*args):
    zbroj = 0
    global krov
    broj_arg = len(args)
    for i in range(broj_arg):
        zbroj = zbroj + (args[i]*dict_velicine[lista_imena[i]])
    if zbroj <= krov:
        return True

def ogranicenje_cijene(*args):
    zbroj = 0
    global max_cijena
    broj_arg = len(args)
    for i in range(broj_arg):
        zbroj = zbroj + (args[i]*dict_cijena[lista_imena[i]])
    if zbroj <= max_cijena:
        return True

obradi_ulaz()
dodaj_varijable()
# print(krov)
# print(max_cijena)
# print(lista_imena)
# print(dict_cijena)
# print(dict_velicine)
#print(dict_watta)

problem.addConstraint(ogranicenje_velicine, lista_imena)
if max_cijena != 0:
    problem.addConstraint(ogranicenje_cijene, lista_imena)

def evaluacija(rjesenje):
    zbroj = 0
    for k,v in rjesenje.items():
        zbroj = zbroj + v * dict_watta[k]
    return zbroj

def evaluacija_cijena(rjesenje):
    zbroj = 0
    for k,v in rjesenje.items():
        zbroj = zbroj + v * dict_cijena[k]
    return zbroj

def evaluacija_velicina(rjesenje):
    zbroj = 0
    for k,v in rjesenje.items():
        zbroj = zbroj + v * dict_velicine[k]
    return zbroj

rjesenje = {}
rjesenja = problem.getSolutions()

max_watta = 0
for r in rjesenja:
    if evaluacija(r) > max_watta:
        max_watta = evaluacija(r)
        rjesenje = r

print("Najviše kwh ce doprinjet ova kombinacija ploca:")
for ploca in lista_imena:
    print(rjesenje[ploca]," ",ploca," ploca")
print("Zauzet ce ", round(evaluacija_velicina(rjesenje),4), "m2")
print("Kostat ce ", round(evaluacija_cijena(rjesenje),2), "kn")
print(round(max_watta/1000,3), "kWh")

# print("""
# Najviše kwh ce doprinjeti ova kombinacija ploca:
# {} A ploca,
# {} B ploca,
# {} C ploca
# Zauzet ce {} m2
# Kostat ce {} kn
# """.format(rjesenje['A'], rjesenje['B'], rjesenje['C'], evaluacija_velicina(rjesenje), evaluacija_cijena(rjesenje)))