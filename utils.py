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