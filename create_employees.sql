-- Create the EMPLOYEE table to store employee information
CREATE TABLE employee (
    employee_id TINYINT,       -- Unique ID for each employee
    first_name VARCHAR,        -- Employee's first name
    last_name VARCHAR,         -- Employee's last name
    manager_id TINYINT         -- ID of the manager for this employee (can be NULL if no manager)
);

-- Insert sample employee data into the EMPLOYEE table
-- Each employee has an ID, first name, last name, and manager_id (if applicable)
INSERT INTO employee (employee_id, first_name, last_name, manager_id)
VALUES
(1, 'John', 'Doe', 2),          -- Employee 1 reports to Manager 2
(2, 'Jane', 'Smith', NULL),     -- Employee 2 has no manager (possibly the CEO)
(3, 'Alex', 'Johnson', 2),      -- Employee 3 reports to Manager 2
(4, 'Emily', 'Davis', 1),       -- Employee 4 reports to Manager 1
(5, 'Michael', 'Brown', 3),     -- Employee 5 reports to Manager 3
(6, 'Emma', 'Wilson', 3),       -- Employee 6 reports to Manager 3
(7, 'Oliver', 'Taylor', 4),     -- Employee 7 reports to Manager 4
(8, 'Isabella', 'Clark', 1),    -- Employee 8 reports to Manager 1
(9, 'Liam', 'Garcia', 5),       -- Employee 9 reports to Manager 5
(10, 'Sophia', 'Martinez', 6);  -- Employee 10 reports to Manager 6