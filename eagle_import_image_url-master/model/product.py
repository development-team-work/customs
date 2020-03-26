# -*- coding: utf-8 -*-

import urllib
import base64

from odoo import fields, models, api, _

class Product(models.Model):
    _inherit = 'product.product'
   
    image_url = fields.Char(
        string='Image Url',
        copy=False,
    )
    
    @api.model
    def create(self, vals):
        if not vals.get('image_medium'):
            image_url = vals.get('image_url')
            if image_url:
                try:
                    image = base64.encodestring(urllib.request.urlopen(image_url).read())
                    vals['image_medium'] = image
                except:
                    pass
        return super(Product, self).create(vals)
            

    def write(self, vals):
        image_url = vals.get('image_url')
        if image_url:
            try:
#            image = base64.encodestring(urllib.urlopen(image_url).read())
                image = base64.encodestring(urllib.request.urlopen(image_url).read())
                vals.update({'image_medium': image})
            except:
                pass
        return super(Product, self).write(vals)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
