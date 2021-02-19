# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'


    # TODO to install ModuleName use this line
    # module_ModuleName = fields.Boolean("comment for ModuleName for")
    module_ribbon = fields.Boolean("if your shop deals with Service ribbon for police")
    module_eagle_book_shop = fields.Boolean("if your shop deals with books")
