# -*- coding: utf-8 -*-

{
    'name': 'LebuPay Payment Acquirer',
    'category': 'Accounting',
    'summary': 'Payment Acquirer: LebuPay Implementation',
    'version': '1.0',
    'description': """

LebuPay Payment Acquirer
=======================
Payment through credit/debit cards,
bKash, Rocket, bank accounts, or agent banking
""",
    'author': 'Metamorphosis Pvt Ltd.',
    'website': 'https://metamorphosis.com.bd',
    'depends': ['payment', 'website'],
    'data': [

        'views/payment_views.xml',
        'views/payment_lebupay_templates.xml',     
        'views/success_views.xml',
        'views/failure_views.xml',
        'data/payment_acquirer_data.xml',

    ],
    'installable': True,
    'price': 149,
    'currency': 'EUR',
    'auto_install': False,
    'application': True,
}