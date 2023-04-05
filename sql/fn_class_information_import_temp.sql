DROP FUNCTION IF EXISTS fn_class_information_import_temp(JSON, INT, INT);
CREATE OR REPLACE FUNCTION fn_class_information_import_temp
  (b_json_data JSON, b_user_id  INT, b_import_id INT)
      RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
	Delete from student_information_temp where class_id=b_import_id   ;
	with data_import as
	(
		Select *
		  from json_to_recordset(b_json_data)
			AS x(
				"stu_id" TEXT
			)
	),

	data_import_sv as (
	    select dip.stu_id, sinfo.name, sinfo.birthday, sinfo.age, sinfo.address
		from data_import dip
	    LEFT JOIN student_information sinfo on dip.stu_id = sinfo.stu_id
	),

	data_insert as (

	    SELECT tb1.stu_id, tb1.name, tb1.birthday,  tb1.age, tb1.address
		FROM data_import_sv tb1

	)
	insert into student_information_temp
	    (  class_id, stu_id, name, birthday, age, address)
    Select
           b_import_id, trim(stu_id), name, birthday, age, address
    from data_insert ;


END;
$$;