from odoo import api, fields, models
from odoo.odoo.exceptions import UserError


class StudentInformationTemp(models.Model):
    _name = "student.information.temp"
    _description = "Student Management"

    stu_id = fields.Char(string='Mã sinh viên')
    name = fields.Char(string='Họ Và Tên')
    birthday = fields.Date(string='Ngày sinh')
    age = fields.Char(string='Tuổi')
    address = fields.Char(string='Địa chỉ')
    import_error = fields.Char(string='Error')
    import_status = fields.Char(string='Status')
    class_id = fields.Many2one('class.information', string='Lớp', ondelete='cascade')
    school_id = fields.Many2one('school.information', string='Trường', ondelete='cascade')
