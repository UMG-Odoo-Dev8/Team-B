from datetime import datetime,timedelta
import string
from odoo import models,fields,api
from odoo.exceptions import AccessError,ValidationError,UserError

class StudentLeave(models.Model):
    _name = 'student.leave'
    _description = 'Student Leave Request'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'leave_type'


    section_id = fields.Many2one('session.model', string="Academic Section")
    student_id = fields.Many2one('attendance.model', string="Student Name")

    start_date = fields.Date(string="Leave Start Date")
    end_date = fields.Date(string="Leave End Date")
    total_leave_day = fields.Integer(string="Total Leave Days")

    # parent_id = fields.Many2one('student.leave', string='Parent', copy=False)
    # linked_request_ids = fields.One2many('student.leave', 'parent_id', string='Linked Requests')

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



    