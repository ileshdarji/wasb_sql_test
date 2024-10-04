-- Generate payment plans for suppliers
WITH InvoicePlan AS (
    -- Calculate the total amount of invoices for each supplier
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
    -- Calculate the monthly payment plan for each supplier
    SELECT
        supplier_id,
        supplier_name,
        invoice_amount AS payment_amount,
        invoice_amount AS balance_outstanding,
        payment_month AS payment_date
    FROM InvoicePlan
)
-- Output the final payment plan
SELECT
    supplier_id,
    supplier_name,
    payment_amount,
    balance_outstanding,
    payment_date
FROM MonthlyPayments
ORDER BY supplier_id, payment_date;


-- expected response:
--  supplier_id |     supplier_name     | payment_amount | balance_outstanding | payment_date
-- -------------+-----------------------+----------------+---------------------+--------------
--            1 | Awesome Animals       |        6000.00 |             6000.00 | 2024-12-01
--            2 | Brilliant Bottles     |        2000.00 |             2000.00 | 2024-11-01
--            3 | Crazy Catering        |        1500.00 |             1500.00 | 2024-12-01
--            4 | Dave's Discos         |         500.00 |              500.00 | 2024-10-01
--            5 | Entertainment Tonight |        6000.00 |             6000.00 | 2024-12-01
--            6 | Ice Ice Baby          |        4000.00 |             4000.00 | 2025-03-01
-- (6 rows)