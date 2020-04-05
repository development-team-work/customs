# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    app_system_name = fields.Char('System Name', help=u"Setup System Name,which replace Eagle")
    app_show_lang = fields.Boolean('Show Quick Language Switcher',
                                   help=u"When enable,User can quick switch language in user menu")
    app_show_debug = fields.Boolean('Show Quick Debug', help=u"When enable,everyone login can see the debug menu")
    app_show_documentation = fields.Boolean('Show Documentation', help=u"When enable,User can visit user manual")
    app_show_documentation_dev = fields.Boolean('Show Developer Documentation',
                                                help=u"When enable,User can visit development documentation")
    app_show_support = fields.Boolean('Show Support', help=u"When enable,User can vist your support site")
    app_show_account = fields.Boolean('Show My Account', help=u"When enable,User can login to your website")
    app_show_enterprise = fields.Boolean('Show Enterprise Tag', help=u"Uncheck to hide the Enterprise tag")
    app_show_share = fields.Boolean('Show Share Dashboard', help=u"Uncheck to hide the Eagle Share Dashboard")
    app_show_poweredby = fields.Boolean('Show Powered by Eagle', help=u"Uncheck to hide the Powered by text")
    app_stop_subscribe = fields.Boolean('Stop Eagle Subscribe(Performance Improve)', help=u"Check to stop Eagle Subscribe function")
    group_show_author_in_apps = fields.Boolean(string="Show Author in Apps Dashboard", implied_group='app_eagle_customize.group_show_author_in_apps',
                                               help=u"Uncheck to Hide Author and Website in Apps Dashboard")

    app_documentation_url = fields.Char('Documentation Url')
    app_documentation_dev_url = fields.Char('Developer Documentation Url')
    app_support_url = fields.Char('Support Url')
    app_account_title = fields.Char('My Eagle.com Account Title')
    app_account_url = fields.Char('My Eagle.com Account Url')
    app_enterprise_url = fields.Char('Customize Module Url(eg. Enterprise)')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        app_system_name = ir_config.get_param('app_system_name', default='eagleApp')

        app_show_lang = True if ir_config.get_param('app_show_lang') == "True" else False
        app_show_debug = True if ir_config.get_param('app_show_debug') == "True" else False
        app_show_documentation = True if ir_config.get_param('app_show_documentation') == "True" else False
        app_show_documentation_dev = True if ir_config.get_param('app_show_documentation_dev') == "True" else False
        app_show_support = True if ir_config.get_param('app_show_support') == "True" else False
        app_show_account = True if ir_config.get_param('app_show_account') == "True" else False
        app_show_enterprise = True if ir_config.get_param('app_show_enterprise') == "True" else False
        app_show_share = True if ir_config.get_param('app_show_share') == "True" else False
        app_show_poweredby = True if ir_config.get_param('app_show_poweredby') == "True" else False
        app_stop_subscribe = True if ir_config.get_param('app_stop_subscribe') == "True" else False

        app_documentation_url = ir_config.get_param('app_documentation_url',
                                                    default='https://www.sunpop.cn/documentation/user/12.0/en/index.html')
        app_documentation_dev_url = ir_config.get_param('app_documentation_dev_url',
                                                        default='https://www.sunpop.cn/documentation/12.0/index.html')
        app_support_url = ir_config.get_param('app_support_url', default='https://www.sunpop.cn/trial/')
        app_account_title = ir_config.get_param('app_account_title', default='My Online Account')
        app_account_url = ir_config.get_param('app_account_url', default='https://www.sunpop.cn/my-account/')
        app_enterprise_url = ir_config.get_param('app_enterprise_url', default='https://www.sunpop.cn')
        res.update(
            app_system_name=app_system_name,
            app_show_lang=app_show_lang,
            app_show_debug=app_show_debug,
            app_show_documentation=app_show_documentation,
            app_show_documentation_dev=app_show_documentation_dev,
            app_show_support=app_show_support,
            app_show_account=app_show_account,
            app_show_enterprise=app_show_enterprise,
            app_show_share=app_show_share,
            app_show_poweredby=app_show_poweredby,
            app_stop_subscribe=app_stop_subscribe,

            app_documentation_url=app_documentation_url,
            app_documentation_dev_url=app_documentation_dev_url,
            app_support_url=app_support_url,
            app_account_title=app_account_title,
            app_account_url=app_account_url,
            app_enterprise_url=app_enterprise_url
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param("app_system_name", self.app_system_name or "")
        ir_config.set_param("app_show_lang", self.app_show_lang or "False")
        ir_config.set_param("app_show_debug", self.app_show_debug or "False")
        ir_config.set_param("app_show_documentation", self.app_show_documentation or "False")
        ir_config.set_param("app_show_documentation_dev", self.app_show_documentation_dev or "False")
        ir_config.set_param("app_show_support", self.app_show_support or "False")
        ir_config.set_param("app_show_account", self.app_show_account or "False")
        ir_config.set_param("app_show_enterprise", self.app_show_enterprise or "False")
        ir_config.set_param("app_show_share", self.app_show_share or "False")
        ir_config.set_param("app_show_poweredby", self.app_show_poweredby or "False")
        ir_config.set_param("app_stop_subscribe", self.app_stop_subscribe or "False")

        ir_config.set_param("app_documentation_url",
                            self.app_documentation_url or "https://www.sunpop.cn/documentation/user/12.0/en/index.html")
        ir_config.set_param("app_documentation_dev_url",
                            self.app_documentation_dev_url or "https://www.sunpop.cn/documentation/12.0/index.html")
        ir_config.set_param("app_support_url", self.app_support_url or "https://www.sunpop.cn/trial/")
        ir_config.set_param("app_account_title", self.app_account_title or "My Online Account")
        ir_config.set_param("app_account_url", self.app_account_url or "https://www.sunpop.cn/my-account/")
        ir_config.set_param("app_enterprise_url", self.app_enterprise_url or "https://www.sunpop.cn")

    def set_module_url(self):
        sql = "UPDATE ir_module_module SET website = '%s' WHERE license like '%s' and website <> ''" % (self.app_enterprise_url, 'OEEL%')
        try:
            self._cr.execute(sql)
        except Exception as e:
            pass

    def remove_sales(self):
        to_removes = [
            # Clear sales documents
            ['sale.order.line', ],
            ['sale.order', ],
            # Sales commission, for personal use
            ['sale.commission.line', ],
            # Cannot delete quote template
            # ['sale.order.template.option',],
            # ['sale.order.template.line',],
            # ['sale.order.template',],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
            seqs = self.env['ir.sequence'].search([
                '|', ('code', '=', 'sale.order'),
                ('code', '=', 'sale.commission.line')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
        except Exception as e:
            raise Warning(e)
        return True

    def remove_product(self):
        to_removes = [
            # Clear product data
            ['product.product', ],
            ['product.template', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number, For automatic product numbering
            seqs = self.env['ir.sequence'].search([('code', '=', 'product.product')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
        except Exception as e:
            pass  # raise Warning(e)
        return True

    def remove_product_attribute(self):
        to_removes = [
            # Clear product attributes
            ['product.attribute.value', ],
            ['product.attribute', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_pos(self):
        to_removes = [
            # Clear POS documents
            ['pos.order.line', ],
            ['pos.order', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
            seqs = self.env['ir.sequence'].search([('code', '=', 'pos.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })

            # Update the value to be closed, because the calculation field of store = true should be reset
            statement = self.env['account.bank.statement'].search([])
            for s in statement:
                s._end_balance()

        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_purchase(self):
        to_removes = [

            # Clear purchase document
            ['purchase.order.line', ],
            ['purchase.order', ],
            ['purchase.requisition.line', ],
            ['purchase.requisition', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
            seqs = self.env['ir.sequence'].search([
                '|', ('code', '=', 'purchase.order'),
                '|', ('code', '=', 'purchase.requisition.purchase.tender'),
                ('code', '=', 'purchase.requisition.blanket.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_expense(self):
        to_removes = [
            # Clear purchase document
            ['hr.expense.sheet', ],
            ['hr.expense', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
            seqs = self.env['ir.sequence'].search([
                ('code', '=', 'hr.expense.invoice')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_expense(self):
        to_removes = [
            # Clear
            ['hr.expense.sheet', ],
            ['hr.expense', ],
            ['hr.payslip', ],
            ['hr.payslip.run', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
            seqs = self.env['ir.sequence'].search([
                ('code', '=', 'hr.expense.invoice')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_mrp(self):
        to_removes = [
            # Clear production document
            ['mrp.workcenter.productivity', ],
            ['mrp.workorder', ],
            ['mrp.production.workcenter.line', ],
            ['change.production.qty', ],
            ['mrp.production', ],
            ['mrp.production.product.line', ],
            ['mrp.unbuild', ],
            ['change.production.qty', ],
            ['sale.forecast.indirect', ],
            ['sale.forecast', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
            seqs = self.env['ir.sequence'].search([
                '|', ('code', '=', 'mrp.production'),
                ('code', '=', 'mrp.unbuild'),
            ])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_mrp_bom(self):
        to_removes = [
            # 清除生产BOM
            ['mrp.bom.line', ],
            ['mrp.bom', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_inventory(self):
        to_removes = [
            # 清除库存单据
            ['stock.quant', ],
            ['stock.move.line', ],
            ['stock.package.level', ],
            ['stock.quantity.history', ],
            ['stock.quant.package', ],
            ['stock.move', ],
            ['stock.pack.operation', ],
            ['stock.picking', ],
            ['stock.scrap', ],
            ['stock.picking.batch', ],
            ['stock.inventory.line', ],
            ['stock.inventory', ],
            ['stock.production.lot', ],
            ['stock.fixed.putaway.strat', ],
            ['procurement.group', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
            seqs = self.env['ir.sequence'].search([
                '|', ('code', '=', 'stock.lot.serial'),
                '|', ('code', '=', 'stock.lot.tracking'),
                '|', ('code', '=', 'stock.orderpoint'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('code', '=', 'picking.batch'),
                '|', ('code', '=', 'stock.quant.package'),
                '|', ('code', '=', 'stock.scrap'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('prefix', '=', 'WH/IN/'),
                '|', ('prefix', '=', 'WH/INT/'),
                '|', ('prefix', '=', 'WH/OUT/'),
                '|', ('prefix', '=', 'WH/PACK/'),
                ('prefix', '=', 'WH/PICK/')
            ])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_account(self):
        to_removes = [
            # Clear financial accounting documents
            ['account.voucher.line', ],
            ['account.voucher', ],
            ['account.bank.statement.line', ],
            ['account.payment', ],
            ['account.analytic.line', ],
            ['account.analytic.account', ],
            ['account.invoice.line', ],
            ['account.invoice.refund', ],
            ['account.invoice', ],
            ['account.partial.reconcile', ],
            ['account.move.line', ],
            ['hr.expense.sheet', ],
            ['account.move', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

                    # Update serial number
                    seqs = self.env['ir.sequence'].search([
                        '|', ('code', '=', 'account.reconcile'),
                        '|', ('code', '=', 'account.payment.customer.invoice'),
                        '|', ('code', '=', 'account.payment.customer.refund'),
                        '|', ('code', '=', 'account.payment.supplier.invoice'),
                        '|', ('code', '=', 'account.payment.supplier.refund'),
                        '|', ('code', '=', 'account.payment.transfer'),
                        '|', ('prefix', 'like', 'BNK1/'),
                        '|', ('prefix', 'like', 'CSH1/'),
                        '|', ('prefix', 'like', 'INV/'),
                        '|', ('prefix', 'like', 'EXCH/'),
                        '|', ('prefix', 'like', 'MISC/'),
                        '|', ('prefix', 'like', 'Bill /'),
                        ('prefix', 'like', 'Miscellaneous /')
                    ])
                    for seq in seqs:
                        seq.write({
                            'number_next': 1,
                        })
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_account_chart(self):
        to_removes = [
            # Clear financial account for resetting
            ['res.partner.bank', ],
            ['res.bank', ],
            ['account.move.line'],
            ['account.invoice'],
            ['account.payment'],
            ['account.bank.statement', ],
            ['account.tax.account.tag', ],
            ['account.tax', ],
            ['account.tax', ],
            ['account.account.account.tag', ],
            ['wizard_multi_charts_accounts'],
            ['account.account', ],
            ['account.journal', ],
        ]
        # todo: do remove_hr because the salary table will use account
        # Update account association, many are multi-company fields, so only ir_property exists, so in the original model, only update
        try:
            # reset default tax， No matter how many companies
            field1 = self.env['ir.model.fields']._get('product.template', "taxes_id").id
            field2 = self.env['ir.model.fields']._get('product.template', "supplier_taxes_id").id

            sql = ("delete from ir_default where field_id = %s or field_id = %s") % (field1, field2)
            self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        try:
            rec = self.env['res.partner'].search([])
            for r in rec:
                r.write({
                    'property_account_receivable_id': None,
                    'property_account_payable_id': None,
                })
        except Exception as e:
            pass  # raise Warning(e)
        try:
            rec = self.env['product.category'].search([])
            for r in rec:
                r.write({
                    'property_account_income_categ_id': None,
                    'property_account_expense_categ_id': None,
                    'property_account_creditor_price_difference_categ': None,
                    'property_stock_account_input_categ_id': None,
                    'property_stock_account_output_categ_id': None,
                    'property_stock_valuation_account_id': None,
                })
        except Exception as e:
            pass  # raise Warning(e)
        try:
            rec = self.env['stock.location'].search([])
            for r in rec:
                r.write({
                    'valuation_in_account_id': None,
                    'valuation_out_account_id': None,
                })
        except Exception as e:
            pass  # raise Warning(e)

        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)


            sql = "update res_company set chart_template_id=null;"
            self._cr.execute(sql)
            # Update serial number
        except Exception as e:
            pass

        return True


    def remove_project(self):
        to_removes = [
            # Clear item
            ['account.analytic.line', ],
            ['project.task', ],
            ['project.forecast', ],
            ['project.project', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            # Update serial number
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_website(self):
        to_removes = [
            # Clear website data, w, w_blog
            ['blog.tag.category', ],
            ['blog.tag', ],
            ['blog.post', ],
            ['blog.blog', ],
            ['website.published.multi.mixin', ],
            ['website.published.mixin', ],
            ['website.multi.mixin', ],
            ['website.redirect', ],
            ['website.seo.metadata', ],
            ['website.page', ],
            ['website.menu', ],
            ['website', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_message(self):
        to_removes = [
            # Clear message data
            ['mail.message', ],
            ['mail.followers', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_workflow(self):
        to_removes = [
            # Clear workflow
            ['wkf.workitem', ],
            ['wkf.instance', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

        except Exception as e:
            pass  # raise Warning(e)
        return True


    def remove_all_biz(self):
        try:
            self.remove_account()
            self.remove_inventory()
            self.remove_mrp()
            self.remove_purchase()
            self.remove_sales()
            self.remove_project()
            self.remove_pos()
            self.remove_expense()
            self.remove_message()
        except Exception as e:
            pass  # raise Warning(e)
        return True
