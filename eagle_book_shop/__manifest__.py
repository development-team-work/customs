# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.


{
    'name' : 'Eagle Book Shop',
    'version' : '14.0.1',
    'summary': 'Shop Customization For Book Retailer',
    'sequence': 15,
    'description': """
Customisation Eagle ERP
=======================
    """,
    'category': 'Custom',
    'website': 'http://www.eagle.com/page/billing',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['eagle_shop'],
    'data': [
        'views/product_view.xml',
        'views/partner_view.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
