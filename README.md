# 📁 Proyecto 1: Validador de Calificaciones y Estudiantes

# 🎓 Validador de Calificaciones y Estudiantes (POO en Python)

Un sistema modular y didáctico desarrollado en Python que demuestra la aplicación práctica de patrones avanzados de **Programación Orientada a Objetos (POO)**. Este proyecto está diseñado como una guía de referencia para entender cómo estructurar un modelo de dominio con validaciones robustas, propiedades calculadas, métodos utilitarios y operadores de comparación.

---

## 📌 ¿Por qué este proyecto? (Conceptos Clave de POO)

Al construir sistemas académicos o administrativos, es muy común encontrarse con código repetitivo en la validación de atributos o con clases sobrecargadas. En esta solución resolvemos esos problemas utilizando cuatro pilares clave de Python:


## 📁 Estructura del Proyecto

```text
ValidadorCalificaciones/
│
├── descriptors.py    # Descriptor reusable ValidarNota (Protocolo __get__/__set__)
├── Estudiante.py     # Entidad principal del dominio con @property y @staticmethod
├── main.py           # Suite de pruebas con ejecuciones e impresiones interactivas
└── README.md         # Documentación técnica y explicativa del proyecto
```
### 1. Descriptores de Validación Reusables (`ValidarNota`)
* **El Problema:** Si tuviéramos múltiples atributos de nota (ej: `nota_examen`, `nota_proyecto`, `nota_asistencia`), usar getters y setters normales (`@property.setter`) nos obligaría a repetir el mismo bloque `if/raise` una y otra vez.
* **La Solución:** Un **Descriptor** es una clase que implementa los métodos mágicos `__get__` y `__set__`. Actúa como un "guardián" del atributo a nivel de clase. En nuestro proyecto, `ValidarNota` encapsula la regla de negocio:
  - Garantiza que la calificación sea de tipo `int` o `float`.
  - Fuerza que la nota se encuentre strictly entre `0.0` y `10.0`.
  - Almacena el dato limpiamente dentro del diccionario privado de la instancia (`instance.__dict__`).


### 📄 File: `descriptors.py`

```python
"""
Módulo de Descriptores de Validación Académica.
Contiene la clase `ValidarNota` que implementa el protocolo descriptor (__get__ y __set__)
para garantizar la integridad de las calificaciones sin duplicar setters.
"""


class ValidarNota:

    def __init__(self, nombre_atributo: str):
        """
        Constructor del descriptor.
        :param nombre_atributo: Clave con la que se guardará el valor en el
                                diccionario `__dict__` de la instancia.
        """
        self.nombre_atributo = nombre_atributo

    def __get__(self, instance, owner):
        """
        Invocado automáticamente al leer el atributo (ej: estudiante.nota_examen).
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.nombre_atributo)

    def __set__(self, instance, value):
        """
        Invocado automáticamente al asignar un valor (ej: estudiante.nota_examen = 8.5).
        Valida que la nota sea un número entre 0.0 y 10.0.
        """
        # 1. Validación de tipo de dato
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"El atributo '{self.nombre_atributo}' debe ser un número entero o flotante."
            )

        # 2. Validación de rango permitido (0.0 a 10.0)
        if not (0.0 <= value <= 10.0):
            raise ValueError(
                f"La nota '{self.nombre_atributo}' debe estar obligatoriamente en el rango de 0.0 a 10.0."
            )

        # 3. Guardar el valor en el diccionario privado de la instancia
        instance.__dict__[self.nombre_atributo] = float(value)
```

### 2. Propiedades Administradas de Solo Lectura (`@property`)
* Usamos el decorador `@property` para exponer el atributo calculable `aprobado`.
* **Ventaja:** En lugar de guardar una variable `self.aprobado = True` que podría desactualizarse si la nota cambia, `@property` calcula dinámicamente si `nota_examen >= 6.0` en tiempo real sin permitir modificaciones accidentales desde fuera de la clase.
---

### 3. Métodos Estáticos de Utilidad (`@staticmethod`)
* La función `es_nombre_valido(nombre)` está decorada con `@staticmethod`.
* **Propósito:** Es una utilidad pura que no requiere acceder al estado de ninguna instancia (`self`) ni de la clase (`cls`). Permite validar o limpiar nombres usando expresiones regulares (`re`) antes incluso de intentar instanciar a un estudiante.

### 4. Sobrecarga de Métodos Dunder (`__eq__` y `__lt__`)
* En lugar de comparar estudiantes con funciones externas, redefinimos los operadores nativos de Python:
  - **`__eq__` (Igualdad `==`):** Determina que dos estudiantes tienen la misma nota si `e1 == e2`.
  - **`__lt__` (Menor que `<`):** Permite evaluar `e1 < e2` comparando sus calificaciones.
  - **Efecto secundario positivo:** Al implementar `__lt__`, Python puede ordenar automáticamente listas de objetos `Estudiante` usando `list.sort()` o `sorted()`.

