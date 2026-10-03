import datetime
from decimal import Decimal

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def make_calculation():
    return Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))

# Test Memento Serialization

def test_memento_to_dict():
    calc = make_calculation()
    timestamp = datetime.datetime(2024, 1, 1, 12, 0, 0)
    memento = CalculatorMemento(history=[calc], timestamp=timestamp)
    data = memento.to_dict()
    assert data['history'] == [calc.to_dict()]
    assert data['timestamp'] == timestamp.isoformat()

def test_memento_from_dict():
    calc = make_calculation()
    timestamp = datetime.datetime(2024, 1, 1, 12, 0, 0)
    data = {'history': [calc.to_dict()], 'timestamp': timestamp.isoformat()}
    memento = CalculatorMemento.from_dict(data)
    assert memento.timestamp == timestamp
    assert len(memento.history) == 1
    assert memento.history[0].operation == "Addition"
    assert memento.history[0].result == Decimal("5")

def test_memento_round_trip():
    original = CalculatorMemento(history=[make_calculation()])
    restored = CalculatorMemento.from_dict(original.to_dict())
    assert restored.to_dict() == original.to_dict()