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
        'data/ribbon.rank.csv',
        'data/ribbon.post.csv',
        'data/product.attribute.csv',
        'data/product.attribute.value.csv',
        'data/ribbon.force.unit.csv',
        'data/data/ribbon.force.unit.csv',
        'data/ribbon.acquisition.rule.csv',
        'data/ribbon.extension.csv',
        'data/ribbon.regulation.csv',
        'views/res_partner.xml',
        'views/product.xml',
        'views/ribbon_force.xml',
        'views/ribbon.xml',
        'views/templates.xml',
        'views/ribbon_regulation.xml',
        'views/test.xml',
        # 'views/ribbon_sales.xml',
        # 'views/ribbon_quotation.xml',
        'security/ir.model.access.csv',
        'wizards/ribbon_acquisition_wizard.xml',

    ],
    'demo': [

    ],
    'qweb': ['static/src/xml/hello_world.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}
