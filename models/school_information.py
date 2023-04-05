import base64
import tempfile
import json
import time
import functools

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


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        val = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"Finished running {func.__name__} in {run_time:.4f} seconds.")
        return val

    return wrapper




class SchoolInformation(models.Model):
    _name = "school.information"
    _description = "School Information"

    sch_id = fields.Char(string='Mã trường', required=True)
    name = fields.Char(string='Tên trường', required=True)
    type = fields.Selection([('private', 'Dân lập'), ('public', 'Công lập')], default='public', string='Loại trường')
    email = fields.Text(string='Email')
    address = fields.Text(string='Địa chỉ')
    phoneNu = fields.Char(string='Số điện thoại ')
    hasOnlineClass = fields.Boolean(string='Có lớp online không?')
    rank = fields.Integer(string='Xếp hạng')
    establishDay = fields.Date(string='Ngày thành lập')
    document = fields.Binary(string='Tài liệu về trường')
    document_name = fields.Char(string='Tên tài liệu')
    tuition = fields.Char(compute='_auto_count_tuition', string='Học phí')

    class_list = fields.One2many('class.information', 'school_id', string='Danh sách lớp học', required=True,  ondelete='cascade')


    _sql_constraints = [
        (
            'unique_duplicate_school',
            'UNIQUE(sch_id)',
            'Mã trường bị trùng',
        ),
    ]

    @api.depends('type')
    def _auto_count_tuition(self):
        for re in self:
            if re.type == 'private':
                re.tuition = '2.000.000'
            else:
                re.tuition = '1.000.000'



    @timer
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
                    'cla_id': json_row[0],
                    'name': json_row[1],
                    'mainteacher': json_row[2],
                    'grade': remove_dot_zeros_float(json_row[3]),

                }
                _category_list.append(_json_ob)
            print(_category_list)
            if len(_category_list) > 0:
                # Xử lý dữ liệu import
                print("insert vào db")
                b_json_data = json.dumps(_category_list)
                string_sql_insert_json = '''SELECT * FROM fn_school_information_import_temp(%s,%s,%s);'''
                self.env.cr.execute(string_sql_insert_json,
                                    (b_json_data, self._uid, self.id))
                # region: validate
                str_cr = '''SELECT * FROM fn_school_information_import_temp_validate(%s);'''
                self.env.cr.execute(str_cr, (self.id,))
                res = self.env.cr.dictfetchall()
                print(res)
                # endregion
                b_action = '''insert'''
                str_cf = '''SELECT * FROM fn_school_information_import_temp_confirm(%s,%s,%s);'''
                self.env.cr.execute(str_cf, (self.id, self._uid, b_action))
        except Exception as e:
            print(e)
            raise ValidationError(u'File import chưa đúng định dạng file mẫu, vui lòng kiểm tra lại!')



if __name__ == '__main__':
    calc = SchoolInformation()
    calc.btn_upload_data(10)