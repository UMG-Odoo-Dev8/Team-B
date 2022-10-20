import string
from odoo import models,fields,api
from datetime import datetime,date

from odoo.exceptions import AccessError, UserError

class StudentAttendance(models.Model):
    '''Defining Monthly Attendance sheet Information.'''


    _name = 'attendance.model'
    _description = 'Student Attendance'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'attendance_date'

    teacher_head = fields.Char(string="Head Teacher")
    # roll_no = fields.Char(string="Roll No")
    attendance_id = fields.One2many('attendance.model.line','attendance_line_id','Attendance Student')
    attendance_date = fields.Date(string="Attendance Date")
    section_name = fields.Many2one('session.model', string="Academic Section")
    end_date = fields.Date(string="Leave End Date")
    leave_type = fields.Selection([
        ('sick','Sick Leave'),
        ('hospital','Hospital Leave'),
        ('family','Family Emergency')
    ], string="Leave Type")
    reason = fields.Text(string="Reason for Leave")
    half_day_leave = fields.Datetime(string="Half Day Leave")
    
    # Retrieving students to one2many field
    @api.onchange('section_name')
    def add_custom_section_name(self):
        self.teacher_head = self.section_name.head_teacher_id.name
        self.attendance_id = [(5,0,0)]
        std_ids = self.env['session.model.line'].search([])
        if std_ids:
            for std in std_ids:
                if self.section_name.section==std.parent_id.section:
                    vals = {
                    'student_id': std.student_id.name,
                    'roll_no': std.roll_no
                    }
                    self.update({'attendance_id':[(0, 0, vals)]})

    is_generate = fields.Boolean("Generate?")
    state = fields.Selection([('draft', 'Draft'), ('validate', 'Validate')],
            'State', readonly=True, default='draft')

    def attendance_validate(self):
        pass

    def attendance_draft(self):
        pass

class AttendanceLine(models.Model):
    _name = 'attendance.model.line'
    _description = 'Attendance Model Line'

    attendance_line_id = fields.Many2one('attendance.model','Attendance Student Line')
    student_id = fields.Char(string="Student Name")
    roll_no = fields.Char(string="Roll No")
    morning_attendance = fields.Boolean("Morning Attendance")
    afternoon_attendance = fields.Boolean("Afternoon Attendance")
    point = fields.Float(string="Point", store="True", compute="_compute_point", readonly=True)

    @api.depends('morning_attendance', 'afternoon_attendance')
    def _compute_point(self):
        for attendance in self:
            if not attendance.morning_attendance and not attendance.afternoon_attendance:
                print(type(attendance.morning_attendance))
                print(attendance.morning_attendance)
                attendance.point = 0
            elif attendance.morning_attendance and attendance.afternoon_attendance: 
                print(attendance.morning_attendance)         
                attendance.point = 1
            elif attendance.morning_attendance or attendance.afternoon_attendance:
                attendance.point = 0.5


class StudentLeaveRequest(models.Model):
    """Defining Model Student Leave Request."""

    _name = 'leave.studentrequest'
    _description = 'Student Leave Request'
    _inherit = ['mail.thread','mail.activity.mixin']

    section_id = fields.Many2one('session.model', string="Academic Section")
    student_id = fields.Many2one('attendance.model', string="Student Name")

    start_date = fields.Date(string="Leave Start Date")
    end_date = fields.Date(string="Leave End Date")
    total_leave_day = fields.Integer(string="Total Leave Days")


    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate', 'Approved')
        ], string='Status', store=True, default='confirm', tracking=True, copy=False, readonly=False,)

    can_reset = fields.Boolean('Can reset', compute='_compute_can_reset')
    can_approve = fields.Boolean('Can Approve', compute='_compute_can_approve')

    leave_type = fields.Selection([
        ('sick','Sick Leave'),
        ('hospital','Hospital Leave'),
        ('family','Family Emergency')
    ], string="Leave Type")
    reason = fields.Text(string="Reason for Leave")
    half_day_leave = fields.Datetime(string="Half Day Leave")

    roll_no = fields.Char(string="Roll No")

    # @api.onchange('student_id')
    # def _onchange_student_id(self):
    #     self.roll_no = self.student_id.roll_no


    @api.onchange('start_date', 'end_date', 'total_leave_day')
    def calculate_date(self):
        if self.start_date and self.end_date:
            s_date = datetime.strptime(str(self.start_date),'%Y-%m-%d')
            e_date = datetime.strptime(str(self.end_date),'%Y-%m-%d')
            t_date = e_date - s_date
            self.total_leave_day = str(t_date.days)

    @api.depends('state', 'student_id')
    def _compute_can_reset(self):
        for student in self:
            try:
                student._check_approval_update('draft')
            except (AccessError, UserError):
                student.can_reset = False
            else:
                student.can_reset = True

    @api.depends('state', 'student_id')
    def _compute_can_approve(self):
        for student in self:
            try:
                if student.state == 'confirm':
                    student._check_approval_update('validate')
            except (AccessError, UserError):
                student.can_approve = False
            else:
                student.can_approve = True

    def action_draft(self):
        pass
        # if any(student.state not in ['confirm', 'refuse'] for student in self):
        #     raise UserError(('Leave request state must be "Refused" or "To Approve" in order to be reset to draft.'))
        # self.write({
        #     'state': 'draft',
        # })
        # linked_requests = self.mapped('linked_request_ids')
        # if linked_requests:
        #     linked_requests.action_draft()
        #     linked_requests.unlink()
        # self.activity_update()
        # return True

    def action_confirm(self):
        pass
        # if self.filtered(lambda student: student.state != 'draft'):
        #     raise UserError(('Time off request must be in Draft state ("To Submit") in order to confirm it.'))
        # self.write({'state': 'confirm'})
        # students = self.filtered(lambda leave: leave.validation_type == 'no_validation')
        # if students:
        #     # Automatic validation should be done in sudo, because user might not have the rights to do it by himself
        #     students.sudo().action_validate()
        # self.activity_update()
        # return True


    def _check_approval_update(self, state):
        pass
            
                

    

   
