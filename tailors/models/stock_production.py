# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
import re


class tailorProductionLot(models.Model):

    _inherit ='stock.production.lot'
    name = fields.Char(
        'Lot/Serial Number',
        required=True, help="Unique Lot/Serial Number")
    @api.model_create_multi
    def create(self, vals_list):
        vals=vals_list
        self._check_create()
        return super(tailorProductionLot, self).create(vals)