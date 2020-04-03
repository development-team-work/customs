# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api

class printBarcodewizard(models.TransientModel):
    _name = 'myshop.barcode.wizard'
    _rec_name = 'picking_id'
    picking_id=fields.Many2one('stock.picking')
    item_ids=fields.One2many('myshop.barcode.items','wizard_id')
    pricelist=fields.Many2one("product.pricelist")

    @api.onchange('picking_id','pricelist')
    def get_product_ids(self):
        self.ensure_one()
        items=self.env['myshop.barcode.items'].search([('wizard_id', '=', self.id)])
        data=[]
        if self.picking_id:
            if not self.pricelist:
                self.pricelist = self.env['product.pricelist'].search([('id', '>', '0')], limit=1)
            for rec in self.picking_id.move_ids_without_package:
               product=rec.product_id
               qty=rec.quantity_done
               rate=self.pricelist.get_product_price(rec.product_id, self.pricelist, False)
               input= items.create({
                    'product_id':product.id,
                    'qty':qty,
                   'rate': rate
               })
               data.append(input.id)
            self.item_ids=[(6,0,data)]
        else:
            for rec in self.item_ids:
                rec.rate=self.pricelist.get_product_price(rec.product_id, self.pricelist, False)


class PrintBarcodeItems(models.TransientModel):
    _name = 'myshop.barcode.items'
    _rec_name = 'product_id'
    wizard_id = fields.Many2one('myshop.barcode.wizard')
    product_id=fields.Many2one("product.product","Product")
    qty=fields.Integer("Qty")
    rate=fields.Float("Rate")
    @api.onchange('product_id')
    def _get_price(self):
        product=self.product_id
        if product.id:
            sale_price_digits = self.env['decimal.precision'].precision_get('Product Price')
            if self.wizard_id:
                pricelist=self.wizard_id.pricelist
            else:
                pricelist=self.env['product.pricelist'].search([('id','>','0')],limit=1)
            price = pricelist.get_product_price(product, pricelist, False)
            if not price:
                price = product.list_price
            self.rate= price