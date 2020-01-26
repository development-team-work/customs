# -*- coding: utf-8 -*-
# Part of EagleERP. See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class ProductPublicCategory(models.Model):

    _inherit = 'product.public.category'

    linked_product_count = fields.Integer(string='# of Products')
    include_in_megamenu = fields.Boolean(
        string="Include in mega menu", help="Include in mega menu")
    menu_id = fields.Many2one('website.menu', string="Main menu")
    description = fields.Text(string="Description",
                              translate=True,
                              help="""Short description which will be 
                              visible below category slider.""")


class EagleshopMultiProductImages(models.Model):
    _name = 'biztech.product.images'
    _description = "Add Multiple Image in Product"

    name = fields.Char(string='Title', translate=True)
    alt = fields.Char(string='Alt', translate=True)
    attach_type = fields.Selection([('image', 'Image'), ('video', 'Video')],
                                   default='image',
                                   string="Type")
    image = fields.Binary(string='Image', store=True, attachment=True)
    video_type = fields.Selection([('youtube', 'Youtube'),
                                   ('vimeo', 'Vimeo'),
                                   ('html5video', 'Html5 Video')],
                                  default='youtube',
                                  string="Video media player")
    cover_image = fields.Binary(string='Cover image', store=True, attachment=True,
                                help="Cover Image will be show untill video is loaded.")
    video_id = fields.Char(string='Video ID')
    video_ogv = fields.Char(string='Video OGV', help="Link for ogv format video")
    video_webm = fields.Char(string='Video WEBM', help="Link for webm format video")
    video_mp4 = fields.Char(string='Video MP4', help="Link for mp4 format video")
    sequence = fields.Integer(string='Sort Order')
    biz_product_tmpl_id = fields.Many2one('product.template', string='Product')
    more_view_exclude = fields.Boolean(string="More View Exclude")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    related_product_ids = fields.Many2many('product.template', 'product_related_rel', 'src_id',
                                           'dest_id',
                                           string='Related Products',
                                           help='Appear on product description in website')
    biz_images = fields.One2many('biztech.product.images', 'biz_product_tmpl_id',
                                 string='Product Images')
    multi_image = fields.Boolean(string="Add Multiple Images?")
    quickview_description = fields.Text(string="Quick View Description",
                                        translate=True,
                                        help="""Short description which will
                                         be visible in quick view.""")


class ProductSortBy(models.Model):
    _name = 'biztech.product.sortby'
    _description = 'Custom Product Sorting'

    name = fields.Char(string="Name", help='Name for sorting option',
                       required=True)
    sort_type = fields.Selection(
        [('asc', 'Ascending'), ('desc', 'Descending')], string="Type", default='asc')
    sort_on = fields.Many2one('ir.model.fields', string='Sort On',
                              help='Select field on which you want to apply sorting',
                              domain=[('model', '=', 'product.template'),
                                      ('ttype', 'in',
                                       ('char', 'float', 'integer', 'datetime', 'date'))])
