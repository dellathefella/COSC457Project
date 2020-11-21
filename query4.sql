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
					advisor_id
				FROM
					Department_christian
			)
			OR id IN (
				SELECT
					advisor_id
				FROM
					Student_christian
			)
	);