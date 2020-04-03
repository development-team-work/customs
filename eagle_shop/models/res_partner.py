# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import _,fields, models,api
from odoo.osv.expression import get_unaccent_wrapper
import re

class res_partner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(index=True, translate=True)
    nick = fields.Char("Nick Name",default="")
    is_writer=fields.Boolean("Is a Writer",default=False , translate=True)
    is_publisher=fields.Boolean("Is a Publisher",default=False , translate=True)
    # book_ids=fields.Many2many('product.template',string="Books")
    published=fields.One2many('product.template','publisher_id',string="Publications", translate=True)
    written=fields.Many2many('product.template','partner_product_template_rel','writer_ids','written',string="Written Books", translate=True)
    balance=fields.Monetary(string="Balance",compute='calculate_balance',  help="Balance for this account.")


    def name_get(self):
        result = []
        for record in self:
            if record.ref:
                record_name = record.name + ' ( ' + record.ref + ' )'
            else:
                record_name = record.name
            result.append((record.id, record_name))
        return result

    @api.depends_context('force_company')
    def calculate_balance(self):
        tables, where_clause, where_params = self.env['account.move.line'].with_context(state='posted',
                                                                                        company_id=self.env.company.id)._query_get()
        where_params = [tuple(self.ids)] + where_params
        if where_clause:
            where_clause = 'AND ' + where_clause
        self._cr.execute("""SELECT account_move_line.partner_id, act.type, SUM(account_move_line.amount_residual)
                         FROM """ + tables + """
                         LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                         LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                         WHERE act.type IN ('receivable','payable')
                         AND account_move_line.partner_id IN %s
                         AND account_move_line.reconciled IS FALSE
                         """ + where_clause + """
                         GROUP BY account_move_line.partner_id, act.type
                         """, where_params)
        treated = self.browse()
        bal=0
        for pid, type, val in self._cr.fetchall():
            partner = self.browse(pid)
            if type == 'receivable':
                bal = bal+val
            elif type == 'payable':
                bal = bal+val
        self.balance=bal

    def _get_name(self):
        """ Utility method to allow name_get to be overrided without re-browse the partner """
        partner = self
        name = partner.name or ''

        if partner.company_name or partner.parent_id:
            if not name and partner.type in ['invoice', 'delivery', 'other']:
                name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
            if not partner.is_company:
                name = "%s, (%s)" % ( name,partner.commercial_company_name or partner.parent_id.name)
        if self._context.get('show_address_only'):
            name = partner._display_address(without_company=True)
        if self._context.get('show_address'):
            name = name + "\n" + partner._display_address(without_company=True)
        name = name.replace('\n\n', '\n')
        name = name.replace('\n\n', '\n')
        if self._context.get('address_inline'):
            name = name.replace('\n', ', ')
        if self._context.get('show_email') and partner.email:
            name = "%s <%s>" % (name, partner.email)
        if self._context.get('show_phone') and partner.phone:
            name = "%s <%s>" % (name, partner.phone)
        if self._context.get('show_mobile') and partner.mobile:
            name = "%s <%s>" % (name, partner.mobile)
        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        if self._context.get('show_vat') and partner.vat:
            name = "%s ‒ %s" % (name, partner.vat)
        return name

    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None,show_mobile=None,show_phone=None, html_format=None, show_vat=False)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)

#### this is for searching partner From others module ie. invoice, Purchase orders etc
    # here I added 2 lines,and edited one to search partner by Mobile
    #1 OR {mobile} {operator} {percent}
    #2  mobile=unaccent('res_partner.mobile'),
    # and edited [search_name]*3 for the followings to add one extra arguments
    #3  where_clause_params += [search_name]*4  # for email / display_name, reference

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        self = self.with_user(name_get_uid or self.env.uid)
        if args is None:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            from_str = from_clause if from_clause else 'res_partner'
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

            query = """SELECT res_partner.id
                         FROM {from_str}
                      {where} ({email} {operator} {percent}
                           OR {display_name} {operator} {percent}
                           OR {mobile} {operator} {percent}
                           OR {phone} {operator} {percent}
                           OR {reference} {operator} {percent}
                           OR {vat} {operator} {percent})
                           -- don't panic, trust postgres bitmap
                     ORDER BY {display_name} {operator} {percent} desc,
                              {display_name}
                    """.format(from_str=from_str,
                               where=where_str,
                               operator=operator,
                               email=unaccent('res_partner.email'),
                               display_name=unaccent('res_partner.display_name'),
                               mobile=unaccent('res_partner.mobile'),
                               phone=unaccent('res_partner.phone'),
                               reference=unaccent('res_partner.ref'),
                               percent=unaccent('%s'),
                               vat=unaccent('res_partner.vat'),)

            where_clause_params += [search_name]*5  # for email / display_name, reference
            where_clause_params += [re.sub('[^a-zA-Z0-9]+', '', search_name) or None]  # for vat
            where_clause_params += [search_name]  # for order by
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            self.env.cr.execute(query, where_clause_params)
            partner_ids = [row[0] for row in self.env.cr.fetchall()]

            if partner_ids:
                return self.browse(partner_ids).name_get()
            else:
                return []
        return super(res_partner, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)
