import pytest
import trino


# Define connection details for the Trino instance running in Docker
@pytest.fixture(scope="module")
def db_connection():
    conn = trino.dbapi.connect(
        host='localhost',  # Assuming you're running Docker locally
        port=8080,  # Trino default port
        user='your_username',  # Replace with any username you prefer (Trino doesn't require passwords by default)
        catalog='memory',  # Catalog to use
        schema='default',  # Schema to use
    )
    yield conn
    conn.close()


# Setup fixture to create tables and insert data before running the tests
@pytest.fixture(scope="module", autouse=True)
def setup_database(db_connection):
    cursor = db_connection.cursor()

    # Clear the employee and expense tables before inserting data
    cursor.execute("TRUNCATE TABLE employee")
    cursor.execute("TRUNCATE TABLE expense")

    # Create employee table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee (
        employee_id TINYINT,
        first_name VARCHAR,
        last_name VARCHAR,
        manager_id TINYINT
    )
    """)

    # Insert employee data
    cursor.execute("""
    INSERT INTO employee (employee_id, first_name, last_name, manager_id)
    VALUES
    (1, 'John', 'Doe', 2),
    (2, 'Jane', 'Smith', NULL),
    (3, 'Alex', 'Johnson', 2),
    (4, 'Emily', 'Davis', 1),
    (5, 'Michael', 'Brown', 3),
    (6, 'Emma', 'Wilson', 3),
    (7, 'Oliver', 'Taylor', 4),
    (8, 'Isabella', 'Clark', 1),
    (9, 'Liam', 'Garcia', 5),
    (10, 'Sophia', 'Martinez', 6)
    """)

    # Create expense table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expense (
        employee_id TINYINT,
        unit_price DECIMAL(8, 2),
        quantity TINYINT
    )
    """)

    # Insert sample expense data
    cursor.execute("""
    INSERT INTO expense (employee_id, unit_price, quantity)
    VALUES
    (1, 100.50, 2),
    (2, 500.00, 3),
    (3, 50.00, 1),
    (4, 200.25, 4),
    (5, 10.75, 6)
    """)

    db_connection.commit()

# Test 1: Check the total number of employees
def test_employee_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM employee")
    result = cursor.fetchone()[0]
    assert result == 10, f"Expected 10 employees, got {result}"


# Test 2: Verify all employees with managers have valid manager_id
def test_valid_managers(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
    SELECT e1.employee_id, e1.manager_id
    FROM employee e1
    LEFT JOIN employee e2 ON e1.manager_id = e2.employee_id
    WHERE e1.manager_id IS NOT NULL AND e2.employee_id IS NULL
    """)
    result = cursor.fetchall()
    assert len(result) == 0, "All managers should exist in the employee table"


# Test 3: Verify that Jane Smith has no manager
def test_ceo_has_no_manager(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
    SELECT employee_id FROM employee 
    WHERE first_name = 'Jane' AND last_name = 'Smith' AND manager_id IS NULL
    """)
    result = cursor.fetchone()
    assert result is not None, "Expected Jane Smith to have no manager"


# Test 4: Check the total number of expenses
def test_expense_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM expense")
    result = cursor.fetchone()[0]
    assert result == 5, f"Expected 5 expenses, got {result}"


# Test 5: Calculate the total expenses for employee 1 (John Doe)
def test_total_expense_for_employee(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
    SELECT SUM(unit_price * quantity) AS total_expense
    FROM expense
    WHERE employee_id = 1
    """)
    result = cursor.fetchone()[0]
    assert result == 201.00, f"Expected total expense of 201.00 for employee 1, got {result}"


# Test 6: Check for invalid expense data (negative or zero quantities)
def test_invalid_quantities(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM expense WHERE quantity <= 0")
    result = cursor.fetchall()
    assert len(result) == 0, "Expected no invalid quantities (<= 0) in expense data"


# Test 7: Check for invalid expense data (negative or zero unit prices)
def test_invalid_unit_price(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM expense WHERE unit_price <= 0")
    result = cursor.fetchall()
    assert len(result) == 0, "Expected no invalid unit prices (<= 0) in expense data"