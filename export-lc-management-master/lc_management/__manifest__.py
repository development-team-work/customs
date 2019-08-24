# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

{
    'name': 'Export LC Management',
    'summary': """This module allows to generate Export L/C Management with set of documents.""",
    'version': '10.0.1.0',
    'author': 'Metamorphosis',
    'website': 'http://metamorphosis.com.bd/',
    'category': 'Sales',
    'images': [
        'static/description/Export-LC.png',
        ],
    'sequence': 7,
    'license': 'OPL-1',
    'depends': ['base', 'account','sale','stock'],
    'data': [  
        'views/all_menu.xml',  
        'views/proforma_invoice.xml',  
        'views/lc_info.xml',
        'views/beneficiary_bank.xml',  
        'views/lc_bank.xml',  
        'views/delivery_challans.xml',  
        'views/delivery_orders.xml',  
        'views/commercial.xml',
        'views/billof_exchange.xml',  
        'views/sequence.xml',  
        'views/to_whom.xml',
        'views/shipment_docs_info.xml',
    ],
    'demo': [],
    'price': 299,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
}
