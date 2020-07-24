{
    'name': 'Eagle Book Shop',
    'version': '13.1.0.1',
    'summary': 'This module is used whether a Shop sales Books',
    'description': 'necesary update for a book shop',
    'category': 'others',
    'author': 'SM Ashraf',
    'website': 'eagle_erp.com',
    'license': '',
    'depends': ["base","eagle_shop",],
    'data': [
             'views/views.xml',
             'views/templates.xml',
             'security/ir.model.access.csv',
             'views/res_partner_view.xml',
             ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    'application': False,

}