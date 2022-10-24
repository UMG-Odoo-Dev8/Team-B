import string
from odoo import models,fields,api
from datetime import datetime,date

from odoo.exceptions import AccessError, UserError

class AttendanceModel(models.Model):
    '''Defining Monthly Attendance sheet Information.'''

    _name = 'sl.attendance'
    _description = 'Student Attendance'
    _rec_name = 'attendance_date'

    section_name = fields.Many2one('sl.section', string="Academic Section")
    teacher_head = fields.Char(string="Head Teacher")
    attendance_date = fields.Date(string="Attendance Date")

    attendance_ids = fields.One2many('sl.attendance.line','attendance_id','Attendance Student')
    
    # Retrieving students to one2many field
    @api.onchange('section_name')
    def add_custom_section_name(self):
        if self.section_name:
            self.teacher_head = self.section_name.head_teacher_id.name
            self.attendance_ids = [(5,0,0)]
            std_ids = self.env['sl.section.line'].search([])
            if std_ids:
                for std in std_ids:
                    if self.section_name.section_name==std.section_id.section_name:
                        vals = {
                        'student_name': std.student_id.name,
                        'student_id' : int(std.student_id),
                        'roll_no': std.roll_no
                        }
                        self.update({'attendance_ids':[(0, 0, vals)]})

class AttendanceLine(models.Model):
    _name = 'sl.attendance.line'
    _description = 'Attendance Model Line'

    attendance_id = fields.Many2one('sl.attendance','Attendance Student Line')

    student_id = fields.Char(string="Student ID")
    student_name = fields.Char(string="Student Name")
    roll_no = fields.Char(string="Roll No")
    morning_attendance = fields.Boolean("Morning Attendance")
    afternoon_attendance = fields.Boolean("Afternoon Attendance")
    leave = fields.Boolean("Leave")
    point = fields.Float(string="Point", store="True", compute="_compute_point", readonly=True)

    @api.depends('morning_attendance', 'afternoon_attendance', 'leave')
    def _compute_point(self):
        for attendance in self:
            if not attendance.morning_attendance and not attendance.afternoon_attendance and not attendance.leave:
                # print(type(attendance.morning_attendance))
                # print(attendance.morning_attendance)
                attendance.point = 0
            elif not attendance.morning_attendance and not attendance.afternoon_attendance and attendance.leave:     
                attendance.point = 1
            elif attendance.morning_attendance and attendance.afternoon_attendance:
                attendance.point = 1
            elif (attendance.morning_attendance or attendance.afternoon_attendance) and not attendance.leave:     
                attendance.point = 0.5
            elif (attendance.morning_attendance or attendance.afternoon_attendance) and attendance.leave:
                attendance.point = 1
            else:
                return False

    