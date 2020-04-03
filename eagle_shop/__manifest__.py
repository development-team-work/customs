# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Eagle Shop',
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
    'depends' : ['base','website','stock','stock_account','account','sale_management','point_of_sale','product',
                 'note','website_sale','purchase','contacts','mrp','accounting_pdf_reports'],
    'data': [
        # 'data/payment_acquirer.xml',
        'data/res.country.state.csv',
        'data/report_paperformat_data.xml',
        'reports/invoice.xml',
        # 'reports/product_label.xml',
        'reports/account_common_report_view.xml',
        'reports/report.xml',
        'reports/print_barcode.xml',
        # 'security/ir.model.access.csv',
        'views/account_payment.xml',
        'views/my_shop.xml',
        'views/ir_qweb_widget_templates.xml',
        # 'views/templates.xml',
        'views/account_invoice.xml',
        'views/order.xml',
        'views/purchase_order.xml',
        'views/product_view.xml',
        'views/pertner_view.xml',
        'views/res_config_settings_views.xml',

        'wizard/print_barcode_wizard.xml',
        'views/stock_picking.xml',
        'views/product_pricelist_view.xml',

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
