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
			Student_christian
		WHERE
			advisor_id = (
				SELECT
					id
				FROM
					Staff_christian
				WHERE
					id_card = (
						SELECT
							id
						FROM
							Id_christian
						WHERE
							fname = "Steve"
							AND lname = "Silk"
					)
			)
	);