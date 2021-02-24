# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api

class productBook(models.Model):
    _inherit = 'product.template'
    is_book=fields.Boolean("Is A Book")
    publisher_ids=fields.Many2many("res.partner",'publisher_book_rel','published_books','publisher_ids',string="Publisher")
    writer_ids=fields.Many2many("res.partner",'writer_book_rel','written_books','writer_ids',string="Writer")
    prefix = fields.Char("Prefix")
    suffix = fields.Char("Suffix")
    edition = fields.Char("edition")
    total_page = fields.Integer("Page")
    printed_price = fields.Float("Printed Price")



# class product_product(models.Model):
#     _inherit = "product.product"
#     is_book = fields.Boolean("Is A Book", related='product_variant_ids.is_book', readonly=False)
#     publisher_ids = fields.Many2many("res.partner", 'publisher_book_rel', 'published_books', 'publisher_ids',
#                                      string="Publisher")
#     writer_ids = fields.Many2many("res.partner", 'writer_book_rel', 'written_books', 'writer_ids', string="Writer")
#     prefix = fields.Char("Prefix", related='product_variant_ids.prefix', readonly=False)
#     suffix = fields.Char("Suffix", related='product_variant_ids.suffix', readonly=False)
#     edition = fields.Char("edition", related='product_variant_ids.edition', readonly=False)
#     total_page = fields.Integer("Page", related='product_variant_ids.total_page', readonly=False)
#     printed_price = fields.Float("Printed Price", related='product_variant_ids.printed_price', readonly=False)

class ProductPublicCategory(models.Model):
    _inherit='product.public.category'
    _description='this modules adds product public categories for writer and publishers'
    related_writer_id=fields.Many2one('res.partner',"Writer")
    related_publisher_id=fields.Many2one('res.partner',"Publisher")