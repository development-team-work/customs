{
    'name': 'Time off',
    'version': '13.0.0.1',
    'category': 'Time Off',
    'summary': 'Change time off to leave',
    "description": """
    1. Change time off to leave
    """,
    'author': 'ERPify Inc.',
    'website': 'http://www.erpify.biz',
    'depends': ['hr_holidays', 'resource'],
    'data': [
        'views/menus.xml',
        'views/views.xml',
    ],
    'qweb': ["static/src/xml/template.xml"],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
