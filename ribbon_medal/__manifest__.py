# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Ribbon And Medal',
    'version' : '1.2.0.1',
    'summary': 'ribbon and medal for Police,Army',
    'sequence': 15,
    'description': """
Riboon And Medal Indicator
==========================
    """,
    'category': 'Custom',
    'website': 'http://www.eagle.com/page/billing',
    'images' : [],
    'depends' : ['my_shop'],
    'data': [
        # 'data/payment_acquirer.xml',
        'views/ribbon_medal.xml',
        'views/ribbon_medal_sales.xml',
        'views/ribbon_medal_quotation.xml',
        'wizards/ribbon_acquisition_wizard.xml',

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
