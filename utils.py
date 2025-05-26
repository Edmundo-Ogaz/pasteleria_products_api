def find_word(list, element):
    """
    Busca una palabra completa o parcial en una lista de palabras.
    
    Args:
        lista: Lista de palabras donde buscar
        busqueda: Palabra o fragmento a buscar
        
    Returns:
        Lista de palabras que contienen la búsqueda
    """
    result = []
    
    for word in list:
        # Comprueba si la búsqueda está contenida en la palabra
        if element.lower() in word.lower():
            result.append(word)
            
    return result

import re

def singularizar(palabra: str) -> str:
    # Simplificación básica; puedes usar nltk o reglas específicas
    if palabra.endswith("es"):
        return palabra[:-2]
    elif palabra.endswith("s"):
        return palabra[:-1]
    return palabra

def singular(palabra):
    """
    Convierte una palabra en plural al singular.
    Si la palabra ya está en singular, la devuelve sin cambios.
    """
    # Reglas para convertir de plural a singular en español
    
    # Excepciones comunes (palabras invariables o casos especiales)
    excepciones = {
        'pies': 'pie',
        'crisis': 'crisis',
        'virus': 'virus',
        'dosis': 'dosis',
        'tesis': 'tesis',
        'análisis': 'análisis',
        'lunes': 'lunes',
        'martes': 'martes',
        'miércoles': 'miércoles',
        'jueves': 'jueves',
        'viernes': 'viernes'
    }
    
    if palabra.lower() in excepciones:
        return excepciones[palabra.lower()]
    
    # Palabras que terminan en "es" pero que solo necesitan quitar la "s" final
    palabras_es_especiales = ['chocolate', 'tomate', 'elefante', 'estudiante', 'diamante']
    
    for raiz in palabras_es_especiales:
        if palabra.lower() == raiz + 's':
            return raiz
    
    # Palabras que terminan en 'es' donde la raíz termina en consonante
    if len(palabra) > 3 and palabra.endswith('es'):
        # Casos especiales para palabras que terminan en 'ces'
        if palabra.endswith('ces'):
            return palabra[:-3] + 'z'
        # Casos especiales para palabras que terminan en 'res'
        elif palabra.endswith('res') and len(palabra) > 4:
            if palabra[-4] in 'aeiou':
                return palabra[:-2]
            return palabra[:-1]
        # Para palabras como "chocolates", verificamos si termina en "tes"
        elif palabra.endswith('tes') and len(palabra) > 6:
            # Verificar si es una palabra como 'chocolates', 'tomates', etc.
            return palabra[:-1]
        # Otros casos de palabras terminadas en "es"
        else:
            return palabra[:-2]
    
    # Palabras que terminan en 's' donde la raíz termina en vocal
    elif len(palabra) > 2 and palabra.endswith('s') and palabra[-2] in 'aeiou':
        return palabra[:-1]
    
    # Palabras que ya están en singular o no se ajustan a las reglas anteriores
    return palabra