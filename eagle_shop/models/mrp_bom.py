# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api

class MrpBomTemplate(models.Model):
    """ Defines bills of material for a product or a product template """
    _name = 'mrp.bom.template'
    _description = 'Bill of Material Template'
    _inherit = ['mail.thread']
    # _rec_name = 'product_tmpl_id'
    _order = "sequence"
    _check_company_auto = True

    # def _get_default_product_uom_id(self):
    #     return self.env['uom.uom'].search([], limit=1, order='id').id

    code = fields.Char('Reference')
    active = fields.Boolean(
        'Active', default=True,
        help="If the active field is set to False, it will allow you to hide the bills of material template without removing it.")


class ComponentType(models.Model):
    """ Defines bills of material for a product or a product template """
    _name = 'eagle.shop.bom.component.type'
    _description = 'Bill of Material Template Component Type'
    _inherit = ['mail.thread']
    # _order = "sequence"
    _check_company_auto = True
    name = fields.Char('Component Type')
    active = fields.Boolean(
        'Active', default=True,
        help="If the active field is set to False, it will allow you to hide the bills of material template without removing it.")


class MrpBomLine(models.Model):
    _inherit="mrp.bom.line"
    component_type=fields.Many2one('eagle.shop.bom.component.type',"Type Of Component")
    product_id = fields.Many2one('product.product', 'Component Product', required=True, check_company=True)

