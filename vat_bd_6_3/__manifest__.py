# -*- coding: utf-8 -*-
{
    'name': "vat_bd_6_3",

    'summary': """
        This app is designed to impliment Bangladesh VAT 6.3 """,

    'description': """
       This app is designed to impliment Bangladesh VAT 6.3
    """,

    'author': "SM Ashraf",
    'website': "http://www.eagle_erp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/report.xml',
        'reports/vat_63_challan.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}