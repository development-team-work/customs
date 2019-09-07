{
    'name': 'Balance field in Partner form',
    'images': ['images/main_screenshot.png'],
    'version': '1.0.1',
    'category': 'Partner',
    'summary': 'Adds Balance field to main Partner form',
    'author': 'SM Ashraf',
    'website': 'http://www.eagle_erp.com',
    'depends': [
	'account','my_shop',
    ],
    'installable': True,
    'license': 'AGPL-3',
    'data': [
        'views/partner_views.xml',
    ],
}
