SELECT
	fname,
	mname,
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
			)
			AND DATEDIFF("2020-08-24", date_hired) >= 1826
	);