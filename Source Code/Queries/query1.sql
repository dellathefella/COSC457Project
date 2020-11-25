SELECT
	title
FROM
	Course_christian
WHERE
	code IN (
		SELECT
			course_code
		FROM
			Program_Courses_christian
		WHERE
			program_id = (
				SELECT
					id
				FROM
					Program_christian
				WHERE
					name = 'Cybersecurity'
			)
	);