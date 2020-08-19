from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
from odoo.tools.safe_eval import safe_eval
from datetime import date, timedelta
import time
from dateutil.relativedelta import relativedelta


class Employee(models.Model):
    _inherit = "hr.employee"

    def get_number_of_leaves_in(self, leave_types=[], lastmonths=12):
        since = date.today() - relativedelta(months=lastmonths)
        applied_leaves = self.env['hr.leave'].search([('employee_id', '=', self.id), ('state', '=', 'validate'), ('holiday_status_id', 'in', leave_types),
                                     ('request_date_from', '>=', since)])
        if applied_leaves:
            return sum(applied_leaves.mapped('number_of_days'))
        else:
            return 0

    def get_probation_leaves(self, date_from, date_to):
        leaves = self.env['hr.leave'].search([('employee_was_on_probation', '=', True), ('state', '=', 'validate'),
                                     ('date_from', '>=', date_from), ('date_to', '<=', date_to), ('employee_id', '=', self.id)])
        if leaves:
            return sum(leaves.mapped('number_of_days'))
        else:
            return 0

