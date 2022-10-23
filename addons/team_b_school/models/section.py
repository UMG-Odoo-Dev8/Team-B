import string
from odoo import models,fields,api

class SectionModel(models.Model):
    _name = 'sl.section'
    _description = 'Section Information'
    _rec_name = 'section_name'


    head_teacher_id = fields.Many2one('sl.school', string="Head Teacher")
    section_ids = fields.One2many('sl.section.line','section_id', string="Student")
    section_name = fields.Char(string="Academic Section")

    def set_roll_no(self):      #for roll number
        roll_no=0
        for line in self.section_ids:
            roll_no+=1
            line.roll_no=roll_no
        return

    @api.model
    def create(self,vals):          #overwrite create method
        res=super(SectionModel,self).create(vals)
        res.set_roll_no()
        return res

    def write(self,values):         #overwrite write method
        res=super(SectionModel,self).write(values)
        self.set_roll_no()
        return res


class SectionLine(models.Model):
    _name = 'sl.section.line'
    _description = 'Link to Section'
    _rec_name = 'student_id'

    section_id = fields.Many2one('sl.section')
    student_id = fields.Many2one('sl.school', string="Student Name")
    roll_no = fields.Char(string="Roll No")

