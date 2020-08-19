from odoo import api, fields, models, tools, exceptions, _
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = 'hr.contract'

    def write(self, vals):
        res = super(Contract, self).write(vals)
        pending = self.employee_id.slip_ids.filtered(lambda r: r.state in ['draft', 'verify'])
        if pending and self.env.user.company_id.lock_transaction_erpify:
            raise ValidationError("You cannot make changes to the record because a payroll is in progress for this employee.")
        return res

    def fetch_data_from_ros(self):
        # Method to fetch data from ROS
        return True


class Employee(models.Model):
    _inherit = 'hr.employee'

    def write(self, vals):
        res = super(Employee, self).write(vals)
        pending = self.slip_ids.filtered(lambda r: r.state in ['draft', 'verify'])
        if pending:
            raise ValidationError("You cannot make changes to the record because a payroll is in progress for this employee.")
        return res

    bank_account_no = fields.Char('Bank Account Number')
    joining_date = fields.Date('Joining Date')
    leaving_date = fields.Date('Leaving Date')
    remaining_leaves_offboarding_erpify = fields.Float('Leaves Balance on Off Boarding')

    def get_remaining_leaves_offboarding_erpify(self):
        if self.contract_id:
            total_allocations = self.env['hr.leave.report'].search([('employee_id', '=', self.id), ('state', '=', 'validate'),
                                                                        ('leave_type', '=', 'allocation'), ('holiday_status_id.allocation_type', 'in', ['fixed_allocation', 'fixed'])])
            current_year_allocations = self.env['hr.leave.report'].search([('employee_id', '=', self.id), ('allocation_period_start', '>=', self.contract_id.date_start),
                                                    ('state', '=', 'validate'), ('leave_type', '=', 'allocation'), ('holiday_status_id.allocation_type', 'in', ['fixed_allocation', 'fixed'])])
            leaves_till_leaving_date = self.env['hr.leave.report'].search([('employee_id', '=', self.id), ('state', '=', 'validate'), ('leave_type', '=', 'request'), ('holiday_status_id.allocation_type', 'in', ['fixed_allocation', 'fixed'])])
            total_allocations = sum(total_allocations.mapped('number_of_days')) if total_allocations else 0
            current_year_allocations = sum(current_year_allocations.mapped('number_of_days')) if current_year_allocations else 0
            leaves_till_leaving_date = sum(
                leaves_till_leaving_date.mapped('number_of_days')) if leaves_till_leaving_date else 0
            accrual_balance = (current_year_allocations / 52) * self.leaving_date.isocalendar()[1]
            self.remaining_leaves_offboarding_erpify = total_allocations - current_year_allocations + accrual_balance - leaves_till_leaving_date

    def initiate_termination(self):
        if len(self) == 1 and not self.leaving_date:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Register Departure/Termination'),
                'res_model': 'hr.departure.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'active_id': self.id},
                'views': [[False, 'form']]
            }


class HrDepartureWizard(models.TransientModel):
    _inherit = 'hr.departure.wizard'

    leaving_date = fields.Date('Leaving Date', required=True)
    departure_reason = fields.Selection([
        ('fired', 'Fired'),
        ('resigned', 'Resigned'),
        ('retired', 'Retired'),
        ('died', 'Died'),
    ], string="Departure Reason", default="fired", required=True)

    def action_register_departure(self):
        super(HrDepartureWizard, self).action_register_departure()
        self.employee_id.leaving_date = self.leaving_date
        self.employee_id.get_remaining_leaves_offboarding_erpify()
