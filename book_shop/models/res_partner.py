from odoo import fields,models,api
class resPartner(models.Model):
    _inherit = 'res.partner'
    product_public_category_id = fields.Many2one('product.public.category', ondelete='restrict',
                                                 auto_join=True,
                                                 string='Related Public Category',
                                                 help='product public Category data of the Writer')


class BookShopWriter(models.Model):
    _inherits = {'res.partner': 'partner_id'}
    _name= 'book_shop.writer'

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
                                 string='Related Partner', help='Partner-related data of the Writer')
    print_name = fields.Char(index=True, translate=True)
    nick_name = fields.Char("Nick Name",default="")
    spouse_name=fields.Char("Spouse Name",default="")
    dob = fields.Date(string="Date of Birth", required=False, )
    biography=fields.Char(string="Biography",defautt="true")
    book_ids=fields.Many2many('product.template',string="Books")

    # book_ids=fields.Many2many('product.template','partner_product_template_rel','writer_ids','book_ids',string="Written Books", translate=True)
