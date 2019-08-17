# -*- coding: utf-8 -*-

{
    'name': 'Rocket Payment Acquirer',
    'category': 'Accounting',
    'summary': 'Payment Acquirer: Rocket Implementation',
    'version': '1.0',
    'description': """Rocket Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_rocket_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'auto_install': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
}
