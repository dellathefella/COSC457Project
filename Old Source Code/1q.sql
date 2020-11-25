SELECT 
	title
FROM 
	offered_courses
WHERE
	program_id in (SELECT
			program_id
		FROM
			offered_programs
		WHERE
			title = 'Dasypus novemcinctus');