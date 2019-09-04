# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from eagle import _,fields, models,api

class accountCommonReport(models.TransientModel):
    _inherit = 'account.common.report'

    partner_id=fields.Many2one('res.partner',default=lambda self: self.env.context.get('default_partner_ids'))

    