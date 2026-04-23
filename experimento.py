import time
import random
import string
import matplotlib.pyplot as plt


# ÁRBOL ROJO-NEGRO (IMPORTADO DESDE TU CÓDIGO)

class Nodo:
    def __init__(self, clave, color="ROJO"):
        self.clave = clave
        self.color = color
        self.padre = None
        self.izq = None
        self.der = None


class ArbolRojoNegro:
    def __init__(self):
        self.NIL = Nodo(0, "NEGRO")
        self.raiz = self.NIL

    def rotar_izquierda(self, x):
        y = x.der
        x.der = y.izq

        if y.izq != self.NIL:
            y.izq.padre = x

        y.padre = x.padre

        if x.padre is None:
            self.raiz = y
        elif x == x.padre.izq:
            x.padre.izq = y
        else:
            x.padre.der = y

        y.izq = x
        x.padre = y

    def rotar_derecha(self, x):
        y = x.izq
        x.izq = y.der

        if y.der != self.NIL:
            y.der.padre = x

        y.padre = x.padre

        if x.padre is None:
            self.raiz = y
        elif x == x.padre.der:
            x.padre.der = y
        else:
            x.padre.izq = y

        y.der = x
        x.padre = y

    def insertar(self, clave):
        nuevo = Nodo(clave)
        nuevo.izq = self.NIL
        nuevo.der = self.NIL

        y = None
        x = self.raiz

        while x != self.NIL:
            y = x
            if nuevo.clave < x.clave:
                x = x.izq
            else:
                x = x.der

        nuevo.padre = y

        if y is None:
            self.raiz = nuevo
        elif nuevo.clave < y.clave:
            y.izq = nuevo
        else:
            y.der = nuevo

        if nuevo.padre is None:
            nuevo.color = "NEGRO"
            return

        if nuevo.padre.padre is None:
            return

        self.corregir_insercion(nuevo)

    def corregir_insercion(self, k):
        while k.padre.color == "ROJO":

            if k.padre == k.padre.padre.der:
                tio = k.padre.padre.izq

                if tio.color == "ROJO":
                    tio.color = "NEGRO"
                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    k = k.padre.padre

                else:
                    if k == k.padre.izq:
                        k = k.padre
                        self.rotar_derecha(k)

                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    self.rotar_izquierda(k.padre.padre)

            else:
                tio = k.padre.padre.der

                if tio.color == "ROJO":
                    tio.color = "NEGRO"
                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    k = k.padre.padre

                else:
                    if k == k.padre.der:
                        k = k.padre
                        self.rotar_izquierda(k)

                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    self.rotar_derecha(k.padre.padre)

            if k == self.raiz:
                break

        self.raiz.color = "NEGRO"



# TABLA HASH MODIFICADA PARA PROBAR 2 FUNCIONES HASH


class TablaHash:
    def __init__(self, m=10007, tipo_hash=1):
        self.m = m
        self.n = 0
        self.tipo_hash = tipo_hash
        self.tabla = [[] for _ in range(self.m)]

    def _calcular_suma_ascii(self, cadena):
        return sum(ord(c) for c in str(cadena))

    def _hash1(self, clave):
        # Hash original: suma ASCII % m
        return self._calcular_suma_ascii(clave) % self.m

    def _hash2(self, clave):
        # Segunda función hash: hash polinomial simple
        h = 0
        for c in str(clave):
            h = (h * 31 + ord(c)) % self.m
        return h

    def _obtener_indice(self, clave):
        if self.tipo_hash == 1:
            return self._hash1(clave)
        return self._hash2(clave)

    def insertar(self, clave):
        indice = self._obtener_indice(clave)

        for i, (c, v) in enumerate(self.tabla[indice]):
            if c == clave:
                self.tabla[indice][i] = (clave, clave)
                return

        self.tabla[indice].append((clave, clave))
        self.n += 1


# GENERADOR DE DATOS


def generar_cadenas(n, longitud=8):
    datos = []
    for _ in range(n):
        cadena = ''.join(random.choices(string.ascii_letters, k=longitud))
        datos.append(cadena)
    return datos


# MEDICIÓN DE TIEMPOS


def medir_arbol(n):
    datos = random.sample(range(n * 10), n)

    arbol = ArbolRojoNegro()

    inicio = time.perf_counter()

    for x in datos:
        arbol.insertar(x)

    fin = time.perf_counter()

    return fin - inicio


def medir_hash(n, tipo_hash):
    datos = generar_cadenas(n)

    tabla = TablaHash(m=n * 2, tipo_hash=tipo_hash)

    inicio = time.perf_counter()

    for x in datos:
        tabla.insertar(x)

    fin = time.perf_counter()

    return fin - inicio



# EXPERIMENTO


tamanos = [100, 1000, 10000, 50000]

resultados = []

print("\n=== INICIANDO EXPERIMENTO ===\n")

for n in tamanos:
    print(f"Probando n = {n}")

    tiempo_arbol = medir_arbol(n)
    tiempo_hash1 = medir_hash(n, 1)
    tiempo_hash2 = medir_hash(n, 2)

    resultados.append({
        "n": n,
        "Arbol RN": tiempo_arbol,
        "Hash Función 1": tiempo_hash1,
        "Hash Función 2": tiempo_hash2
    })

    print(f"Árbol RN: {tiempo_arbol:.6f} s")
    print(f"Hash 1 : {tiempo_hash1:.6f} s")
    print(f"Hash 2 : {tiempo_hash2:.6f} s")
    print("-" * 40)


# TABLA DE RESULTADOS


print("\n=== TABLA DE RESULTADOS ===\n")

print(f"{'n':<10}{'Árbol RN':<20}{'Hash 1':<20}{'Hash 2':<20}")

for r in resultados:
    print(f"{r['n']:<10}{r['Arbol RN']:<20.6f}{r['Hash Función 1']:<20.6f}{r['Hash Función 2']:<20.6f}")




fig, ax = plt.subplots(figsize=(10, 3))
ax.axis('off')

datos_tabla = []

for r in resultados:
    datos_tabla.append([
        r["n"],
        f"{r['Arbol RN']:.6f}",
        f"{r['Hash Función 1']:.6f}",
        f"{r['Hash Función 2']:.6f}"
    ])

columnas = ["n", "Árbol RN", "Hash 1", "Hash 2"]

tabla = ax.table(
    cellText=datos_tabla,
    colLabels=columnas,
    loc='center'
)

tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.5)

plt.title("Tabla Comparativa de Resultados")
plt.show()


# GRÁFICAS

x = [r["n"] for r in resultados]
y_arbol = [r["Arbol RN"] for r in resultados]
y_hash1 = [r["Hash Función 1"] for r in resultados]
y_hash2 = [r["Hash Función 2"] for r in resultados]

plt.figure(figsize=(10, 6))

plt.plot(x, y_arbol, marker='o', label="Árbol Rojo-Negro")
plt.plot(x, y_hash1, marker='s', label="Tabla Hash - Función 1")
plt.plot(x, y_hash2, marker='^', label="Tabla Hash - Función 2")

plt.xlabel("Número de elementos (n)")
plt.ylabel("Tiempo de inserción (segundos)")
plt.title("Comparación Experimental de Rendimiento")
plt.legend()
plt.grid(True)

plt.show()

