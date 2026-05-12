import sys
import os
import json
import pytest

from unittest.mock import patch

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions import (
    addExpense,
    deleteExpense,
    monthlySummary,
    exportToCSV
)


# ----------------------------------------
# Fixture Setup
# ----------------------------------------

@pytest.fixture
def sample_data():

    test_data = [
        {
            "category": "Food",
            "amount": 200,
            "date": "2026-05-01"
        },
        {
            "category": "Travel",
            "amount": 500,
            "date": "2026-05-03"
        }
    ]

    with open("expense.json", "w") as file:
        json.dump(test_data, file)

    yield

    # Cleanup
    if os.path.exists("expense.json"):
        os.remove("expense.json")

    if os.path.exists("expense.csv"):
        os.remove("expense.csv")


# ----------------------------------------
# Test addExpense()
# ----------------------------------------

def test_add_expense(sample_data):

    addExpense("Shopping", 1000)

    with open("expense.json", "r") as file:
        data = json.load(file)

    assert len(data) == 3
    assert data[-1]["category"] == "Shopping"
    assert data[-1]["amount"] == 1000


# ----------------------------------------
# Test deleteExpense()
# ----------------------------------------

@patch("builtins.input", return_value="Food")
def test_delete_expense(mock_input, sample_data):

    deleteExpense()

    with open("expense.json", "r") as file:
        data = json.load(file)

    categories = [exp["category"] for exp in data]

    assert "Food" not in categories


# ----------------------------------------
# Test monthlySummary()
# ----------------------------------------

@patch("builtins.input", side_effect=["5", "2026"])
@patch("builtins.print")
def test_monthly_summary(mock_print, mock_input, sample_data):

    monthlySummary()

    mock_print.assert_any_call("Food : ₹200.0")
    mock_print.assert_any_call("Travel : ₹500.0")
    mock_print.assert_any_call("Total Expense :₹700.0")


# ----------------------------------------
# Test exportToCSV()
# ----------------------------------------

def test_export_to_csv(sample_data):

    exportToCSV()

    assert os.path.exists("expense.csv")

    with open("expense.csv", "r") as file:
        content = file.read()

    assert "Food" in content
    assert "Travel" in content


# ----------------------------------------
# Edge Case: Empty JSON File
# ----------------------------------------

@patch("builtins.print")
def test_empty_json_file(mock_print):

    with open("expense.json", "w") as file:
        file.write("")

    monthlySummary()

    mock_print.assert_any_call("You've not made any expense yet.")

    os.remove("expense.json")


# ----------------------------------------
# Edge Case: Invalid JSON
# ----------------------------------------

@patch("builtins.print")
def test_invalid_json(mock_print):

    with open("expense.json", "w") as file:
        file.write("{ invalid json }")

    exportToCSV()

    mock_print.assert_any_call("Expense file is empty!")

    os.remove("expense.json")


# ----------------------------------------
# Edge Case: Delete Non-existing Category
# ----------------------------------------

@patch("builtins.input", return_value="Movies")
def test_delete_non_existing_category(mock_input, sample_data):

    deleteExpense()

    with open("expense.json", "r") as file:
        data = json.load(file)

    assert len(data) == 2


# ----------------------------------------
# Edge Case: Export Empty Data
# ----------------------------------------

def test_export_empty_data():

    with open("expense.json", "w") as file:
        json.dump([], file)

    exportToCSV()

    assert os.path.exists("expense.csv")

    with open("expense.csv", "r") as file:
        content = file.read()

    assert "category,amount,date" in content

    os.remove("expense.json")
    os.remove("expense.csv")


# ----------------------------------------
# Edge Case: Monthly Summary No Expenses
# ----------------------------------------

@patch("builtins.input", side_effect=["1", "2030"])
@patch("builtins.print")
def test_monthly_summary_no_expenses(mock_print, mock_input, sample_data):

    monthlySummary()

    mock_print.assert_any_call("Total Expense :₹0")