from odoo import api, fields, models, tools, exceptions, _
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import ValidationError


class Company(models.Model):
    _inherit = 'res.company'

    lock_transaction_erpify = fields.Boolean('Lock Transactions while Payroll is In-Progress?')


class Leaves(models.Model):
    _inherit = 'hr.leave'

    def write(self, vals):
        res = super(Leaves, self).write(vals)
        pending = self.employee_id.slip_ids.filtered(lambda r: r.state in ['draft', 'verify'])
        if pending and self.env.user.company_id.lock_transaction_erpify:
            raise ValidationError("You cannot make changes to the record because a payroll is in progress for this employee.")
        return res


class TimesheetSubmission(models.Model):
    _inherit = 'timesheet.submission.erpify'

    def approve_reject(self):
        pending = self.employee_id.slip_ids.filtered(lambda r: r.state in ['draft', 'verify'])
        if pending and self.env.user.company_id.lock_transaction_erpify:
            raise ValidationError(
                "You cannot make changes to the record because a payroll is in progress for this employee.")
        return super(TimesheetSubmission, self).approve_reject()


class Allocation(models.Model):
    _inherit = 'hr.leave.allocation'

    allocation_period_start = fields.Date('Allocation for the period')
    allocation_period_end = fields.Date('Ending')


class LeaveReport(models.Model):
    _inherit = "hr.leave.report"

    allocation_period_start = fields.Date('Allocation for the period', readonly=True)
    allocation_period_end = fields.Date('Ending', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_leave_report')

        self._cr.execute("""
                CREATE or REPLACE view hr_leave_report as (
                    SELECT row_number() over(ORDER BY leaves.employee_id) as id,
                    leaves.employee_id as employee_id, leaves.name as name,
                    leaves.number_of_days as number_of_days, leaves.leave_type as leave_type,
                    leaves.category_id as category_id, leaves.department_id as department_id,
                    leaves.holiday_status_id as holiday_status_id, leaves.state as state,
                    leaves.holiday_type as holiday_type, leaves.date_from as date_from,
                    leaves.date_to as date_to, leaves.payslip_status as payslip_status,
                    leaves.allocation_period_end as allocation_period_end, leaves.allocation_period_start as allocation_period_start

                    from (select
                        allocation.employee_id as employee_id,
                        allocation.name as name,
                        allocation.number_of_days as number_of_days,
                        allocation.category_id as category_id,
                        allocation.department_id as department_id,
                        allocation.holiday_status_id as holiday_status_id,
                        allocation.state as state,
                        allocation.holiday_type,
                        null as date_from,
                        null as date_to,
                        FALSE as payslip_status,
                        'allocation' as leave_type,
                        allocation.allocation_period_start AS allocation_period_start,
                        allocation.allocation_period_end AS allocation_period_end
                    from hr_leave_allocation as allocation
                    union all select
                        request.employee_id as employee_id,
                        request.name as name,
                        (request.number_of_days * -1) as number_of_days,
                        request.category_id as category_id,
                        request.department_id as department_id,
                        request.holiday_status_id as holiday_status_id,
                        request.state as state,
                        request.holiday_type,
                        request.date_from as date_from,
                        request.date_to as date_to,
                        request.payslip_status as payslip_status,
                        'request' as leave_type,
                        null AS allocation_period_start,
                        null AS allocation_period_end
                    from hr_leave as request) leaves
                );
            """)

