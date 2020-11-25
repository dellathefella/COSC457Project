SELECT
	grade
FROM
	Student_Sections_christian
WHERE
	student_id = 1
	AND section_id IN (
		SELECT
			id
		FROM
			Section_christian
		WHERE
			date_start >= "2020-08-24"
			AND date_end <= "2020-12-14"
	);