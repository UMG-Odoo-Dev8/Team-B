import imp
from odoo import models,fields,api

class MonthlyAttendanceReport(models.Model):
    """Defining Student's Monthly Attendance Report"""

    _name = 'sl.monthly.attendance'
    _description = 'Student Monthly Attendance'
    _rec_name = 'section_name'

    section_name = fields.Many2one('sl.section', string="Academic Section")
    months=fields.Selection([
        ('January','January'),
        ('February','February'),
        ('March','March'),
        ('April','April'),
        ('May','May'),
        ('June','June'),
        ('July','July'),
        ('August','August'),
        ('September','September'),
        ('October','October'),
        ('November','November'),
        ('December','December')],default="January",string="Month", required=True, store=True)

    report_ids = fields.One2many("sl.monthly.attendance.line","report_id",string="Attendance Report")

    def check_percent(self,parm_per):
        per=""
        if parm_per < 0.06:
            per="Rejected"
        else:
            per="Accessed"
        return per

    def cal_percent(self,param_point):
        # print(param_point)
        percent=0.0
        if self.months in ['April','June','September','November']:
            percent=param_point/30
        elif self.months=='February':
            percent=param_point/28
        else:
            percent=param_point/31
        return percent

    @api.onchange('section_name','months')
    def onchange_sec_name(self):
        if self.section_name and self.months:
            self.report_ids=[(5,0,0)]
            total_point={}
            attendance_no = self.env['sl.attendance.line'].search([])
            student_ids = self.env['sl.school'].search([('role','=','student')])
            
            if student_ids:
                for student in student_ids:

                    # print("......",roll_num.filtered(lambda x:int(x.student_id) == student.id).mapped("state"))
                    individual_point = sum(attendance_no.filtered(lambda x:int(x.student_id) == student.id and x.attendance_id.attendance_date.strftime('%B') == self.months).mapped("point"))
                
                    # print("total state", total_point)
                    total_point.update({student.id:individual_point})
                    print(total_point)

            sections = self.env['sl.section.line'].search([])
            if sections:
                for sec in sections:
                    if self.section_name.section_name == sec.section_id.section_name:
                        # print("......",sec.student_id)
                        # print(total_point.get(int(sec.student_id)))
                        tot_point = total_point.get(int(sec.student_id))
                        percent = self.cal_percent(tot_point)
                        vals = {
                            'roll_no':sec.roll_no,
                            # 'student_id':int(sec.student_id),
                            'student_name':sec.student_id.name,
                            'total_attendance':tot_point,
                            'attendance_percent': percent,
                            'for_exam' : self.check_percent(percent)
                        }
                        # self.update({'attendance_line_ids':[(0,0,vals)]})
                        self.report_ids=[(0,0,vals)]

class MonthlyAttendanceLine(models.Model):
    """Defining Reverse Relation for One2Many Field"""

    _name = "sl.monthly.attendance.line"
    _description = "Monthly Attendance Line"

    report_id = fields.Many2one("sl.monthly.attendance",string="Report Line ID")
    roll_no = fields.Char("Roll Number")
    student_name = fields.Char("Student Name")
    total_attendance = fields.Float("Total Attendance")
    attendance_percent = fields.Float("Percentage % ")
    for_exam = fields.Char(string="Permission")