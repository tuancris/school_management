drop function IF EXISTS fn_class_information_import_temp_validate( INT);
create or replace function fn_class_information_import_temp_validate
  ( b_import_id int)
      RETURNS TABLE (r_pass int,r_fail int)
LANGUAGE plpgsql
as $$
DECLARE b_total int = 0;
        b_pass int = 0;
		b_fail int = 0;
begin

	CREATE TEMP TABLE IF NOT EXISTS supplies_category_temp_validate (item_id INTEGER, validate_status TEXT, validate_error TEXT);
	DELETE FROM supplies_category_temp_validate;

    update student_information_temp set import_error='', import_status='none'
	    where class_id=b_import_id;

	with data_validate as
	(
        SELECT import_temp.id, import_temp.class_id, import_temp.stu_id, import_temp.name, import_temp.birthday,
            import_temp.age, import_temp.address

        FROM student_information_temp import_temp
        WHERE import_temp.class_id = b_import_id
	),

	validate_grade_length as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','tên sinh viên vượt quá 255 kí tự'
        from data_validate tb1
        Where LENGTH(tb1.name) > 255


	),

	validate_regex_grade as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','số tuổi chỉ gồm số không chữ'
        from data_validate tb1
        Where tb1.age ~ '/^\d+$/'

	),

	validate_name_empty  as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','Tên sinh viên không được để trống'
        from data_validate tb1
        Where trim(tb1.name) = ''
	),
	validate_name_length as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','Tên địa chỉ vượt quá 255 kí tự'
        from data_validate tb1
        Where LENGTH(tb1.address) > 255
	)



	insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
	Select tb1.id,'fail','Tất cả mã sinh viên đều bỏ trống' from data_validate tb1;

	b_fail = count(distinct item_id) from supplies_category_temp_validate;
	with merge_notes as
			(select item_id, validate_status, string_agg(validate_error:: TEXT, ', ') validate_error
			from supplies_category_temp_validate group by item_id, validate_status)
	update student_information_temp set import_error=tb1.validate_error, import_status=tb1.validate_status
	from merge_notes tb1
	where tb1.item_id=student_information_temp.id;

	RETURN QUERY

   SELECT b_pass :: INT r_pass, b_fail  :: INT r_fail ;

END;
$$;