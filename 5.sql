SELECT first_name, last_name, id
FROM issued_id 
WHERE id in (
SELECT student_id
FROM advises
WHERE advise_id = (
SELECT issued_id
FROM issued_id 
WHERE last_name = "Lynes"));