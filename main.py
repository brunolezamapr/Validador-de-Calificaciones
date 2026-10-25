
if __name__ == "__main__":

    from descriptors import ValidarNota
    from Estudiante import Estudiante

    print("=" * 60)
    print("PRUEBA EJERCICIO 1: ESTUDIANTE Y VALIDADOR DE NOTA")
    print("=" * 60)

    e1 = Estudiante("Bruno", 8.5)
    e2 = Estudiante("Carlos", 5.0)

    print(f"{e1.nombre} - Aprobado: {e1.aprobado}")  # True
    print(f"¿{e2.nombre} tiene menor nota que {e1.nombre}?: {e2 < e1}") # True
    print(f"Validación estática de nombre 'Ana Maria': {Estudiante.es_nombre_valido('Ana Maria')}") # True

   

