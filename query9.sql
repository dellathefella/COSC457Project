SELECT
	fname,
	mname,
	lname
FROM
	Id_christian
WHERE
	id = (
		SELECT
			id_card
		FROM
			Student_christian
		WHERE
			id = 1
	);