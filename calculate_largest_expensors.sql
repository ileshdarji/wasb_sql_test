-- Query to find employees who have expensed more than 1000
-- Include employee and manager details, order by total_expensed_amount in descending order

SELECT e1.employee_id,
       CONCAT(e1.first_name, ' ', e1.last_name) AS employee_name,
       e1.manager_id,
       CONCAT(e2.first_name, ' ', e2.last_name) AS manager_name,
       SUM(ex.unit_price * ex.quantity) AS total_expensed_amount
FROM employee e1
JOIN expense ex ON e1.employee_id = ex.employee_id
LEFT JOIN employee e2 ON e1.manager_id = e2.employee_id
GROUP BY e1.employee_id, e1.first_name, e1.last_name, e1.manager_id, e2.first_name, e2.last_name
HAVING SUM(ex.unit_price * ex.quantity) > 1000
ORDER BY total_expensed_amount DESC;


-- expected response:
-- employee_id | employee_name | manager_id | manager_name | total_expensed_amount
-- -------------+---------------+------------+--------------+-----------------------
--            2 | Jane Smith    |       NULL | NULL         |               1500.00