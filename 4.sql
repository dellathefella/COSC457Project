SELECT first_name, last_name, id
FROM issued_id 
WHERE id in (
SELECT issued_id
FROM advises);