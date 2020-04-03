# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api

class productPriceList(models.Model):
    _inherit = "product.pricelist"
    kit_discount=fields.Float('Kit Discount', default=0, digits=(16, 2))
    kit_add=fields.Float('Kit Additional', default=0, digits=(16, 2))

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
            # self.product_id = self._context['default_product_id']
        if self.applied_on == 'product_tmpl_id':
            self.product_tmpl_id = self._context['default_product_tmpl_id']

class productPricePerPriceList(models.Model):
    _name="product.pricelist.price"

    product_id = fields.Many2one('product.product', 'Product', index=True, ondelete="cascade", required=True)

