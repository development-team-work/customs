# -*- coding: utf-8 -*-
# Part of EagleERP. See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models


class EventInherit(models.Model):
    _inherit = "event.event"

    event_cover_poster = fields.Binary(string="Event Image")
