{
    'name' : 'Demo School',
    'license' : 'LGPL-3',
    'description' : """School Management System""",

    'depends' : [
        'base','mail'
    ],
    'data' : [
        'security/ir.model.access.csv',
        'wizard/wizard_monthly_attendance_view.xml',
        'views/menu.xml',
        'views/school_demo_view.xml',
        'views/session_view.xml',
        'views/attendance_view.xml',
    ],
    'application' : True,
    'auto_install' : False
}