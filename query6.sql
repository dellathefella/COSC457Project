SELECT
	COUNT(student_id) AS num_students
FROM
	Student_Sections_christian
WHERE
	STATUS = "dropped"
	AND section_id IN (
		SELECT
			id
		FROM
			Section_christian
		WHERE
			course_code = "ARTS-101"
			AND date_start >= "2020-08-24"
			AND date_end <= "2020-12-14"
	);