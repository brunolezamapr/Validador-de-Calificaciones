"""
Módulo del Modelo Estudiante.
Define la entidad Estudiante integrando descriptores para atributos gerenciados,
propiedades de solo lectura, métodos estáticos utilitarios y sobrecarga de operadores de comparación.
"""

from descriptors import ValidarNota

class Estudiante:
    # Atributo gerenciado mediante el descriptor reutilizable `ValidarNota`
    nota_examen = ValidarNota("nota_examen")
    def __init__(self,nombre:str,nota_examen:float):
        self.nombre = nombre
        self.nota_examen = nota_examen

    @property
    def aprobado(self) -> bool :
        """
        Propiedad de SOLO LECTURA (@property).
        Calcula dinámicamente si el estudiante aprobó el examen sin almacenar un estado redundante.
        Criterio: Aprobado si nota_examen >= 6.0.
        """
        return self.nota_examen >= 6.0 

    @staticmethod
    def es_nombre_valido(nombre:str) -> bool:

        """
        Método Estático (@staticmethod):
        Función utilitaria pura sin acceso ni dependencia a 'self' o 'cls'.
        Valida que el nombre sea una cadena no vacía que contenga únicamente letras,
        tildes, espacios o la letra Ñ.
        """


        if not isinstance(nombre, str):
            return False
            
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            return False
            
        # Verifica que cada carácter sea una letra o un espacio
        return all(c.isalpha() or c.isspace() for c in nombre_limpio)

    def __eq__(self, other) -> bool:

        """
        Sobrecarga del operador de igualdad (==).
        Dos estudiantes son considerados iguales si obtuvieron exactamente la misma nota de examen.
        """
        if not isinstance(other,Estudiante):
            return NotImplemented

        return self.nota_examen == other.nota_examen

    def __lt__(self, other) -> bool :

        """
        Sobrecarga del operador 'menor que' (<).
        Permite comparar si la nota de este estudiante es menor que la de otro.
        Permite el ordenamiento automático de listas usando sort() o sorted().
        """

        if not isinstance(other,Estudiante):
            return NotImplemented
        
        return self.nota_examen < other.nota_examen 