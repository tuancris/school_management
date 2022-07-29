import base64
import tempfile
import json

import self as self
import xlrd
from io import BytesIO
import xlsxwriter
import re

from odoo import api, fields, models
from odoo.odoo.exceptions import ValidationError


def remove_dot_zeros_float(float_param):
    if isinstance(float_param, float):
        if float(float_param) == int(float_param):
            return int(float_param)
        else:
            return float(float_param)
    else:
        return float_param


class ClassInformation(models.Model):
    _name = "class.information"
    _description = "Class Management"

    cla_id = fields.Char(string='Mã lớp', required=True)
    name = fields.Char(string='Tên lớp', required=True)
    grade = fields.Char(string='Khối', require=True)
    mainteacher = fields.Char(string='GVCN', required=True)
    document = fields.Binary(string='Tài liệu về lớp')
    document_name = fields.Char(string='Tên tài liệu')
    import_error = fields.Char(string='Error')
    import_status = fields.Char(string='Status')
    school_id = fields.Many2one('school.information', string=' Trường', required=True, ondelete='cascade')
    student_list = fields.One2many('student.information', 'class_id', string="Danh sách sinh viên", require=True,
                                   ondelete='cascade')

    _sql_constraints = [
        (
            'unique_duplicate_class',
            'UNIQUE(cla_id)',
            'Mã lớp bị trùng',
        ),
    ]

    def btn_upload_data(self):
        if not self.document:
            raise ValidationError(u'Chưa chọn file import.')
        tmp = self.document_name.split('.')
        if len(tmp) <= 1:
            raise ValidationError(u"Tệp tin tải lên phải là file excel, theo mẫu")
        ext = tmp[len(tmp) - 1]
        if ext != 'xls' and ext != 'xlsx':
            raise ValidationError(u"Tệp tin tải lên phải là file excel, theo mẫu")

        data = base64.decodebytes(self.document)
        fobj = tempfile.NamedTemporaryFile(delete=False)
        fname = fobj.name
        fobj.write(data)
        fobj.close()
        row_start = 1

        xl_workbook = xlrd.open_workbook(fname, on_demand=True)
        current_sheet = xl_workbook.sheet_by_index(0)
        _category_list = []

        try:
            for row in range(row_start, current_sheet.nrows):
                json_row = current_sheet.row_values(row)
                _json_ob = {
                    # 'school_id' : remove_dot_zeros_float(json_row[0]),
                    'stu_id': json_row[0],
                }
                _category_list.append(_json_ob)
            print(_category_list)
            if len(_category_list) > 0:
                # Xử lý dữ liệu import
                print("insert vào db")
                b_json_data = json.dumps(_category_list)
                string_sql_insert_json = '''SELECT * FROM fn_class_information_import_temp(%s,%s,%s);'''
                self.env.cr.execute(string_sql_insert_json,
                                    (b_json_data, self._uid, self.id))
                # region: validate
                str_cr = '''SELECT * FROM fn_class_information_import_temp_validate(%s);'''
                self.env.cr.execute(str_cr, (self.id,))
                res = self.env.cr.dictfetchall()
                print(res)
                # endregion
                b_action = '''insert'''
                str_cf = '''SELECT * FROM fn_class_information_import_temp_confirm(%s,%s,%s);'''
                self.env.cr.execute(str_cf, (self.id, self._uid, b_action))




        except Exception as e:
            print(e)
            raise ValidationError(u'File import chưa đúng định dạng file mẫu, vui lòng kiểm tra lại!')
