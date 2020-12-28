# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Eagle Uniform Tailor',
    'version' : '14.0.1',
    'summary': 'Uniform Tailos Customization',
    'sequence': 15,
    'description': """
Customisation Eagle ERP
=======================
    """,
    'category': 'Custom',
    'website': 'http://www.eagle.com/page/billing',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base','eagle_shop','sale','ribbon'],
    'data': [
        'views/tailor_measerment.xml',
        'security/ir.model.access.csv',
        # 'views/res_config_settings_views.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}
