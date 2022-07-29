from odoo import api, fields, models
from odoo.odoo.exceptions import UserError


class StudentInformation(models.Model):
    _name = "student.information"
    _description = "Student Management"

    stu_id = fields.Char(string='Mã sinh viên')
    name = fields.Char(string='Họ Và Tên', required=True)
    birthday = fields.Date(string='Ngày sinh', required=True)
    age = fields.Char(string='Tuổi', required=True)
    address = fields.Char(string='Địa chỉ', required=True)
    import_error = fields.Char(string='Error')
    import_status = fields.Char(string='Status')
    class_id = fields.Many2one('class.information', string='Lớp', ondelete='cascade')
    school_id = fields.Many2one('school.information', string='Trường', required = True, ondelete='cascade')
    subject_list = fields.Many2many("subject.information", 'relation_subject_student' ,  'student_id', 'subject_id', string='Bảng quan hệ môn học và học sinh')

    _sql_constraints = [
        (
            'unique_duplicate_student',
            'UNIQUE(stu_id)',
            'Mã sinh viên bị trùng',
        ),
    ]

    def write(self, values):
        rtn = super(StudentInformation, self).write(values)
        if not self.subject_list:
            raise UserError("Bạn cần chọn môn học")
        return rtn








class SubjectInformation(models.Model) :
    _name = "subject.information"
    _description = "Subject Information"

    name = fields.Char(string='Tên môn học')
    room = fields.Char(string='Phòng học')
    thu = fields.Char(string='Thứ ')
    start_day = fields.Date(string='Ngày bắt đầu')
    end_day   = fields.Date(string='Ngày kết thúc')
    start_time = fields.Char(string='Thời gian bắt đầu')
    end_time = fields.Char(string='Thời gian kết thúc')
