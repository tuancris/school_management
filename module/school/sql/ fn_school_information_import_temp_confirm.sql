drop function IF EXISTS fn_school_information_import_temp_confirm(INT, INT, TEXT);
create or replace function fn_school_information_import_temp_confirm
  (b_import_id int, b_user_id int, b_action TEXT)
      RETURNS VOID
LANGUAGE plpgsql
as $$
DECLARE rec record;
begin
        with
        category_import_temp_insert as
        (
        select import_temp.id, import_temp.school_id,import_temp.cla_id, import_temp.name, import_temp.mainteacher,
                import_temp.grade,import_temp.import_error, import_temp.import_status

        from class_information_temp import_temp

        where import_temp.school_id = b_import_id

        )
        insert into class_information
            (school_id, cla_id, name, mainteacher, grade, import_error,import_status)
        select
           b_import_id,  tbl_import_temp.cla_id,
		   tbl_import_temp.name, tbl_import_temp.mainteacher,
            tbl_import_temp.grade, tbl_import_temp.import_error, tbl_import_temp.import_status
        FROM category_import_temp_insert AS tbl_import_temp
        where tbl_import_temp.school_id = b_import_id;
END;
$$;