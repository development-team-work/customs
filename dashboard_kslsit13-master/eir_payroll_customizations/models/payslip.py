from odoo import api, fields, models, tools, exceptions, _
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import ValidationError


class PayslipBatch(models.Model):
    _inherit = 'hr.payslip.run'

    salary_structure_id_erpify = fields.Many2one('hr.payroll.structure', string='Pay Group')
    last_batch_history = fields.Html(compute='_compute_last_batch_history_erpify', store=True)
    current_batch_details = fields.Html(compute='_compute_current_batch_details', store=True)

    @api.depends('state')
    def _compute_current_batch_details(self):
        for rec in self:
            if rec.state in ['verify', 'close']:
                dicts = self.get_figures_erpify(rec)
                currency = self.company_id.currency_id.symbol
                rec.current_batch_details = _('The summary of this batch is as follows:<br>'
                                           '<b>Gross:</b> %s %s<br>'
                                           '<b>Deductions:</b> %s %s<br>'
                                           '<b>Net:</b> %s %s<br>') % (
                                             currency, dicts['gross'], currency,
                                             dicts['deductions'],
                                             currency, dicts['net'])

    @api.depends('salary_structure_id_erpify')
    def _compute_last_batch_history_erpify(self):
        for rec in self:
            if rec.salary_structure_id_erpify:
                latest_batch = self.env['hr.payslip.run'].search([('state', '!=', 'draft'), ('id', '!=', self._origin.id),
                                                   ('salary_structure_id_erpify', '=', rec.salary_structure_id_erpify.id)],
                                                  order='date_start DESC', limit=1)
                if latest_batch:
                    dicts = self.get_figures_erpify(latest_batch)
                    currency = self.company_id.currency_id.symbol
                    rec.last_batch_history = _('Last payroll for <b>%s</b> was ran for <b>%s</b> to <b>%s</b>.<br>'
                                               'Summary is as follows:<br>'
                                               '<b>Gross:</b> %s %s<br>'
                                               '<b>Deductions:</b> %s %s<br>'
                                               '<b>Net:</b> %s %s<br>') % (
                                                 latest_batch.salary_structure_id_erpify.name, latest_batch.date_start,
                                                 latest_batch.date_end, currency, dicts['gross'], currency, dicts['deductions'],
                                                currency, dicts['net'])

            else:
                rec.last_batch_history = 'No history found.'

    def get_figures_erpify(self, batch_id):
        deductions, gross, net = 0, 0, 0
        for payslip in batch_id.slip_ids:
            if payslip.line_ids:
                deductions += sum(payslip.line_ids.filtered(lambda r: r.category_id.code == 'DED').mapped('amount'))
                gross += sum(payslip.line_ids.filtered(lambda r: r.code == 'GROSS').mapped('amount'))
                net += sum(payslip.line_ids.filtered(lambda r: r.code == 'NET').mapped('amount'))

        return {
            'gross': gross,
            'deductions': deductions,
            'net': net,
            }


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    def _get_available_contracts_domain(self):
        payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))
        if payslip_run and payslip_run.salary_structure_id_erpify:
            return [('contract_ids.state', 'in', ('open', 'close')), ('company_id', '=', self.env.company.id),
                    ('contract_id.structure_type_id.default_struct_id', '=', payslip_run.salary_structure_id_erpify.id)]
        return [('contract_ids.state', 'in', ('open', 'close')), ('company_id', '=', self.env.company.id)]
