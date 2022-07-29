drop function IF EXISTS fn_class_information_import_temp_confirm(INT, INT, TEXT);
create or replace function fn_class_information_import_temp_confirm
  (b_import_id int, b_user_id int, b_action TEXT)
      RETURNS VOID
LANGUAGE plpgsql
as $$
DECLARE rec record;
begin
        with
        category_import_temp_insert as
        (
        select import_temp.id, import_temp.class_id, import_temp.name, import_temp.birthday,
                import_temp.age, import_temp.address, import_temp.import_error, import_temp.import_status

        from student_information_temp import_temp

        where import_temp.class_id = b_import_id

        )
        insert into student_information
            (class_id, name, birthday, age, address, import_error,import_status)
        select
           b_import_id,
		   tbl_import_temp.name, tbl_import_temp.birthday,
            tbl_import_temp.age, tbl_import_temp.address,  tbl_import_temp.import_error, tbl_import_temp.import_status
        FROM category_import_temp_insert AS tbl_import_temp
        where tbl_import_temp.class_id = b_import_id;
END;
$$;