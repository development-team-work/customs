{
    'name': 'Payroll Customizations',
    'version': '13.0.0.3',
    'category': 'Human Resource',
    'summary': 'Add more facilities to payroll',
    "description": "",
    'author': 'ERPify Inc.',
    'website': 'http://www.erpify.biz',
    'depends': ['hr', 'hr_contract', 'hr_payroll', 'custom_timesheet_erpify'],
    'data': [
                'views/inherited_employee.xml',
                "views/inherited_batch_view.xml",
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
