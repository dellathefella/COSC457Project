SELECT
	fname,
	lname
FROM
	Id_christian
WHERE
	sex = "F"
	AND id IN (
		SELECT
			id_card
		FROM
			Student_christian
		WHERE
			id IN (
				SELECT
					student_id
				FROM
					Program_Enrollment_christian
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
	);