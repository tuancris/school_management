from odoo import api, fields, models


class ClassInformationTemp(models.Model):
    _name = "class.information.temp"
    _description = "Class Management"

    cla_id = fields.Char(string='Mã lớp',require=True)
    name = fields.Char(string='Tên lớp', require=True)
    grade = fields.Char(string='Khối', require=True)
    mainteacher = fields.Char(string='GVCN', require=True)
    import_error = fields.Char(string='Error', require=True)
    import_status = fields.Char(string='Status', require=True)
    school_id = fields.Many2one('school.information', string=' Trường', require=True, ondelete='cascade')
    student_list = fields.One2many('student.information', 'class_id', string="Danh sách sinh viên", require=True, ondelete='cascade')

    # _sql_constraints = [
    #     (
    #         'unique_duplicate_class',
    #         'UNIQUE(cla_id)',
    #         'Mã lớp bị trùng',
    #     ),
    # ]
