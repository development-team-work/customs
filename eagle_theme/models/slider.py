# -*- coding: utf-8 -*-
# Part of EagleERP. See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class BlogSlider(models.Model):
    _name = 'blog.slider.config'
    _description = 'Blog Slider'

    name = fields.Char(string="Slider name", default='Blogs',
                       help="""Slider title to be displayed on 
                       website like Our Blogs, Latest Blog Post and etc...""",
                       required=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    no_of_counts = fields.Selection([('1', '1'), ('2', '2'), ('3', '3')], string="Counts",
                                    default='3',
                                    help="No of blogs to be displayed in slider.",
                                    required=True)
    auto_rotate = fields.Boolean(string='Auto Rotate Slider', default=True)
    sliding_speed = fields.Integer(string="Slider sliding speed", default='5000',
                                   help='''Sliding speed of a slider can be set 
                                   from here and it will be in milliseconds.''')
    collections_blog_post = fields.Many2many('blog.post', 'blogpost_slider_rel', 'slider_id',
                                             'post_id',
                                             string="Collections of blog posts", required=True)


class MultiSlider(models.Model):
    _name = 'multi.slider.config'
    _description = 'Product Multi Slider'

    name = fields.Char(string="Slider name", default='Trending',
                       required=True,
                       translate=True,
                       help="""Slider title to be displayed on website 
                       like Best products, Latest and etc...""")
    active = fields.Boolean(string="Active", default=True)

    auto_rotate = fields.Boolean(string='Auto Rotate Slider', default=True)
    sliding_speed = fields.Integer(string="Slider sliding speed", default='5000',
                                   help='''Sliding speed of a slider can be set
                                    from here and it will be in milliseconds.''')

    no_of_collection = fields.Selection([('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                        string="No. of collections to show", default='2',
                                        required=True,
                                        help="No of collections to be displayed on slider.")

    label_collection_1 = fields.Char(string="1st collection name", default='First collection',
                                     required=True,
                                     help="""Collection label to be displayed in
                                      website like Featured, Trending, Best Sellers, etc...""",
                                     translate=True)
    collection_1_ids = fields.Many2many('product.template',
                                        'product_slider_collection_1_rel', 'slider_id',
                                        'prod_id',
                                        required=True,
                                        string="1st product collection")
    special_offer_1_product_tmpl_id = fields.Many2one('product.template',
                                                      required=True,
                                                      string='''Special Offer product 
                                                      for 1st collection''')

    label_collection_2 = fields.Char(string="2nd collection name", default='Second collection',
                                     required=True,
                                     translate=True,
                                     help="""Collection label to be 
                                     displayed in website like Featured, Trending, Best Sellers, etc...""")
    collection_2_ids = fields.Many2many('product.template',
                                        'product_slider_collection_2_rel', 'slider_id',
                                        'prod_id',
                                        required=True,
                                        string="2nd product collection")
    special_offer_2_product_tmpl_id = fields.Many2one('product.template',
                                                      required=True,
                                                      string='''Special Offer
                                                       product for 2nd collection''')

    label_collection_3 = fields.Char(string="3rd collection name", default='Third collection',
                                     translate=True,
                                     help="""Collection label to be 
                                     displayed in website like Featured, Trending, Best Sellers, etc...""")
    collection_3_ids = fields.Many2many('product.template',
                                        'product_slider_collection_3_rel', 'slider_id',
                                        'prod_id',
                                        string="3rd product collection")
    special_offer_3_product_tmpl_id = fields.Many2one(
        'product.template', string='Special Offer product for 3rd collection')

    label_collection_4 = fields.Char(string="4th collection name", default='Fourth collection',
                                     translate=True,
                                     help="""Collection label to be displayed in 
                                     website like Featured, Trending, Best Sellers, etc...""")
    collection_4_ids = fields.Many2many('product.template',
                                        'product_slider_collection_4_rel', 'slider_id',
                                        'prod_id',
                                        string="4th product collection")
    special_offer_4_product_tmpl_id = fields.Many2one(
        'product.template', string='Special Offer product for 4th collection')

    label_collection_5 = fields.Char(string="5th collection name", default='Fifth collection',
                                     translate=True,
                                     help="""Collection label to be
                                      displayed in website like Featured,
                                       Trending, Best Sellers, etc...""")
    collection_5_ids = fields.Many2many('product.template',
                                        'product_slider_collection_5_rel', 'slider_id',
                                        'prod_id',
                                        string="5th product collection")
    special_offer_5_product_tmpl_id = fields.Many2one(
        'product.template', string='Special Offer product for 5th collection')


class CategorySlider(models.Model):
    _name = 'category.slider.config'
    _description = 'Categories Slider'

    name = fields.Char(string="Slider name", default='Trending Categories', required=True,
                       translate=True,
                       help="""Slider title to be displayed on website
                        like Best Categories, Latest and etc...""")
    active = fields.Boolean(string="Active", default=True)
    no_of_counts = fields.Selection([('3', '3'), ('4', '4'), ('5', '5'),
                                     ('6', '6')], string="Counts",
                                    default='4', required=True,
                                    help="No of products to be displayed in slider.")

    auto_rotate = fields.Boolean(string='Auto Rotate Slider', default=True)
    sliding_speed = fields.Integer(string="Slider sliding speed", default='5000',
                                   help='''Sliding speed of a slider can be set
                                    from here and it will be in milliseconds.''')

    collections_category = fields.Many2many('product.public.category',
                                            'eagle_theme_category_slider_rel',
                                            'slider_id', 'cat_id',
                                            string="Collections of category")


class ProductSlider(models.Model):
    _name = 'product.slider.config'
    _description = 'Product Sliders'

    name = fields.Char(string="Slider name", default='New Products', required=True,
                       translate=True,
                       help="""Slider title to be displayed on website 
                       like Best Product, Latest and etc...""")
    active = fields.Boolean(string="Active", default=True)
    no_of_counts = fields.Selection([('3', '3'), ('4', '4'),
                                     ('5', '5'), ('6', '6')], string="Counts",
                                    default='4', required=True,
                                    help="No of products to be displayed in slider.")

    auto_rotate = fields.Boolean(string='Auto Rotate Slider', default=True)
    sliding_speed = fields.Integer(string="Slider sliding speed", default='5000',
                                   help='''Sliding speed of a slider can 
                                   be set from here and it will be in milliseconds.''')
    collections_products = fields.Many2many('product.template',
                                            'eagle_theme_product_template_slider_rel',
                                            'slider_id', 'prod_id',
                                            string="Collections of products")


class FeatureProductSlider(models.Model):
    _name = 'feature.product.slider.config'
    _description = 'Featured Products Slider'

    name = fields.Char(string="Name", default='My Products Slider', required=True,
                       translate=True,
                       help="""Slider name will not be visible in website it 
                       is only for unique identification while dragging the snippet in website.""")
    active = fields.Boolean(string="Active", default=True)
    feature_name = fields.Char(string="Featured Products Slider Label",
                               default='Featured Products', required=True,
                               translate=True,
                               help="""Slider title to be displayed on website 
                               like Featured Products, Latest and etc...""")
    feature_products_collections = fields.Many2many('product.template',
                                                    'eagle_theme_feature_pro_colle_slider_rel',
                                                    'slider_id', 'prod_id',
                                                    required=True,
                                                    string="Featured Products Collections")

    on_sale_name = fields.Char(string="On Sale Slider Label", default='On Sale', required=True,
                               translate=True,
                               help="""Slider title to be displayed on
                                website like On Sale, Latest and etc...""")
    on_sale_collections = fields.Many2many('product.template',
                                           'eagle_theme_on_sale_name_collections_slider_rel',
                                           'slider_id', 'prod_id',
                                           required=True, string="Sale Products Collections")

    random_name = fields.Char(string="Random Products Slider Label",
                              default='Random Products', required=True,
                              translate=True,
                              help="""Slider title to be displayed on website 
                              like Random Products, Latest and etc...""")
    random_products_collections = fields.Many2many('product.template',
                                                   'eagle_theme_random_product_coll_slider_rel',
                                                   'slider_id', 'prod_id', required=True,
                                                   string="Random Products Collections")

    low_price_name = fields.Char(string="Low Price Slider Label",
                                 default='Low Price', required=True,
                                 translate=True,
                                 help="""Slider title to be displayed on website 
                                 like Low Price, Latest and etc...""")
    low_price_collections = fields.Many2many('product.template',
                                             'eagle_theme_low_price_products_collec_slider_rel',
                                             'slider_id', 'prod_id', required=True,
                                             string="Low Products Collections")
