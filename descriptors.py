"""
Módulo de Descriptores de Validación.
Contiene clases de descriptores reusables que implementan el protocolo descriptor (__set__ y __get__)
para garantizar la integridad de datos en los atributos de instancia sin duplicar código de validación.
"""

class ValidarNota:

    def __init__(self,nombre_atributo):

        """
        Constructor del descriptor.
        :param nombre_atributo: Nombre de la clave con la que se guardará el valor
                                dentro del diccionario privado `__dict__` de la instancia.
        """
        self.nombre_atributo = nombre_atributo

    def __get__(self, instance, owner):

        """
        Método invocado automáticamente al LEER el atributo (ej: estudiante.nota_examen).
        - Si se accede desde la clase (instance is None), retorna el propio descriptor.
        - Si se accede desde una instancia, retorna el valor guardado en su `__dict__`.
        """

        if instance is None:
            return self

        return instance.__dict__.get(self.nombre_atributo,0.0)

    def __set__(self, instance, value):
        """
        Método invocado automáticamente al ASIGNAR un valor (ej: estudiante.nota_examen = 8.5).
        Aplica las reglas de negocio estrictas antes de guardar el valor.
        """
        if not isinstance(value,(int,float)): 
            raise TypeError("La nota debe ser un número comprendido entre el 0 y el 10")

        # 2. Validación de rango académico (0.0 a 10.0)
        if not ( 0.0 <= value <= 10.00):
            raise ValueError("La nota debe estar comprendida entre el 0 y el 10.00")

        # 3. Almacenamiento seguro en el diccionario interno de la instancia
        instance.__dict__[self.nombre_atributo] = float(value)
        