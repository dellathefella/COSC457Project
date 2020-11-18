SELECT
	first_name,
	last_name
FROM
	issued_id
WHERE
	(
		STATUS = "Instructor"
		OR STATUS = "Staff"
	)
	AND id IN (
		SELECT
			issued_id
		FROM
			offered_courses
		WHERE
			program_id = (
				SELECT
					program_id
				FROM
					offered_programs
				WHERE
					title = 'Hystrix indica'
			)
	);