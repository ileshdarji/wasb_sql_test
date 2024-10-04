-- Query to find cycles in the employee-manager relationship
WITH RECURSIVE ManagerHierarchy AS (
    -- Start with all employees and their direct managers
    SELECT employee_id, manager_id, ARRAY[employee_id] AS path
    FROM employee
    WHERE manager_id IS NOT NULL
    UNION ALL
    -- Recursively follow the management chain
    SELECT e.employee_id, e.manager_id, mh.path || e.employee_id
    FROM employee e
    JOIN ManagerHierarchy mh ON e.manager_id = mh.employee_id
    WHERE NOT contains(mh.path, e.employee_id)  -- Prevent loops in recursion
)
-- Find any cycles where an employee ends up managing themselves
SELECT DISTINCT employee_id, array_join(path, ', ') AS cycle
FROM ManagerHierarchy
WHERE contains(path, employee_id)
AND CARDINALITY(path) > 1;

-- expected response:
--   employee_id |  cycle
-- -------------+----------
--            5 | 3, 5
--            8 | 1, 8
--           10 | 6, 10
--            9 | 5, 9
--            4 | 1, 4
--            7 | 1, 4, 7
--            7 | 4, 7
--            6 | 3, 6
--            9 | 3, 5, 9
--           10 | 3, 6, 10
-- (10 rows)