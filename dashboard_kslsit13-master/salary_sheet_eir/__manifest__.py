{
    'name': "Salary Sheet",
    'description': "Salary Sheet",
    'author': 'odoo',
    'website': "http://www.odoo.com",
    'category': 'sale',
    'version': '12.0.01',
    'application': True,
    'depends': ['base','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'template.xml',
        'views/module_report.xml',
    ],
}