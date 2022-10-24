from odoo import fields,models,api

class MajorModel(models.Model):
    '''Subject Information'''
    _name="sl.major"
    _description="Subjects"

    name=fields.Char(string="Subject")
    author=fields.Char(string="Author")
    edition=fields.Text(string="Edition")
    publisher=fields.Text(string="Publisher")

    teacher_id=fields.Many2one('sl.school','Subject Teacher')
