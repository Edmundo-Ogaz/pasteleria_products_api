from utils import find_word

def test_find_word():
    words = ["manzana", "plátano", "naranja", "mandarina", "uva", "pera"]
    
    assert find_word(words, "manzana") == ["manzana"]
    assert find_word(words, "man") == ["manzana", "mandarina"]