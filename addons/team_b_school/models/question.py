from odoo import models,fields,api

class QuestionModel(models.Model):
    _name="sl.question"
    _description="Exam Questions"
    _rec_name="major_id"

    major_id=fields.Many2one('sl.major',string="Subject") # for major name
    question_ids=fields.One2many('sl.question.line','question_id',string="Questions") # for questions

    # @api.onchange('major_id')
    # def onchange_major_id(self):
    #     for rec in self:
    #         for line in self.question_ids:
    #             # print(".....",line)
    #             if rec.major_id.name:
    #                 # print("Major:",line.major) #False
    #                 print("......",rec.major_id.name)
    #                 line.major=rec.major_id.name
    #             else:
    #                 line.major=rec.major_id.name


class QuestionLine(models.Model):
    _name="sl.question.line"
    _description="Question Line"
    _rec_name="question_name"

    question_id=fields.Many2one('sl.question') # for inverse name to link One2many

    question_name=fields.Text(string="Questions")
    answer=fields.Selection([
        ('true','True'),
        ('false','False')],string="Answers")

    active = fields.Boolean(
        string='Active',
        default=True
    )

    # major=fields.Char()