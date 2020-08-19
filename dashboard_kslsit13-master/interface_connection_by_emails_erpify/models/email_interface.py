# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
from odoo.tools.safe_eval import safe_eval
import base64
import time
import dateutil


class InterfaceEmailERPify(models.Model):
    _name = 'email.interfaces.erpify'
    _inherit = ['mail.thread']
    _description = 'Interfaces Through Emails'
    _rec_name = 'name'

    def _get_alias_domain(self):
        alias_domain = self.env["ir.config_parameter"].sudo().get_param("mail.catchall.domain")
        for record in self:
            record.alias_domain = alias_domain

    name = fields.Char(required=True)
    model_name = fields.Many2one('ir.model', required=True, string='Model')
    state = fields.Selection([('inactive', 'Inactive'), ('active', 'Active')], default='inactive', track_visibility='onchange')
    file_type = fields.Selection([('text', 'Text')], required=True, default='text')
    separator = fields.Char('Separator')
    field_ids = fields.Many2many('ir.model.fields', domain="[('ttype', 'not in', ['many2many', 'many2one', 'one2many'])]")
    columns = fields.Integer('Number of Columns')
    alias_name = fields.Char('Alias Name', help="The name of the email alias, e.g. 'jobs' if you want to catch emails for <jobs@example.odoo.com>", track_visibility='onchange')
    alias_domain = fields.Char('Alias domain', compute='_get_alias_domain',
                               default=lambda self: self.env["ir.config_parameter"].sudo().get_param(
                                   "mail.catchall.domain"))

    @api.constrains('alias_name')
    def _check_alias_name(self):
        found = self.env['email.interfaces.erpify'].search([('alias_name', '=', self.alias_name)])
        if len(found) > 1:
            raise ValidationError('This alias is already exists in the system. Please try a new one.')

    def activate(self):
        self.state = 'active'

    def deactivate(self):
        self.state = 'inactive'

    def search_create_write(self, column1):
        # If it finds the record it returns its ID
        # Else it returns false
        record = self.env[self.model_name.model].search([(self.field_ids[0].name, '=', column1)])
        if record:
            return record
        return False

    def get_and_store_decoded_data(self, attachment):
        new_records = 0
        updated = 0
        for a in attachment:
            for line in a.index_content.splitlines():
                temp_dict = {}
                datas = line.split(self.separator)
                r = self.search_create_write(datas[0].strip())
                for i in range(self.columns):
                    temp_dict.update({self.field_ids[i].name: datas[i].strip()})
                if r:
                    r.write(temp_dict)
                    updated += 1
                else:
                    self.env[self.model_name.model].create(temp_dict)
                    new_records += 1
        return new_records

    def create_attachments_from_class(self, attachments, model, res_id):
        for attachment in attachments:
            cid = False
            if len(attachment) == 2:
                name, content = attachment
            elif len(attachment) == 3:
                name, content, info = attachment
                cid = info and info.get('cid')
            else:
                continue
            if isinstance(content, str):
                content = content.encode('utf-8')
            elif content is None:
                continue
            attachement_values = {
                'name': name,
                'datas': base64.b64encode(content),
                'type': 'binary',
                'description': name,
                'res_model': model,
                'res_id': res_id,
            }
        new_attachments = self.env['ir.attachment'].create(attachement_values)
        return new_attachments

