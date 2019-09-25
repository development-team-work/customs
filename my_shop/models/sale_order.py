# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from eagle import _,fields, models,api

class saleOrderInherit(models.Model):
    _inherit = 'sale.order'




