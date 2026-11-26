# programa ventas tienda
# version final 2
import time

t = time.time()
f = open("datos/ventas_amazonfit.csv", encoding="utf-8")
d = []
for l in f.readlines():
    d.append(l.strip().split(","))
f.close()
d = d[1:]

total = 0
cont = 0
u = 0
for x in d:
    try:
        if x[9] == "Efectivo":
            total = total + int(x[7]) * float(x[8]) * 0.95
        else:
            total = total + int(x[7]) * float(x[8])
        cont = cont + 1
        u = u + int(x[7])
    except:
        pass
print("TOTAL VENTAS: " + str(cont))
print("UNIDADES: " + str(u))
print("INGRESOS: " + str(round(total, 2)))

# ventas zapatillas
d2 = d[:]
z1 = 0
for x in d2:
    try:
        if x[2] == "Zapatillas de asfalto":
            if x[9] == "Efectivo":
                z1 = z1 + int(x[7]) * float(x[8]) * 0.95
            else:
                z1 = z1 + int(x[7]) * float(x[8])
    except:
        pass
z2 = 0
for x in d2:
    try:
        if x[2] == "Zapatillas de trail":
            if x[9] == "Efectivo":
                z2 = z2 + int(x[7]) * float(x[8]) * 0.95
            else:
                z2 = z2 + int(x[7]) * float(x[8])
    except:
        pass
print("zapatillas asfalto: " + str(round(z1, 2)))
print("zapatillas trail: " + str(round(z2, 2)))

# por categoria
cats = []
for x in d:
    if x[2] not in cats:
        cats.append(x[2])
for c in cats:
    s = 0
    for x in d:
        try:
            if x[2] == c:
                if x[9] == "Efectivo":
                    s = s + int(x[7]) * float(x[8]) * 0.95
                else:
                    s = s + int(x[7]) * float(x[8])
        except:
            pass
    print(c + ": " + str(round(s, 2)))

# por mes
meses = []
for x in d:
    if x[1][0:7] not in meses:
        meses.append(x[1][0:7])
for m in meses:
    s = 0
    for x in d:
        try:
            if x[1][0:7] == m:
                if x[9] == "Efectivo":
                    s = s + int(x[7]) * float(x[8]) * 0.95
                else:
                    s = s + int(x[7]) * float(x[8])
        except:
            pass
    print(m + " -> " + str(round(s, 2)))

# top productos
p = []
for x in d:
    if x[3] not in p:
        p.append(x[3])
r = []
for i in p:
    n = 0
    for x in d:
        if x[3] == i:
            n = n + int(x[7])
    r.append([i, n])
for i in range(len(r)):
    for j in range(len(r) - 1):
        if r[j][1] < r[j + 1][1]:
            aux = r[j]
            r[j] = r[j + 1]
            r[j + 1] = aux
txt = ""
for i in range(10):
    txt = txt + str(i + 1) + ". " + r[i][0] + " " + str(r[i][1]) + "\n"
print(txt)

# tallas zapatillas
for tipo in ["Zapatillas de asfalto", "Zapatillas de trail"]:
    tl = []
    for x in d:
        if x[2] == tipo and x[5] not in tl:
            tl.append(x[5])
    res = []
    for t2 in tl:
        n = 0
        for x in d:
            if x[2] == tipo and x[5] == t2:
                n = n + int(x[7])
        res.append([t2, n])
    res.sort(key=lambda a: a[1], reverse=True)
    print(tipo, res[0:5])

# marcas y segunda mano
mk = []
for x in d:
    if (x[2] == "Zapatillas de asfalto" or x[2] == "Zapatillas de trail") and x[4] not in mk:
        mk.append(x[4])
for m in mk:
    n = 0
    n2 = 0
    for x in d:
        if (x[2] == "Zapatillas de asfalto" or x[2] == "Zapatillas de trail") and x[4] == m:
            n = n + int(x[7])
            if x[6] == "Segunda mano":
                n2 = n2 + int(x[7])
    print(m, n, str(round(n2 / n * 100, 1)) + "%")

print("tiempo: " + str(time.time() - t))
