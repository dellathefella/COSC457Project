SELECT title 
FROM offered_courses
WHERE semester_title = "Spring 2020" AND department_id IN (
SELECT department_id 
FROM department 
WHERE name = "Desert tortoise");