# test suite
# from roman.converter import to_roman, from_roman
import pytest
from roman.converter import (
    to_roman,
    from_roman,
    is_valid_roman,
    add_roman,
    subtract_roman,
    RomanError,
    _roundtrip_differs,
    _count_char
)


def test_one():
    assert to_roman(1) == "I"


def test_two():
    assert to_roman(2) == "II"


def test_three():
    assert to_roman(3) == "III"


def test_five():
    assert to_roman(5) == "V"


def test_ten():
    assert to_roman(10) == "X"


def test_fifty():
    assert to_roman(50) == "L"


def test_hundred():
    assert to_roman(100) == "C"


def test_five_hundred():
    assert to_roman(500) == "D"


def test_thousand():
    assert to_roman(1000) == "M"


def test_from_one():
    assert from_roman("I") == 1


def test_from_five():
    assert from_roman("V") == 5


def test_from_two():
    assert from_roman("II") == 2


def test_roundtrip_small():
    assert from_roman(to_roman(7)) == 7


def test_roundtrip_medium():
    assert from_roman(to_roman(58)) == 58


def test_lowercase_input():
    assert from_roman("xi") == 11


# --- Pruebas para to_roman  ---

def test_to_roman_not_int():
    with pytest.raises(RomanError, match="value must be an integer"):
        to_roman("10")

def test_to_roman_bool():
    with pytest.raises(RomanError, match="value must be an integer"):
        to_roman(True)

def test_to_roman_less_than_min():
    with pytest.raises(RomanError, match="value must be >= 1"):
        to_roman(0)

def test_to_roman_greater_than_max():
    with pytest.raises(RomanError, match="value must be <= 3999"):
        to_roman(4000)

# --- Pruebas para from_roman  ---

def test_from_roman_not_str():
    with pytest.raises(RomanError, match="value must be a string"):
        from_roman(10)

def test_from_roman_empty_string():
    with pytest.raises(RomanError, match="empty string is not a roman numeral"):
        from_roman("")

def test_from_roman_invalid_char():
    with pytest.raises(RomanError, match="invalid roman character: A"):
        from_roman("XA")

def test_from_roman_invalid_subtractive():
    with pytest.raises(RomanError, match="invalid subtractive pair: IC"):
        from_roman("IC")

def test_from_roman_out_of_range():
    with pytest.raises(RomanError, match="value out of range 1..3999"):
        from_roman("MMMM")

def test_from_roman_valid_subtractive_pairs():
    assert from_roman("IV") == 4
    assert from_roman("IX") == 9
    assert from_roman("XL") == 40
    assert from_roman("XC") == 90
    assert from_roman("CD") == 400
    assert from_roman("CM") == 900

# --- Pruebas para las funciones adicionales y helpers ---

def test_is_valid_roman():
    assert is_valid_roman("XIV") is True
    assert is_valid_roman("HOLA") is False

def test_add_roman():
    assert add_roman("II", "III") == "V"

def test_subtract_roman():
    assert subtract_roman("V", "II") == "III"

def test_roundtrip_differs():
    assert _roundtrip_differs(4, "IIII") is True
    assert _roundtrip_differs(4, "IV") is False

def test_count_char():
    assert _count_char("XVIII", "I") == 3


# --- Parte 4: Prueba a Nivel de Integración ---

def test_integration_collaboration():
    # integración con suma (X + V = XV)
    sum_result = add_roman("X", "V")
    assert is_valid_roman(sum_result) is True, f"El resultado de la suma {sum_result} no fue aceptado como válido."

    # integración con resta (X - V = V)
    sub_result = subtract_roman("X", "V")
    assert is_valid_roman(sub_result) is True, f"El resultado de la resta {sub_result} no fue aceptado como válido."

    # caso problemático: restar para obtener 0 (I - I = 0)
    with pytest.raises(RomanError):
        subtract_roman("I", "I")
