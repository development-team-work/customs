# -*- coding: utf-8 -*-
{
    "name": "Timesheets Custom",
    "description": "Project",
    "version": "13.0.0.2",
    'author': "ERPify Inc.",
    'website': 'http://erpify.biz',
    'category': '',
    'depends': ['base','project','analytic','hr','hr_timesheet','timesheet_grid','web_grid', 'resource', 'hr_payroll'],
    'data': [
        "view/time_sheet_view.xml",
        "view/timesheet_submission_view.xml",
        "view/allowances_view.xml",
        'security/ir.model.access.csv'
    ],
    'installable': True,
}
