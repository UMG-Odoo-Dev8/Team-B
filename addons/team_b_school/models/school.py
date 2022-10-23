from datetime import date
from email.policy import default
import string
from odoo import models,fields,api

class DemoSchool(models.Model):
    _name = 'sl.school'
    _description = 'School Information'

    name = fields.Char(string="Name", required=True)
    avatar = fields.Binary(string="Profile Picture :")
    role = fields.Selection([
        ('student','Student'),
        ('teacher','Teacher')], string="Role", required=True, default="student")
    teacher_role = fields.Selection([
        ('principal','Principal'),
        ('teacher','Teacher'),
        ('teacher_head','Teacher Head')], string="Teacher Role")
    father_name = fields.Char(string="Father Name")
    address = fields.Text(string="Address")
    phone_no = fields.Char(string="Phone Number")
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('other','Other')], string="Gender")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age")

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                self.age = today.year - rec.dob.year
            else:
                self.age = 1