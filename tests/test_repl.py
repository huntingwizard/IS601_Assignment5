from decimal import Decimal
from unittest.mock import patch

import pytest

from app.calculator_repl import calculator_repl
from app.exceptions import OperationError, ValidationError

# Test Exit

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history', side_effect=Exception("disk full"))
def test_calculator_repl_exit_save_failure(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Warning: Could not save history: disk full")
    mock_print.assert_any_call("Goodbye!")

# Test History

@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.show_history', return_value=[])
def test_calculator_repl_history_empty(mock_show_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("No calculations in history")

@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.show_history',
       return_value=["Addition(2, 3) = 5", "Subtraction(5, 1) = 4"])
def test_calculator_repl_history_with_entries(mock_show_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nCalculation History:")
    mock_print.assert_any_call("1. Addition(2, 3) = 5")
    mock_print.assert_any_call("2. Subtraction(5, 1) = 4")

# Test Clear

@patch('builtins.input', side_effect=['clear', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.clear_history')
def test_calculator_repl_clear(mock_clear_history, mock_print, mock_input):
    calculator_repl()
    mock_clear_history.assert_called_once()
    mock_print.assert_any_call("History cleared")

# Test Undo

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.undo', return_value=True)
def test_calculator_repl_undo(mock_undo, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation undone")

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.undo', return_value=False)
def test_calculator_repl_undo_nothing(mock_undo, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to undo")

# Test Redo

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.redo', return_value=True)
def test_calculator_repl_redo(mock_redo, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation redone")

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.redo', return_value=False)
def test_calculator_repl_redo_nothing(mock_redo, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to redo")

# Test Save

@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
def test_calculator_repl_save(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History saved successfully")

@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history', side_effect=Exception("nope"))
def test_calculator_repl_save_failure(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error saving history: nope")

# Test Load

@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
@patch('app.calculator.Calculator.load_history')
def test_calculator_repl_load(mock_load_history, mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History loaded successfully")

@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
@patch('app.calculator.Calculator.load_history', side_effect=Exception("corrupt"))
def test_calculator_repl_load_failure(mock_load_history, mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error loading history: corrupt")

# Test Arithmetic Commands

@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
def test_calculator_repl_cancel_first_number(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")

@patch('builtins.input', side_effect=['add', '2', 'cancel', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
def test_calculator_repl_cancel_second_number(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
@patch('app.calculator.Calculator.perform_operation', return_value=Decimal("5.00"))
def test_calculator_repl_result_normalized(mock_perform, mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 5")

@patch('builtins.input', side_effect=['add', 'x', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
@patch('app.calculator.Calculator.perform_operation', side_effect=ValidationError("bad input"))
def test_calculator_repl_validation_error(mock_perform, mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error: bad input")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
@patch('app.calculator.Calculator.perform_operation', side_effect=OperationError("bad op"))
def test_calculator_repl_operation_error(mock_perform, mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error: bad op")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
@patch('app.calculator.Calculator.perform_operation', side_effect=Exception("weird"))
def test_calculator_repl_unexpected_error(mock_perform, mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Unexpected error: weird")

# Test Unknown Command

@patch('builtins.input', side_effect=['frobnicate', 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
def test_calculator_repl_unknown_command(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Unknown command: 'frobnicate'. Type 'help' for available commands.")

# Test Interrupts and Fatal Errors

@patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
def test_calculator_repl_keyboard_interrupt(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nOperation cancelled")

@patch('builtins.input', side_effect=[EOFError])
@patch('builtins.print')
def test_calculator_repl_eof_error(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nInput terminated. Exiting...")

@patch('builtins.input', side_effect=[Exception("boom"), 'exit'])
@patch('builtins.print')
@patch('app.calculator.Calculator.save_history')
def test_calculator_repl_unexpected_loop_error(mock_save_history, mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error: boom")

@patch('builtins.print')
@patch('app.calculator_repl.Calculator', side_effect=Exception("init failed"))
def test_calculator_repl_fatal_error(mock_calculator, mock_print):
    with pytest.raises(Exception, match="init failed"):
        calculator_repl()
    mock_print.assert_any_call("Fatal error: init failed")