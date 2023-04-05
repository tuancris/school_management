DROP FUNCTION IF EXISTS fn_school_information_import_temp(JSON, INT, INT);
CREATE OR REPLACE FUNCTION fn_school_information_import_temp
  (b_json_data JSON, b_user_id INT, b_import_id INT)
      RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
	Delete from class_information_temp where school_id=b_import_id ;
	with data_import as
	(
		Select *
		  from json_to_recordset(b_json_data)
			AS x(
			    "cla_id" TEXT,
				"name" TEXT,
				"mainteacher" TEXT,
				"grade" TEXT
			)
	),
	data_insert as (

	    SELECT tb1.cla_id, tb1.name, tb1.mainteacher, tb1.grade
		FROM data_import tb1

	)
	insert into class_information_temp
	    ( school_id,cla_id, name, mainteacher, grade)
    Select
            b_import_id, trim(cla_id) ,trim(name), trim(mainteacher), trim(grade)
        from data_insert;
END;
$$;