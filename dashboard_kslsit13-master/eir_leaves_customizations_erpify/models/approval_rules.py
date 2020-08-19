# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
from odoo.tools.safe_eval import safe_eval
import datetime
import time
import dateutil

erpify_dict = {
    'person': 'Specific Person',
    'group': 'Specific Group',
    'manager': 'Direct Manager',
    '2nd_manager': 'Higher Manager',
    'dynamic': 'Dynamic Selection'
}


class Leaves(models.Model):
    _inherit = 'hr.leave.type'

    leave_rules_lines_erpify = fields.One2many('leave.approval.rules.erpify', 'leave_type_id', string='Approval Rules')
    required_docs_erpify = fields.One2many('leave.docs.management.erpify', 'leave_type_id', string='Required Documents')
    only_once_erpify = fields.Boolean('Applicable only once in service?')
    depends_erpify = fields.Boolean('Depends on another Leave type?')
    depends_leave_type_erpify = fields.Many2one('hr.leave.type', string='Depends on',
                                help="This leave can be used after consuming all the leaves in this dependent type.")
    restrict_continous_leaves_upto = fields.Integer('Restriction Continuous Leaves Upto? (Days)')


class LeaveApprovalRules(models.Model):
    _name = 'leave.approval.rules.erpify'
    _description = 'Leave Approval Rules'
    _rec_name = 'name'

    name = fields.Char()
    sequence = fields.Integer('Sequence')
    type = fields.Selection([('person', 'Specific Person'), ('group', 'Specific Group'), ('manager', 'Direct Manager'),
                             ('2nd_manager', 'Higher Manager'), ('dynamic', 'Dynamic Selection')],
                            help='Higher Manager means the manager of direct manager, '
                                 'if there would be no manager this level will be passed automatically.')
    leave_type_id = fields.Many2one('hr.leave.type')
    group_id = fields.Many2one('res.groups', 'Group')
    user_id = fields.Many2one('res.users', 'User')
    message = fields.Text('Message for the Approver')

    @api.model
    def create(self, vals_list):
        rec = super(LeaveApprovalRules, self).create(vals_list)
        rec.name = rec.leave_type_id.name + ' - ' + erpify_dict[rec.type]
        return rec
