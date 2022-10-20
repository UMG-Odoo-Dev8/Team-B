import string
from odoo import models,fields,api

class SessionModel(models.Model):
    _name = 'session.model'
    _description = 'Session Info'
    _rec_name = 'section'


    head_teacher_id = fields.Many2one('school.model', string="Head Teacher")
    child_id = fields.One2many('session.model.line','parent_id', string="Student")
    section = fields.Char(string="Academic Section")

    def set_roll_no(self):      #for roll number
        roll_no=0
        for line in self.child_id:
            roll_no+=1
            line.roll_no=roll_no
        return

    @api.model
    def create(self,vals):          #overwrite create method
        res=super(SessionModel,self).create(vals)
        res.set_roll_no()
        return res

    def write(self,values):         #overwrite write method
        res=super(SessionModel,self).write(values)
        self.set_roll_no()
        return res


class SessionRelation(models.Model):
    _name = 'session.model.line'
    _description = 'Link to Session'
    _rec_name = 'student_id'

    parent_id = fields.Many2one('session.model')
    student_id = fields.Many2one('school.model', string="Student Name")
    roll_no = fields.Char(string="Roll No")

