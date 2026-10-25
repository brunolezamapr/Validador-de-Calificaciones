from descriptors import ValidarNota

class Estudiante:
    
    nota_examen = ValidarNota("nota_examen")
    def __init__(self,nombre:str,nota_examen:float):
        self.nombre = nombre
        self.nota_examen = nota_examen

    @property
    def aprobado(self) -> bool :
        return self.nota_examen >= 6.0 

    @staticmethod
    def es_nombre_valido(nombre:str) -> bool:
        if not isinstance(nombre, str):
            return False
            
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            return False
            
        # Verifica que cada carácter sea una letra o un espacio
        return all(c.isalpha() or c.isspace() for c in nombre_limpio)

    def __eq__(self, other) -> bool:

        if not isinstance(other,Estudiante):
            return NotImplemented

        return self.nota_examen == other.nota_examen

    def __lt__(self, other) -> bool :

        if not isinstance(other,Estudiante):
            return NotImplemented
        
        return self.nota_examen < other.nota_examen 