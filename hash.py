class TablaHash:
    def __init__(self, m=7):
        """
        Inicializa la tabla con tamaño m=7.
        Complejidad Temporal: O(m) para crear las cubetas.
        """
        self.m = m
        self.n = 0
        self.tabla = [[] for _ in range(self.m)]

    def _calcular_suma_ascii(self, cadena):
        """
        Calcula el valor automático sumando los códigos ASCII.
        Complejidad Temporal: O(k), donde k es el número de caracteres de la cadena.
        """
        return sum(ord(char) for char in str(cadena))

    def _hash(self, suma_ascii):
        """
        Calcula el índice de la tabla usando el método de división.
        Complejidad Temporal: O(1).
        """
        return suma_ascii % self.m

    def insertar(self, clave):
        """
        Inserta un par clave-valor. Si la clave existe, actualiza el valor.
        Complejidad Temporal: 
           - Promedio: O(1 + alpha), donde alpha es el factor de carga.
           - Peor caso: O(n) si todos los elementos colisionan en la misma cubeta.
        """
        valor_automatico = self._calcular_suma_ascii(clave)
        indice = self._hash(valor_automatico)
        
        for i, (c, v) in enumerate(self.tabla[indice]):
            if c == clave:
                self.tabla[indice][i] = (clave, valor_automatico)
                return valor_automatico
        
        self.tabla[indice].append((clave, valor_automatico))
        self.n += 1
        return valor_automatico

    def buscar(self, clave):
        """
        Busca una clave y retorna el valor ASCII asociado.
        Complejidad Temporal:
           - Promedio: O(1 + alpha).
           - Peor caso: O(n).
        """
        suma_ascii = self._calcular_suma_ascii(clave)
        indice = self._hash(suma_ascii)
        for c, v in self.tabla[indice]:
            if c == clave:
                return v
        return None

    def eliminar(self, clave):
        """
        Elimina la clave de la tabla.
        Complejidad Temporal:
           - Promedio: O(1 + alpha).
           - Peor caso: O(n).
        """
        suma_ascii = self._calcular_suma_ascii(clave)
        indice = self._hash(suma_ascii)
        for i, (c, v) in enumerate(self.tabla[indice]):
            if c == clave:
                self.tabla[indice].pop(i)
                self.n -= 1
                return True
        return False

    def factor_carga(self):
        """
        Calcula la densidad de la tabla (alpha = n/m).
        Complejidad Temporal: O(1).
        """
        return self.n / self.m

    def mostrar_tabla(self):
        """
        Visualiza la estructura de encadenamiento.
        Complejidad Temporal: O(m + n).
        """
        print("\n--- VISUALIZACIÓN DE LA TABLA ---")
        for i in range(self.m):
            nodos = [f"[{c}: {v}]" for c, v in self.tabla[i]]
            print(f"Índice {i}: {' -> '.join(nodos) if nodos else 'Vacio'}")
        print("---------------------------------")

def ejecutar():
    mi_tabla = TablaHash(7)
    
    while True:
        print("\n[1] Insertar [2] Buscar [3] Eliminar [4] Mostrar Tabla [5] Factor Carga [6] Salir")
        opcion = input("Seleccione: ")

        if opcion == "1":
            c = input("Clave: ")
            v = mi_tabla.insertar(c)
            print(f"Insertado con valor ASCII: {v}")
        elif opcion == "2":
            c = input("Clave: ")
            res = mi_tabla.buscar(c)
            print(f"Resultado: {res if res is not None else 'No encontrado'}")
        elif opcion == "3":
            c = input("Clave: ")
            print("Eliminado" if mi_tabla.eliminar(c) else "No encontrado")
        elif opcion == "4":
            mi_tabla.mostrar_tabla()
        elif opcion == "5":
            print(f"Factor de carga (alpha): {mi_tabla.factor_carga():.2f}")
        elif opcion == "6":
            break

if __name__ == "__main__":
    ejecutar()