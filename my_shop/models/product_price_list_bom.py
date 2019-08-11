# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from eagle import _,fields, models,api

class productPriceList(models.Model):
    _inherit = "product.pricelist"
    kit_discount=fields.Float('Kit Discount', default=0, digits=(16, 2))
    kit_add=fields.Float('Kit Additional', default=0, digits=(16, 2))

class product_product(models.Model):
    _inherit = "product.product"
    pricelist_item_ids = fields.One2many(
        'product.pricelist.item','product_id',string='Pricelist Items')
    product_price_list_item_count = fields.Integer(
        '# Pricelist', compute='_compute_product_pricelist_items_count')
    @api.multi

    def _compute_product_pricelist_items_count(self):
        self.product_price_list_item_count = len(self.with_prefetch().pricelist_item_ids)
#


class productPriceListItem(models.Model):
    _inherit = "product.pricelist.item"
    bom_price=fields.Float("Price BOM") #,compute="_get_pricelist_item_component_price")
    product_id = fields.Many2one(
        'product.product',string= 'Product', ondelete='cascade',
        help="Specify a product if this rule only applies to one product. Keep empty otherwise.")
    compute_price = fields.Selection([
        ('fixed', 'Fix Price'),
        ('percentage', 'Percentage (discount)'),
        ('bom', 'Bill of material (BOM)'),
        ('formula', 'Formula')], index=True, default='fixed')
    @api.one
    @api.depends('categ_id', 'product_tmpl_id', 'product_id', 'compute_price', 'fixed_price', \
        'pricelist_id', 'percent_price', 'price_discount', 'price_surcharge')
    def _get_pricelist_item_name_price(self):
        if self.categ_id:
            self.name = _("Category: %s") % (self.categ_id.name)
        elif self.product_tmpl_id:
            self.name = self.product_tmpl_id.name
        elif self.product_id:
            self.name = self.product_id.display_name.replace('[%s]' % self.product_id.code, '')
        else:
            self.name = _("All Products")

        if self.compute_price == 'fixed':
            self.price = ("%s %s") % (self.fixed_price, self.pricelist_id.currency_id.name)
        elif self.compute_price == 'percentage':
            self.price = _("%s %% discount") % (self.percent_price)
        elif self.compute_price == 'bom':
            self.price = self.bom_price
        else:
            self.price = _("%s %% discount and %s surcharge") % (self.price_discount, self.price_surcharge)

    def _get_pricelist_item_component_price(self,kit):

        if component.compute_price == 'fixed':
            self.price = ("%s %s") % (self.fixed_price, self.pricelist_id.currency_id.name)
        elif self.compute_price == 'percentage':
            self.price = _("%s %% discount") % (self.percent_price)
        elif self.compute_price == 'bom':
            self.price = self.bom
        else:
            self.price = _("%s %% discount and %s surcharge") % (self.price_discount, self.price_surcharge)

class productBook(models.Model):
    _inherit = 'product.template'
    is_book=fields.Boolean("Is A Book",default=False)
    writer_ids=fields.Many2many("res.partner",'res_partner_product_template_rel','book_ids','writer_ids',string="Writer")
    publisher=fields.Many2one("res.partner",string="Publisher")
    prefix = fields.Char("Prefix")
    suffix = fields.Char("Suffix")

class ProductPriceListIterms(models.Model):
    _inherit = "product.pricelist.item"


    @api.onchange('applied_on')
    def _onchange_applied_on(self):
        if self.applied_on != '0_product_variant':
            self.product_id = False
#todo correct following line
            # self.product_tmpl_id=context['default_product_id'}
        if self.applied_on != '1_product':
            self.product_tmpl_id = False
        if self.applied_on != '2_product_category':
            self.categ_id = False
        if self.applied_on == '0_product_variant':
            self.product_id = self._context['default_product_id']



