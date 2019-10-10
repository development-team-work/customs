{
    'name': "Eagle SMS GateWay",
    'version': '12.0.1.0.0',
    'author': 'SM Ashraf',
    'license': 'LGPL-3',
    'category': 'SMS',
    "support": "",
    'website': 'https://www.eagle.com/apps/modules/12.0/sms_gateway/',
    'depends': ['base'],
    'price': 30.00,
    'currency': 'EUR',
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'template.xml'
    ],
    # 'qweb': [
    #     'static/src/xml/pos_debranding.xml',
    # ],
    'installable': True,
}
