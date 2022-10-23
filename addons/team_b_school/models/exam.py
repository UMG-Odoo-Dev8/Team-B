from odoo import fields,models,api
import math

class ExamModel(models.Model):
    _name="sl.exam"
    _description="Examination"
    _rec_name="student_id"


    monthly=fields.Selection([
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
        ('December','December')],default="January",string="Month",required=True,store=True)

    student_id=fields.Many2one('sl.monthly.attendance.line',string="Student Name",domain="[('for_exam','=','Accessed'),('report_id.months','=', monthly)]") #for student name    
    student_roll=fields.Char(string='Roll Number',readonly=True)
    section=fields.Char(string='Section',readonly=True)

    major_id=fields.Many2one('sl.major',string="Subject")
    teacher_id=fields.Many2one('sl.school','Subject Teacher', readonly=True)

    # question_id=fields.Many2one('question.line',string="Question:")
    
    exam_ids=fields.One2many('sl.exam.line','exam_id',string="Questions",store=True)

    default_value=fields.Char()
    result=fields.Char()


    # enter into a class -> onchange method is automatically run without action
    
    @api.onchange('student_id')
    def onchange_student_id(self):
        # print(self.student_id)
        # print("Starting.......")
        if self.student_id :
            self.student_roll=self.student_id.roll_no
            self.section=self.student_id.report_id.section_name.section_name

    
    # @api.onchange('major_id')
    # def add_custom_line_ids(self):
    #     mrp = self.env['question.line'].search([])
    #     result = []
    #     print("....",mrp)
    #     vals = {
    #             'question_name': mrp.question_name,
    #             'answer': mrp.answer,
    #             'major': mrp.major
    #         }
    #     self.update({'exam_ids':[(0, 0, vals)]})
    
    @api.onchange('major_id')
    def add_custom_question_ids(self):
        if self.major_id:
            # global answer_list
            # answer_list=[]
            self.teacher_id=self.major_id.teacher_id
            self.exam_ids=[(5,0,0)]
            que_ids = self.env['sl.question.line'].search([])
            # print("....",que_ids)
            if que_ids:
                for que in que_ids:
                    # print(".....",que)
                    # print(".....",que.question_name)
                    # print(".....",que.answer)
                    # print("......",self.major_id.name,que.question_id.major_id.name)
                    if self.major_id.name==que.question_id.major_id.name:
                        # answer_list.append(que.answer)
                        vals = {
                        'question_name': que.question_name,
                        'answer': que.answer
                        }
                        self.exam_ids=[(0,0,vals)]
                        # self.update({'exam_ids':[(0, 0, vals)]})
                        # self.create({'exam_ids':[(0, 0, vals)]})
                # print(answer_list)


    def submit_result(self):
        mark=0
        count=0

        # print("......",answer_list)
        # ex_ids = self.env['exam.line'].search([])
        ex_ids=self.exam_ids
        # print(".........",ex_ids)
        # print("....",ex_ids)
        if ex_ids:
            for ex in ex_ids:
                # print(".....",ex)
                # print(".....Answer ",ex.answer)
                # print(".....Choice ",ex.ans_choice)
                # if self.major_id.name==ex.exam_id.major_id.name: #check subject
                    # if check_id==0 or check_id!=int(ex.exam_id): #initial state or ID not equal state
                    #     check_id=int(ex.exam_id)
                    #     mark=0
                    #     count=0
                    # print(self.major_id.name,ex.exam_id.major_id.name)    
                    # if int(ex.exam_id)==check_id:               
                        if ex.answer==ex.ans_choice:
                        # if answer_list[iterate]==ex.ans_choice:
                            mark+=1
                        count+=1
                                     
        self.default_value="  Your Mark:  "+str(mark)+"/"+str(count)
        if (mark>=math.ceil(count/2)):
            self.default_value+=" Great! You Passed the Exam. "
            self.result="Passed"
        else:
            self.default_value+=" Sorry! You Failed."
            self.result="Failed"
    
class ExamLine(models.Model):
    _name="sl.exam.line"
    _description="Link to Exam"

    exam_id=fields.Many2one('school.exam')

    question_name=fields.Text("Questions")
    answer=fields.Char()

    ans_choice=fields.Selection([
        ('true','True'),
        ('false','False')
       ],string="Answers")

