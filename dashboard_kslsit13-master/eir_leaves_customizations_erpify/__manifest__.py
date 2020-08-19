# -*- coding: utf-8 -*-
{
    'name': 'Odoo Leaves Enhancement',
    'summary': "Make possible to apply rules to leaves approval",
    'category': 'HR',
    'version': "1.0",
    'depends': ['hr', 'hr_holidays', 'mail', 'base'],
    'author': 'ERPify Inc.',
    'company': 'ERPify Inc.',
    'website': "https://www.erpify.biz",
    'data': [
        'views/approval_rules.xml',
        'views/other_models.xml',
        'security/ir.model.access.csv',
        'security/approvals_security.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
