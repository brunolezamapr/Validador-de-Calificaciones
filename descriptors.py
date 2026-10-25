
class ValidarNota:

    def __init__(self,nombre_atributo):
        self.nombre_atributo = nombre_atributo

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self.nombre_atributo,0.0)

    def __set__(self, instance, value):
        if not isinstance(value,(int,float)): 
            raise TypeError("La nota debe ser un número comprendido entre el 0 y el 10")

        if not ( 0.0 <= value <= 10.00):
            raise ValueError("La nota debe estar comprendida entre el 0 y el 10.00")

        instance.__dict__[self.nombre_atributo] = float(value)
        