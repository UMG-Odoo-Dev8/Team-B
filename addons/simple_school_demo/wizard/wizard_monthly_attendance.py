from odoo import models,fields,api

class StudentMonthAttendance(models.TransientModel):
    _name = 'month.attendance.wizard'
    _description = 'Student Month Attendance'

    academic_section = fields.Many2one('attendance.model',string="Academic Secton")
    att_month = fields.Selection([
        ('1','January'),
        ('2','February'),
        ('3','March'),
        ('4','April'),
        ('5','May'),
        ('6','June'),
        ('7','July'),
        ('8','August'),
        ('9','September'),
        ('10','October'),
        ('11','November'),
        ('12','December'),
    ])
    roll_no = fields.Many2one('attendance.model', string="Roll NO")