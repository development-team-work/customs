# -*- coding: utf-8 -*-
{
    'name': 'Integration with Interfaces through Email',
    'summary': "Makes possible to receive data from any Interface through emails",
    'category': 'Integrations',
    'version': "1.0",
    'depends': ['base', 'mail'],
    'author': 'ERPify Inc.',
    'company': 'ERPify Inc.',
    'website': "https://www.erpify.biz",
    'data': [
        'security/interface_security.xml',
        'views/integrate_interface_view.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
