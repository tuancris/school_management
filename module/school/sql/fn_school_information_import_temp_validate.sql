drop function IF EXISTS fn_school_information_import_temp_validate( INT);
create or replace function fn_school_information_import_temp_validate
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

    update class_information_temp set import_error='', import_status='none'
	    where school_id=b_import_id;

	with data_validate as
	(
        SELECT import_temp.id, import_temp.school_id, import_temp.cla_id, import_temp.name, import_temp.mainteacher,
            import_temp.grade

        FROM class_information_temp import_temp
        WHERE import_temp.school_id = b_import_id
	),

	validate_grade_length as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','tên khối vượt quá 25 kí tự'
        from data_validate tb1
        Where LENGTH(tb1.grade) > 25


	),
	validate_regex_name as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','tên lớp không đúng quy tắc'
        from data_validate tb1
        Where tb1.name ~ '/^[a-zA-Z0-9]+$/'

	),
	validate_regex_grade as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','tên khối không đúng quy tắc'
        from data_validate tb1
        Where tb1.grade ~ '/^\d+$/'

	),

	validate_name_empty  as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','Tên lớp không được để trống'
        from data_validate tb1
        Where trim(tb1.name) = ''
	),
	validate_name_length as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','Tên gọi vượt quá 25 kí tự'
        from data_validate tb1
        Where LENGTH(tb1.name) > 25
	),


	validate_mainteacher_length as
	(
        insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
        Select tb1.id,'fail','tên giáo viên vượt quá 255 kí tự'
        from data_validate tb1
        Where LENGTH(tb1.mainteacher) > 255
	)
	insert into supplies_category_temp_validate (item_id, validate_status, validate_error)
	Select tb1.id,'fail','Tất cả mã lớp đều bỏ trống' from data_validate tb1
	where
        (tb1.name IS NULL and tb1.mainteacher IS NULL and tb1.grade IS NULL)
        OR
        (tb1.name ='' and tb1.mainteacher ='' and tb1.grade ='' );
	b_fail = count(distinct item_id) from supplies_category_temp_validate;
	with merge_notes as
			(select item_id, validate_status, string_agg(validate_error:: TEXT, ', ') validate_error
			from supplies_category_temp_validate group by item_id, validate_status)
	update class_information_temp set import_error=tb1.validate_error, import_status=tb1.validate_status
	from merge_notes tb1
	where tb1.item_id=class_information_temp.id;

	RETURN QUERY

   SELECT b_pass :: INT r_pass, b_fail  :: INT r_fail ;

END;
$$;