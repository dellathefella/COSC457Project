SELECT
	code,
	title
FROM
	Course_christian
WHERE
	dep_num = (
		SELECT
			dep_num
		FROM
			Department_christian
		WHERE
			name = 'Business'
	)
	AND code IN (
		SELECT
			course_code
		FROM
			Section_christian
		WHERE
			DAYOFYEAR(date_start) >= DAYOFYEAR('2020-01-01')
			AND DAYOFYEAR(date_end) <= DAYOFYEAR('2020-12-31')
	);