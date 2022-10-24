{
    'name' : 'Our School (TeamB)',
    'version' : '0.1',
    'author' : 'Team B: Aung Myat Thu, Ye Zaw Oo',
    'category' : 'School',
    'sequence' : -100,
    'license' : 'LGPL-3',
    'description' : """School Management System""",

    'depends' : [
        'base'
    ],
    'data' : [
        'security/ir.model.access.csv',
        # 'wizard/wizard_monthly_attendance_view.xml',
        'views/menu.xml',
        'views/school_views.xml',
        'views/section_views.xml',
        'views/attendance_views.xml',
        'views/monthly_attendance_views.xml',
        'views/major_views.xml',
        'views/question_views.xml',
        'views/exam_views.xml'
    ],
    'auto_install' : False
}