### 📄 File: `Estudiante.py`

```python
"""
Módulo del Modelo Estudiante.
Entidad principal del dominio que integra descriptores, propiedades calculadas (@property),
utilidades estáticas (@staticmethod) y sobrecarga de operadores Dunder (__eq__, __lt__).
"""

import re
from descriptors import ValidarNota


class Estudiante:
    # Atributo gerenciado mediante el descriptor reutilizable ValidarNota
    nota_examen = ValidarNota("nota_examen")

    def __init__(self, nombre: str, nota_examen: float):
        """
        Inicializa un objeto Estudiante.
        La asignación `self.nota_examen = nota_examen` dispara el descriptor.
        """
        if not Estudiante.es_nombre_valido(nombre):
            raise ValueError(f"El nombre '{nombre}' no es un nombre válido.")

        self.nombre = nombre.strip()
        self.nota_examen = nota_examen  # Dispara ValidarNota.__set__

    @property
    def aprobado(self) -> bool:
        """
        Propiedad calculada de SOLO LECTURA (@property).
        Retorna True si la nota es >= 6.0, evaluada en tiempo real.
        """
        return self.nota_examen >= 6.0

    @staticmethod
    def es_nombre_valido(nombre: str) -> bool:
        """
        Método Estático (@staticmethod):
        Función utilitaria pura que valida que el nombre contenga únicamente letras,
        tildes, espacios o la letra Ñ mediante Expresiones Regulares (regex).
        """
        if not isinstance(nombre, str):
            return False
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            return False
        return bool(re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre_limpio))

    # --- SOBRECARGA DE MÉTODOS DUNDER DE COMPARACIÓN ---

    def __eq__(self, other) -> bool:
        """
        Sobrecarga del operador de igualdad (==).
        Dos estudiantes son iguales si obtuvieron la misma nota.
        """
        if not isinstance(other, Estudiante):
            return NotImplemented
        return self.nota_examen == other.nota_examen

    def __lt__(self, other) -> bool:
        """
        Sobrecarga del operador 'menor que' (<).
        Permite comparar si la nota de este estudiante es menor a la de otro,
        habilitando ordenamiento con sort() o sorted().
        """
        if not isinstance(other, Estudiante):
            return NotImplemented
        return self.nota_examen < other.nota_examen

    def __repr__(self) -> str:
        """Representación oficial del objeto para depuración."""
        return f"Estudiante(nombre='{self.nombre}', nota_examen={self.nota_examen})"
```

---

### 📄 File: `main.py`

```python
"""
Main Script - Punto de entrada y suite de pruebas para el Validador de Calificaciones.
"""

from Estudiante import Estudiante

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBA EJERCICIO 1: ESTUDIANTE Y VALIDADOR DE NOTAS")
    print("=" * 60)

    # 1. Instanciación correcta de objetos Estudiante
    e1 = Estudiante("Bruno Lezama", 8.5)
    e2 = Estudiante("Carlos Perez", 5.0)

    print(f"Estudiante 1: {e1} | ¿Aprobado?: {e1.aprobado}")
    print(f"Estudiante 2: {e2} | ¿Aprobado?: {e2.aprobado}")

    # 2. Pruebas de comparación con Métodos Dunder (__lt__ y __eq__)
    print(f"\n¿{e2.nombre} tiene menor nota que {e1.nombre}? (e2 < e1): {e2 < e1}")
    print(f"¿Tienen la misma nota? (e1 == e2): {e1 == e2}")

    # 3. Prueba de Método Estático de validación de nombres
    print(
        f"\nValidación estática de nombre 'Ana María': {Estudiante.es_nombre_valido('Ana María')}"
    )
    print(
        f"Validación estática de nombre 'Bruno123': {Estudiante.es_nombre_valido('Bruno123')}"
    )

    # 4. Pruebas de captura de errores gestionadas por el Descriptor
    print("\n" + "-" * 40)
    print("PRUEBAS DE CAPTURA DE ERRORES (DESCRIPTORES)")
    print("-" * 40)

    try:
        e_invalido = Estudiante("Error Examen", 15.0)  # Lanza ValueError (> 10.0)
    except ValueError as err:
        print(f"[ÉXITO] Captura de nota fuera de rango: {err}")

    try:
        e_tipo_err = Estudiante("Error Tipo", "diez")  # Lanza TypeError
    except TypeError as err:
        print(f"[ÉXITO] Captura de tipo inválido: {err}")
```
