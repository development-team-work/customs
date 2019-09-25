# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.
{
    'name' : 'My Shop',
    'version' : '1.2.0.1',
    'summary': 'SME Customization',
    'sequence': 15,
    'description': """
Customisation Eagle ERP
=======================
    """,
    'category': 'Custom',
    'website': 'http://www.eagle.com/page/billing',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base','website','stock','stock_account','account','sale_management','point_of_sale',
                 'note','website_sale','accounting_pdf_reports','purchase','contacts','mrp','l10n_bd'],
    'data': [
        # 'data/payment_acquirer.xml',
        # 'data/res.country.state.csv',
        'reports/invoice.xml',
        'reports/product_label.xml',
        'reports/account_common_report_view.xml',
        'reports/report.xml',
        'security/ir.model.access.csv',
        'views/my_shop.xml',
        'views/account_invoice.xml',
        'views/order.xml',
        'views/product_view.xml',
        'views/pertner_view.xml',

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
