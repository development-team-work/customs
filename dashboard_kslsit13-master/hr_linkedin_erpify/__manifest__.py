# -*- coding: utf-8 -*-
{
    'name': 'Share Jobs on Linked-In',
    'summary': "Make possible to share jobs on Linked-In",
    'category': 'Human Resources',
    'version': "1.0",
    'depends': ['hr_recruitment','website_hr_recruitment', 'social_linkedin', 'social'],
    'author': 'ERPify Inc.',
    'company': 'ERPify Inc.',
    'website': "https://www.erpify.biz",
    'data': [
        'views/hr_job_linkedin.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
