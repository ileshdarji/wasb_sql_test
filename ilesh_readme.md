# SQL Test Solution for SilverBullet

## Overview

This repository contains the solution for the SilverBullet SQL test, including SQL scripts, test data, and automated test cases. The primary tasks involve:

1. **Creating and managing employee and expense data**
2. **Handling supplier invoices and generating payment plans**
3. **Finding employee-manager cycles in a recursive hierarchy**
4. **Validating data consistency and integrity**

Additional Python test scripts were also added using **pytest** to verify the SQL logic programmatically, providing a complete testing environment.

---

## Solution Breakdown

### SQL Files

1. **`create_employees.sql`**: Creates and populates the employee table with necessary data for testing employee-manager relationships.
2. **`create_expenses.sql`**: Creates and populates the expense table with necessary data for testing expense-related logic.
3. **`create_invoices.sql`**: Creates and populates the invoice table with invoice data linked to suppliers.
4. **`find_manager_cycles.sql`**: Detects cycles in the employee-manager hierarchy using recursive SQL queries.
5. **`generate_supplier_payment_plans.sql`**: Generates a monthly payment plan for suppliers based on outstanding invoices.
6. **`test_data_validation.sql`**: Provides SQL queries to validate the integrity of the data in the employee and invoice tables.

### Python Test Suite

- **`tests/test_sexi_db.py`**:
   - Tests the SQL scripts using the **Trino** database connector.
   - Each test checks specific business logic, such as:
     - Employee count and integrity.
     - Expense calculations.
     - Manager cycle detection.
     - Supplier payment plan generation.

---

## Prerequisites

- **Python** (version 3.10 or higher recommended)
- **Docker** (to run the Trino container)
- **pytest** (for running automated tests)

---

## Setup Instructions

### 1. Running Trino in Docker

To run the Trino container, use the following command:

```bash
docker run -d --name sexi-silverbullet -p 8080:8080 trinodb/trino
```

Ensure that the container is running by checking with:

```bash
docker ps
```

### 2. Running the Python Test Suite
```bash
python -m venv venv
source venv/bin/activate  # for Linux/macOS
venv\Scripts\activate  # for Windows
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Running the Test Suite
Once the environment is set up, run the test suite using the following command:

```bash
pytest
```
Alternatively, you can run individual test cases using:

```bash
pytest tests/test_sexi_db.py::test_employee_count
```

The test suiot covers multiple scenarios:

- validating employee data
- calculating expenses
- detecting manager cycles
- generating supplier payment plans

### 4. Data Validation Queries

For manual validation, you can use the SWL queries in the `test_data_validation.sql` file to check the integrity of the employee and invoice data.

### Additional Considerations:
- **Attention to Detail**: the solution ensures optimal SQL queries, proper documentation and detailed test cases.
- **Pull Requests:** The branch feature/sexi-expense-solution contains all changes
- **Comments and Explainations:** throughought the SQL and Python files, comments are provided to explain each part of the solution.
- **Dockerization**: The solution can be Dockerized for easier setup and deployment. By containerizing the environment, you ensure the entire solution can run consistently across any system. Future steps might include creating a Dockerfile and ensuring smooth integration with the Trino service running in the container. This makes the solution portable and easy to distribute without manual installation of dependencies.



