-- Create the SUPPLIER table
CREATE TABLE IF NOT EXISTS supplier (
    supplier_id TINYINT,   -- ID for each supplier
    name VARCHAR           -- Supplier name
);

-- Insert supplier data (sorted alphabetically)
INSERT INTO supplier (supplier_id, name)
VALUES
(CAST(1 AS TINYINT), 'Awesome Animals'),
(CAST(2 AS TINYINT), 'Brilliant Bottles'),
(CAST(3 AS TINYINT), 'Crazy Catering'),
(CAST(4 AS TINYINT), 'Dave''s Discos'),  -- Escaped the apostrophe for Dave's Discos
(CAST(5 AS TINYINT), 'Entertainment Tonight'),
(CAST(6 AS TINYINT), 'Ice Ice Baby');

-- Create the INVOICE table
CREATE TABLE IF NOT EXISTS invoice (
    supplier_id TINYINT,         -- ID of the supplier (foreign key to SUPPLIER)
    invoice_amount DECIMAL(8, 2), -- Amount of the invoice
    due_date DATE                -- Due date of the invoice
);

-- Insert invoice data (ensure casting for TINYINT and using DATE literals)
INSERT INTO invoice (supplier_id, invoice_amount, due_date)
VALUES
(CAST(1 AS TINYINT), 6000.00, DATE '2024-12-31'),  -- Invoice for Awesome Animals
(CAST(2 AS TINYINT), 2000.00, DATE '2024-11-30'),  -- Invoice for Brilliant Bottles
(CAST(3 AS TINYINT), 1500.00, DATE '2024-12-31'),  -- Invoice for Crazy Catering
(CAST(4 AS TINYINT), 500.00, DATE '2024-10-31'),   -- Invoice for Dave's Discos
(CAST(5 AS TINYINT), 6000.00, DATE '2024-12-31'),  -- Invoice for Entertainment Tonight
(CAST(6 AS TINYINT), 4000.00, DATE '2025-03-31');  -- Invoice for Ice Ice Baby