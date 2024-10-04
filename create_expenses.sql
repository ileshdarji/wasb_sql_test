-- Create the EXPENSE table
CREATE TABLE IF NOT EXISTS expense (
    employee_id TINYINT,         -- ID of the employee who made the expense
    unit_price DECIMAL(8, 2),    -- Price per unit of the item purchased
    quantity TINYINT             -- Quantity of the item purchased
);

-- Insert data into the EXPENSE table
INSERT INTO expense (employee_id, unit_price, quantity)
VALUES
(1, 100.50, 2),     -- Sample data for John Doe
(2, 500.00, 3),     -- Sample data for Jane Smith
(3, 50.00, 1),      -- Sample data for Alex Johnson
(4, 200.25, 4),     -- Sample data for Emily Davis
(5, 10.75, 6);      -- Sample data for Michael Brown