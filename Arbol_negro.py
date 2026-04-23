import sys

class Nodo:
    """ Clase que representa un nodo en el Árbol Rojo-Negro. """
    def __init__(self, clave, color="ROJO"):
        self.clave = clave
        self.padre = None
        self.izq = None
        self.der = None
        self.color = color  # "ROJO" o "NEGRO"

class ArbolRojoNegro:
    def __init__(self):
        # Nodo centinela (hojas NIL siempre son negras)
        self.NIL = Nodo(0, color="NEGRO")
        self.raiz = self.NIL

    # --- Rotaciones ---

    def rotar_izquierda(self, x):
        """ Complejidad: O(1) """
        y = x.der
        x.der = y.izq
        if y.izq != self.NIL:
            y.izq.padre = x
        y.padre = x.padre
        if x.padre == None:
            self.raiz = y
        elif x == x.padre.izq:
            x.padre.izq = y
        else:
            x.padre.der = y
        y.izq = x
        x.padre = y

    def rotar_derecha(self, x):
        """ Complejidad: O(1) """
        y = x.izq
        x.izq = y.der
        if y.der != self.NIL:
            y.der.padre = x
        y.padre = x.padre
        if x.padre == None:
            self.raiz = y
        elif x == x.padre.der:
            x.padre.der = y
        else:
            x.padre.izq = y
        y.der = x
        x.padre = y

    # --- Inserción ---

    def insertar(self, clave):
        """ 
        Inserta una clave y corrige el balanceo.
        Complejidad Temporal: O(log n) 
        """
        nuevo_nodo = Nodo(clave)
        nuevo_nodo.izq = self.NIL
        nuevo_nodo.der = self.NIL
        
        y = None
        x = self.raiz

        # Búsqueda de la posición de inserción
        while x != self.NIL:
            y = x
            if nuevo_nodo.clave < x.clave:
                x = x.izq
            else:
                x = x.der

        nuevo_nodo.padre = y
        if y == None:
            self.raiz = nuevo_nodo
        elif nuevo_nodo.clave < y.clave:
            y.izq = nuevo_nodo
        else:
            y.der = nuevo_nodo

        # Si el árbol solo tiene la raíz
        if nuevo_nodo.padre == None:
            nuevo_nodo.color = "NEGRO"
            return

        # Si el abuelo no existe, no hay que corregir
        if nuevo_nodo.padre.padre == None:
            return

        self._corregir_insercion(nuevo_nodo)

    def _corregir_insercion(self, k):
        """ Rebalanceo tras inserción. Complejidad: O(log n) """
        while k.padre.color == "ROJO":
            if k.padre == k.padre.padre.der:
                tio = k.padre.padre.izq
                if tio.color == "ROJO": # Caso 1: Tío rojo
                    tio.color = "NEGRO"
                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    k = k.padre.padre
                else: # Caso 2 o 3: Tío negro
                    if k == k.padre.izq:
                        k = k.padre
                        self.rotar_derecha(k)
                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    self.rotar_izquierda(k.padre.padre)
            else:
                tio = k.padre.padre.der
                if tio.color == "ROJO": # Caso 1: Tío rojo
                    tio.color = "NEGRO"
                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    k = k.padre.padre
                else: # Caso 2 o 3: Tío negro
                    if k == k.padre.der:
                        k = k.padre
                        self.rotar_izquierda(k)
                    k.padre.color = "NEGRO"
                    k.padre.padre.color = "ROJO"
                    self.rotar_derecha(k.padre.padre)
            if k == self.raiz:
                break
        self.raiz.color = "NEGRO"

    # --- Búsqueda y Recorrido ---

    def buscar(self, clave):
        """ Complejidad: O(log n) """
        curr = self.raiz
        while curr != self.NIL:
            if clave == curr.clave:
                return True
            curr = curr.izq if clave < curr.clave else curr.der
        return False

    def inorden(self):
        """ Complejidad: O(n) """
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo != self.NIL:
            self._inorden_recursivo(nodo.izq, resultado)
            resultado.append(nodo.clave)
            self._inorden_recursivo(nodo.der, resultado)

    # --- Visualización ---

    def mostrar(self, nodo=None, prefijo="", es_izq=True):
        """ Imprime el árbol con colores ANSI. Complejidad: O(n) """
        if nodo is None:
            nodo = self.raiz
        
        if nodo == self.NIL:
            return

        if nodo.der != self.NIL:
            self.mostrar(nodo.der, prefijo + ("│   " if es_izq else "    "), False)
        
        # Color rojo para ROJO, gris para NEGRO
        color_code = "\033[91m" if nodo.color == "ROJO" else "\033[90m"
        reset_code = "\033[0m"
        print(prefijo + ("└── " if es_izq else "┌── ") + f"{color_code}{nodo.clave}{reset_code}")
        
        if nodo.izq != self.NIL:
            self.mostrar(nodo.izq, prefijo + ("    " if es_izq else "│   "), True)

# --- Bloque de ejecución ---
if __name__ == "__main__":
    arbol = ArbolRojoNegro()
    # Insertamos valores que fuercen rotaciones
    valores = [20, 15, 25, 10, 5, 1, 30, 27]
    
    print("Iniciando inserción de valores...")
    for v in valores:
        arbol.insertar(v)
    
    print("\nRecorrido Inorden (debería estar ordenado):")
    print(arbol.inorden())
    
    print("\nEstructura Visual del Árbol (Rojo = Rojo, Gris = Negro):")
    arbol.mostrar()
    
    print("\n--- Pruebas de Búsqueda ---")
    for b in [10, 99]:
        print(f"¿Existe la clave {b}?: {arbol.buscar(b)}")