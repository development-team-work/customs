# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

import re
import logging
from eagle import api, fields, models
from eagle.osv import expression
from psycopg2 import IntegrityError
from eagle.tools.translate import _
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
        if self.state_id:
            args = expression.AND([args, [('state_id', '=', self.state_id)]])

        if operator == 'ilike' and not (name or '').strip():
            first_domain = []
            domain = []
        else:
            first_domain = [('name', '=ilike', name)]
            domain = [('name', operator, name)]

        first_city_ids = self._search(expression.AND([first_domain, args]), limit=limit, access_rights_uid=name_get_uid) if first_domain else []
        city_ids = first_city_ids + [city_id for city_id in self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid) if not city_id in first_city_ids]
        return self.browse(city_ids).name_get()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.state_id.code)))
        return result
