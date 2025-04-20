from calculator.calculator import Calculator

def test_add() -> None:
    calc = Calculator()
    assert calc.add(1, 2) == 3 

def test_subtract() -> None:
    calc = Calculator()
    assert calc.subtract(5, 3) == 2

def test_multiply() -> None:
    calc = Calculator()
    assert calc.multiply(2, 3) == 6

def test_divide()-> None:
    calc = Calculator()
    assert calc.divide(6, 3) == 2
    try:
        calc.divide(1, 0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero."