from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date as date_obj
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools.safe_eval import safe_eval


class TimeSheetSubmissionAllowances(models.Model):
    _name = 'timesheet.submission.allowances.erpify'
    _description = 'Timesheets Allowances Submission'

    name = fields.Many2one('timesheet.allowances.category.erpify')
    hours = fields.Float()
    hours_after_TIL = fields.Float('Hours after TIL', help='Hours after applying Time in Lieu', compute='get_amount', store=True)
    amount = fields.Float(compute='get_amount', store=True)
    employee_id = fields.Many2one('hr.employee')
    submission_request_id = fields.Many2one('timesheet.submission.erpify')
    currency_id = fields.Many2one(related='submission_request_id.currency_id')
    is_weekly = fields.Boolean(related='name.is_weekly')
    compute_amount = fields.Float()
    # Fields to show
    x_rate = fields.Boolean('Rate %?', related='name.x_rate')
    x_days = fields.Boolean('Days?', related='name.x_days')
    x_hours = fields.Boolean('Hours?', related='name.x_hours')
    x_team_code = fields.Boolean('Team Code?', related='name.x_team_code')
    x_rank = fields.Boolean('Rank?', related='name.x_rank')
    x_number_of_calls = fields.Boolean('Number of Calls?', related='name.x_number_of_calls')
    # Actual Fields
    rate = fields.Float('Rate %')
    days = fields.Integer('Days')
    team_code = fields.Char('Team Code')
    rank = fields.Char('Rank')
    number_of_calls = fields.Integer('Number of Calls')

    def _compute_rule(self, localdict):
        for rec in self:
            if rec.is_weekly:
                localdict.update(**{
                    'rate': rec.rate,
                    'hours': rec.hours,
                    'days': rec.days,
                    'team_code': rec.team_code,
                    'rank': rec.rank,
                    'number_of_calls': rec.number_of_calls,
                    'result_hours': 0.0,
                    'result_amount': 0.0,
                })
                safe_eval(rec.name.python_code or 0.0, localdict, mode='exec', nocopy=True)
                self.hours = localdict['result_hours']
                self.compute_amount = localdict['result_amount']

    @api.depends('hours', 'employee_id', 'submission_request_id.time_in_lieu')
    def get_amount(self):
        for r in self:
            if r.is_weekly and r.compute_amount:
                r.amount = r.compute_amount
            else:
                til = r.hours - (r.hours * r.submission_request_id.time_in_lieu / 100)
                r.amount = til * r.employee_id.timesheet_cost
                r.hours_after_TIL = til

    def add_data(self):
        if self.submission_request_id.state == 'submit':
            raise ValidationError('You cannot change or add any allowance once the request is submitted.')
        view_id = self.env.ref('custom_timesheet_erpify.allowance_popup_timesheet_submission_form_erpify').id
        return {
            'name': _('Submit Allowance Details'),
            'view_mode': 'form',
            'views': [[view_id, 'form']],
            'res_model': 'timesheet.submission.allowances.erpify',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new'
            }


class Timesheets(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def _get_ordinary_type(self):
        default = self.env['timesheet.allowances.category.erpify'].search([('select_by_default', '=', True)], limit=1).id
        if default:
            return default
        else:
            return False

    tz = fields.Selection(related='employee_id.tz', string='Time Zone', readonly=True, store=False)
    start = fields.Float(string="From")
    end = fields.Float(string="To")
    name = fields.Char(string='Appropriation Code')
    employee_shift_erpify = fields.Many2one('resource.calender')
    timesheet_submission_erpify_id = fields.Many2one('timesheet.submission.erpify')
    type_id_erpify = fields.Many2one('timesheet.allowances.category.erpify', string='Work Type',
                                     default=_get_ordinary_type)
    unit_amount = fields.Float(compute=False, store=True, string='Actual Hours')
    calc_hours = fields.Float('Calculated Hours', compute='calculate_calculated_hours', store=True)
    start_end_mand = fields.Boolean(related='employee_id.project_id_erpify.start_end_mand')

    @api.depends('start', 'end', 'type_id_erpify', 'employee_id', 'unit_amount')
    def calculate_calculated_hours(self):
        for record in self:
            if record.type_id_erpify and record.employee_id:
                record.calc_hours = record.type_id_erpify.calculate_allowance_hours(record.unit_amount,
                                                                                    record.employee_id)

    @api.constrains('calc_hours')
    def check_limit_erpify(self):
        for record in self:
            rule = record.type_id_erpify.get_rule(record.employee_id.resource_calendar_id)
            if rule and rule.limited == 'yes':
                if rule.number_of_occurences:
                    week_start = record.date - datetime.timedelta(days=record.date.weekday())
                    week_end = record.date + datetime.timedelta(days=6 - record.date.weekday())
                    timesheet_entries = self.env['account.analytic.line'].search([('employee_id', '=', record.employee_id.id), ('date', '>=', week_start), ('date', '<=', week_end),
                                                              ('type_id_erpify', '=', record.type_id_erpify.id)])
                    if timesheet_entries and len(timesheet_entries) + 1 > rule.number_of_occurences:
                        raise ValidationError("Your limit to apply for this work type has been reached for this week, please try any other work type.")
                if rule.limit:
                    timesheet_entries = self.env['account.analytic.line'].search(
                        [('employee_id', '=', record.employee_id.id), ('date', '=', record.date),
                         ('type_id_erpify', '=', record.type_id_erpify.id)])
                    if sum(timesheet_entries.mapped('calc_hours')) + record.calc_hours > rule.limit:
                        raise ValidationError(
                            "Your limit to apply for this work type has been reached for this day, please try any other work type.")

    @api.model
    def create(self, vals):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        if not vals.get('project_id', False) or not vals.get('account_id', False):
            vals.update({'project_id': employee.project_id_erpify.id,
                         'account_id': employee.project_id_erpify.analytic_account_id.id})
        result = super(Timesheets, self).create(vals)
        result.calculate_duration()
        if result.employee_id:
            result.employee_shift_erpify = result.employee_id.resource_calendar_id.id
        return result

    @api.onchange('start', 'end')
    def calculate_duration(self):
        for r in self:
            if r.start and r.end:
                r.unit_amount = r.end - r.start
            else:
                r.unit_amount = r.unit_amount

    @api.constrains('start', 'end', 'type_id_erpify')
    def check_validaty_of_start_end(self):
        if self.start > 24:
            raise ValidationError('The starting time entered is not correct')
        if self.end > 24:
            raise ValidationError('The ending time entered is not correct')
        if self.start > self.end:
            raise ValidationError('The starting time can not be earlier than ending time.')
        self.type_id_erpify.check_restriction(self.date, self.start, self.end, self.employee_id)


class TimeSheetSubmission(models.Model):
    _name = 'timesheet.submission.erpify'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Timesheets Request'

    @api.model
    def default_get(self, field_list):
        result = super(TimeSheetSubmission, self).default_get(field_list)
        if 'employee_id' in field_list:
            result['employee_id'] = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).id
        return result

    def get_start_date(self):
        today = date_obj.today()
        current_weekday = today.weekday()
        return today - timedelta(days=current_weekday)

    def get_end_date(self):
        today = date_obj.today()
        current_weekday = today.weekday()
        return today + timedelta(days=6 - current_weekday)

    name = fields.Char(compute='_get_record_name', store=True)
    start_date = fields.Date(required=True, default=get_start_date)
    end_date = fields.Date(required=True, default=get_end_date)
    employee_id = fields.Many2one('hr.employee', required=True)
    timesheet_ids = fields.One2many('account.analytic.line', 'timesheet_submission_erpify_id')
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'), ('approved', 'Approved'),
                              ('cancel', 'Cancelled')], default='draft', string='Status')
    approval_matrix = fields.One2many('timesheet.approval.matrix', 'timesheet_submission_id')
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    submission_date = fields.Datetime()
    allowances_ids = fields.One2many('timesheet.submission.allowances.erpify', 'submission_request_id')
    allowance_total = fields.Float('Allowances', compute='_compute_all_amounts', store=True)
    normal_total = fields.Float('Basic Pay', compute='_compute_all_amounts', store=True)
    total_amount = fields.Float(compute='_compute_all_amounts', store=True)
    time_in_lieu = fields.Integer('Time in Lieu %', default=50)

    def _calculate_weekly_allowances(self):
        employee = self.employee_id
        localdict = {
            **{
                'employee': employee,
            }
        }
        for allowance in self.allowances_ids:
            allowance._compute_rule(localdict)

    @api.depends('timesheet_ids.unit_amount', 'time_in_lieu', 'start_date', 'end_date', 'employee_id', 'allowances_ids.hours')
    def _compute_all_amounts(self):
        for rec in self:
            normal_hours = rec.timesheet_ids.filtered(lambda r: r.type_id_erpify.select_by_default)
            allowance_amount = rec.allowances_ids.mapped('amount')
            rec.normal_total = (sum(normal_hours.mapped('unit_amount')) * rec.employee_id.timesheet_cost) if normal_hours else 0
            rec.allowance_total = (sum(allowance_amount)) if allowance_amount else 0
            rec.total_amount = rec.normal_total + rec.allowance_total

    @api.constrains('time_in_lieu')
    def check_time_in_lieu(self):
        if self.time_in_lieu > 100 or self.time_in_lieu < 0:
            raise ValidationError('You have entered a wrong value for time in lieu, it should be in between 0 to 100 %')

    @api.depends('employee_id', 'start_date', 'end_date')
    def _get_record_name(self):
        for r in self:
            r.name = r.employee_id.name + ': ' + r.start_date.strftime(DATE_FORMAT) + ' to ' + r.end_date.strftime(DATE_FORMAT)

    @api.constrains('start_date', 'end_date')
    def _onchange_start_date_or_end_date(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError(_('The end date should be greater than the starting date.'))
            start = self.start_date.weekday()
            end = self.end_date.weekday()
            if start != 0 or end != 6:
                raise ValidationError('Your week duration should start from Monday to Sunday.')
            duration = (self.end_date - self.start_date).days
            if duration != 6:
                raise ValidationError('A week cannot be of more or less than 7 days.')

    def fetch_timesheets(self):
        if self.start_date and self.end_date and self.employee_id:
            timesheets = self.env['account.analytic.line'].search([('employee_id', '=', self.employee_id.id), ('date', '>=', self.start_date),
                                                      ('date', '<=', self.end_date), ('timesheet_submission_erpify_id', 'in', [False, self.id]),
                                                                   ('project_id', '=', self.employee_id.project_id_erpify.id)]).ids
            if timesheets:
                self.timesheet_ids = [(6, 0, timesheets)]
            if self.allowances_ids:
                self.allowances_ids.unlink()
            all_categ = self.env['timesheet.allowances.category.erpify'].search([('select_by_default', '=', False)])
            for categ in all_categ:
                t = self.timesheet_ids.filtered(lambda r: r.type_id_erpify.id == categ.id)
                if t:
                    t_sum = sum(t.mapped('calc_hours'))
                else:
                    t_sum = 0
                self.env['timesheet.submission.allowances.erpify'].create({
                    'name': categ.id,
                    'hours': t_sum,
                    'submission_request_id': self.id,
                    'employee_id': self.employee_id.id,
                    'hours_after_TIL': t_sum - (t_sum * self.time_in_lieu / 100),
                })

    def cancel(self):
        self.state = 'cancel'
        self.timesheet_ids = [(5)]

    def approve_reject(self):
        return {
            'name': _('Approve or Reject the timesheets'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'popup.wizard.timesheet',
            'target': 'new',
            'context': dict(
                self.env.context,
                default_user_id=self.env.user.id,
                default_timesheet_submission_id=self.id,
            ),
        }

    def submit_request(self):
        self.submission_date = datetime.now()
        self.state = 'submit'
        self._calculate_weekly_allowances()


class ApprovalMatrixTimesheet(models.Model):
    _name = 'timesheet.approval.matrix'
    _description = 'Timesheet Approval Matrix'

    user_id = fields.Many2one('res.users', 'Approver')
    checked_at = fields.Datetime()
    status = fields.Selection([('approve', 'Approved'), ('reject', 'Rejected')])
    comments = fields.Text()
    timesheet_submission_id = fields.Many2one('timesheet.submission.erpify')


class Wizard(models.TransientModel):
    _name = 'popup.wizard.timesheet'

    comments = fields.Text('Comments')
    user_id = fields.Many2one('res.users')
    timesheet_submission_id = fields.Many2one('timesheet.submission.erpify')
    status = fields.Selection([('approve', 'Approve'), ('reject', 'Reject')], string='Action to Perform?')

    def proceed(self):
        self.timesheet_submission_id.approval_matrix.create({
            'user_id': self.user_id.id,
            'checked_at': datetime.now(),
            'status': self.status,
            'comments': self.comments,
            'timesheet_submission_id': self.timesheet_submission_id.id,
        })


class Employee(models.Model):
    _inherit = 'hr.employee'

    project_id_erpify = fields.Many2one('project.project', 'Timesheet Project')
    time_in_lieu_balance = fields.Float('Time in Lieu Balance (hours)')


class TimesheetProject(models.Model):
    _inherit = 'project.project'

    start_end_mand = fields.Boolean('Is Start and End time Mandatory?', default=True)