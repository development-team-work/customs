# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

import re
import logging
from odoo import api, fields, models
from odoo.osv import expression
from psycopg2 import IntegrityError
from odoo.tools.translate import _
_logger = logging.getLogger(__name__)



class CountryCity(models.Model):
    _description = "City of a state"
    _name = 'res.country.city'
    _order = 'name'

    state_id = fields.Many2one('res.country.state', string='State', required=True)
    name = fields.Char(string='City', required=True,
               help='city',translate=True)

    _sql_constraints = [
        ('name_uniq', 'unique(state_id, name)', 'The city must be unique by State !')
    ]


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if self.env.context.get('country_id'):
            args = expression.AND([args, [('country_id', '=', self.env.context.get('country_id'))]])

        if operator == 'ilike' and not (name or '').strip():
            first_domain = []
            domain = []
        else:
            first_domain = [('code', '=ilike', name)]
            domain = [('name', operator, name)]

        first_state_ids = self._search(expression.AND([first_domain, args]), limit=limit, access_rights_uid=name_get_uid) if first_domain else []
        state_ids = first_state_ids + [state_id for state_id in self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid) if not state_id in first_state_ids]
        return self.browse(state_ids).name_get()


    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.state_id.code)))
        return result
