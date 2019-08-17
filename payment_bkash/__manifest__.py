# -*- coding: utf-8 -*-

{
    'name': 'bKash Payment Acquirer',
    'category': 'Accounting',
    'summary': 'Payment Acquirer: bKash Implementation',
    'version': '1.0',
    'description': """bKash Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'data/payment_acquirer_data.xml',
        'views/payment_views.xml',
        'views/payment_bkash_templates.xml',


    ],
    'installable': True,
    # 'post_init_hook': 'create_missing_journal_for_acquirers',
}
