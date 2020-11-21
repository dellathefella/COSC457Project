SELECT
	fname,
	lname
FROM
	Id_christian
WHERE
	id IN (
		SELECT
			id_card
		FROM
			Staff_christian
		WHERE
			id IN (
				SELECT
					instructor_id
				FROM
					Section_christian
				WHERE
					course_code IN (
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
									name = "Bachelor's in Computer Science"
							)
					)
			)
	);