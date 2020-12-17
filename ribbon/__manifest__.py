# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.



{
    'name' : 'Police Ribbon And Medal',
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
    'depends' : ['eagle_shop'],
    'data': [
        'data/ribbon.force.csv',
        'data/ribbon.post.csv',
        'data/ribbon.rank.csv',
        'data/ribbon.force.unit.csv',
        'data/ribbon.acquisition.rule.csv',
        'views/res_partner.xml',
        'views/ribbon.xml',
        # 'views/ribbon_sales.xml',
        # 'views/ribbon_quotation.xml',
        'security/ir.model.access.csv',
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
