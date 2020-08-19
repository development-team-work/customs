from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class Allowances(models.Model):
    _name = 'timesheet.allowances.category.erpify'
    _description = 'Timesheet Allowances Categories'

    name = fields.Char(required=True)
    start = fields.Float('Start')
    end = fields.Float('End')
    active = fields.Boolean('Active', default=True, tracking=True)
    show_in_timesheet = fields.Boolean('Show while entering timesheets?', default=True)
    select_by_default = fields.Boolean('Select by Default?')
    apply_restriction = fields.Selection([('no', 'No'), ('schedule', "Based on Employee's Work Schedule"),
                                          ('define', 'As defined in Start and End time')], string='Apply Restrictions?', default='no')
    rule_line_ids = fields.One2many('timesheet.allowances.rules.erpify', 'timesheet_allowance_categ_id', string='Rules')
    is_weekly = fields.Boolean('Is weekly?')
    python_code = fields.Text('Python Code')
    x_rate = fields.Boolean('Rate %?')
    x_days = fields.Boolean('Days?')
    x_hours = fields.Boolean('Hours?')
    x_team_code = fields.Boolean('Team Code?')
    x_rank = fields.Boolean('Rank?')
    x_number_of_calls = fields.Boolean('Number of Calls?')

    def check_restriction(self, date, start, end, employee_id):
        if self.apply_restriction == 'no':
            return True
        elif self.apply_restriction == 'define':
            if self.end > start >= self.start and self.start < end <= self.end:
                return True
            else:
                raise ValidationError('Your start and ending time is not applicable for this work type.')
        elif self.apply_restriction == 'schedule':
            days = employee_id.resource_calendar_id.attendance_ids.filtered(lambda r: r.dayofweek == str(date.weekday()))
            s = min(days.mapped('date_from'))
            e = max(days.mapped('date_to'))
            if e > start >= s and s < end <= e:
                return True
            else:
                raise ValidationError('Your start and ending time is not applicable for this work type.')

    def calculate_allowance_hours(self, actual_hours, employee_id):
        rule = self.rule_line_ids.filtered(lambda r: employee_id.resource_calendar_id.id in r.applicable_to.ids)
        if not rule:
            return actual_hours
        prev, hours = 0, 0
        if rule.round_up and actual_hours < rule.round_up:
            actual_hours = rule.round_up
        for line in rule.rule_details:
            if prev < actual_hours:
                hours += (line.upto * line.rate) if actual_hours > line.upto else ((actual_hours - prev) * line.rate)
                prev = line.upto
        return hours

    def get_rule(self, resource):
        for rule in self.rule_line_ids:
            if resource.id in rule.applicable_to.ids:
                return rule
        return False


class AllowanceRules(models.Model):
    _name = 'timesheet.allowances.rules.erpify'
    _description = 'Timesheet Allowances Rules'

    timesheet_allowance_categ_id = fields.Many2one('timesheet.allowances.category.erpify')
    applicable_to = fields.Many2many('resource.calendar')
    rule_details = fields.One2many('timesheet.allowances.rules.details.erpify', 'rule_id', string='Parameters Details')
    limited = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    limit = fields.Float('Daily Limit')
    number_of_occurences = fields.Integer(help='How many times it can appear in a weekly timesheet submission?')
    round_up = fields.Float('Round Up?')


class AllowanceRuleDetails(models.Model):
    _name = 'timesheet.allowances.rules.details.erpify'
    _description = 'Timesheet Allowances Rule Details'

    upto = fields.Float('Hours Upto')
    rate = fields.Float('Rate Multiplier')
    rule_id = fields.Many2one('timesheet.allowances.rules.erpify')