# -*- coding: utf-8 -*-
# Part of EagleERP. See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class CustomThemeView(models.Model):
    _inherit = 'theme.ir.ui.view'

    customize_show = fields.Boolean("Show As Optional Inherit", default=False)

    @api.multi
    def _convert_to_base_model(self, website, **kwargs):
        res = super(CustomThemeView, self)._convert_to_base_model(website=website,
                                                                  **kwargs)
        if res:
            res.update({'customize_show': self.customize_show or False})
        return res
