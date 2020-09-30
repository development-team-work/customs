# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Eagle SMS',
    'version' : '1.2.0.1',
    'summary': 'SMS Integration With Odoo',
    'sequence': 15,
    'description': """
Integrate SMS to odoo
=====================
    """,
    'category': 'Custom',
    'website': 'http://www.eagle.com/page/billing',
    'images' : [],
    'depends' : ['base','sms'],
    'data': [
        'views/sms.xml',
        'views/sms_gateway.xml',
        'views/sms_gateway_account.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
