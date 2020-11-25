SELECT first_name, last_name 
FROM issued_id 
WHERE gender = "F" AND id IN (
SELECT issued_id
FROM enrolled_programs
WHERE title = 'Marmota caligata' );