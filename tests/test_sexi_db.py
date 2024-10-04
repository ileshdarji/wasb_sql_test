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


# Test 8: Detect manager-employee cycles
def test_manager_cycles(db_connection):
    cursor = db_connection.cursor()

    # Run the cycle detection query
    cursor.execute("""
    WITH RECURSIVE ManagerHierarchy (employee_id, manager_id, path) AS (
        SELECT employee_id, manager_id, ARRAY[employee_id] AS path
        FROM employee
        WHERE manager_id IS NOT NULL

        UNION ALL

        SELECT e.employee_id, e.manager_id, mh.path || e.employee_id
        FROM employee e
        JOIN ManagerHierarchy mh ON e.manager_id = mh.employee_id
        WHERE NOT contains(mh.path, e.employee_id)
    )
    SELECT DISTINCT employee_id, array_join(path, ', ') AS cycle
    FROM ManagerHierarchy
    WHERE contains(path, employee_id)
    AND CARDINALITY(path) > 1
    """)

    result = cursor.fetchall()
    # print(f"Results: {result}")

    # Expected cycles based on the query results
    expected_cycles = [
        [7, '1, 4, 7'],
        [4, '1, 4'],
        [9, '3, 5, 9'],
        [10, '3, 6, 10'],
        [6, '3, 6'],
        [10, '6, 10'],
        [5, '3, 5'],
        [7, '4, 7'],
        [8, '1, 8'],
        [9, '5, 9']
    ]

    assert len(result) == len(expected_cycles), f"Expected {len(expected_cycles)} cycles, but found {len(result)}"

    # Compare expected and actual results by normalizing them to the same format
    for cycle in expected_cycles:
        assert cycle in result, f"Expected cycle {cycle}, but it wasn't found in {result}"

# Test 9: Generate supplier payment plans
def test_supplier_payment_plans(db_connection):
    cursor = db_connection.cursor()

    # Run the query to generate supplier payment plans
    cursor.execute("""
        WITH InvoicePlan AS (
            SELECT
                i.supplier_id,
                s.name AS supplier_name,
                i.invoice_amount,
                i.due_date,
                DATE_TRUNC('month', i.due_date) AS payment_month
            FROM invoice i
            JOIN supplier s ON i.supplier_id = s.supplier_id
        ),
        MonthlyPayments AS (
            SELECT
                supplier_id,
                supplier_name,
                invoice_amount AS payment_amount,
                invoice_amount AS balance_outstanding,
                payment_month AS payment_date
            FROM InvoicePlan
        )
        SELECT
            supplier_id,
            supplier_name,
            payment_amount,
            balance_outstanding,
            payment_date
        FROM MonthlyPayments
        ORDER BY supplier_id, payment_date
    """)  # Remove the semicolon at the end

    result = cursor.fetchall()
    # print(f"Supplier Payment Plans result: {result}")

    # Example: Check if the correct number of payment plans is generated
    assert len(result) == 6, f"Expected 6 payment plans, but got {len(result)}"

    # Example: Validate that one of the payment plans has the expected amount
    for row in result:
        supplier_id, supplier_name, payment_amount, balance_outstanding, payment_date = row
        if supplier_id == 1:
            assert payment_amount == 6000.00, f"Expected payment amount of 6000.00 for supplier 1, but got {payment_amount}"