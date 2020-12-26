# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2011 Smartmode LTD (<http://www.smartmode.co.uk>).
{
    'name': 'Bangladesh - Check Printing',
    'version': '1.0',
    'category': 'Localization',
    'description': """
This is the latest Bangladeshi Odoo localisation necessary to Print Checks  with:
=================================================================================
""",
    'author': 'SM Ashraf',
    'website': 'https://www.odoo.com/page/accounting',
    'depends': [
        'account',
        'base_iban',
        'base_vat',
    ],
    'data': [
        'data/report_paperformat_data.xml',
        'reports/report_print_check.xml',
        'reports/reports.xml',

    ],
    'demo' : ['demo/l10n_bd_check_printing_demo.xml'],
}

