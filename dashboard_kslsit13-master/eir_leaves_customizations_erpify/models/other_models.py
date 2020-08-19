from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning, AccessError
from datetime import datetime

erpify_dict = {
    'person': 'Specific Person',
    'group': 'Specific Group',
    'manager': 'Direct Manager',
    '2nd_manager': 'Higher Manager',
    'dynamic': 'Dynamic Selection'
}


class DynamicApproval(models.TransientModel):
    _name = 'dynamic.approver.selector.erpify'

    user_id = fields.Many2one('res.users', 'Approver')
    comments = fields.Text('Comments for Approver')
    leave_id_erpify = fields.Many2one('hr.leave')

    def action_assign(self):
        self.leave_id_erpify.dynamic_approver_responsible_erpify = self.user_id.id
        holiday = self.leave_id_erpify
        note = _('New %s Request created by %s from %s to %s.'
                 '\n Please read the following instructions:\n %s') % (
                   holiday.holiday_status_id.name, holiday.create_uid.name,
                   fields.Datetime.to_string(holiday.date_from),
                   fields.Datetime.to_string(holiday.date_to), self.leave_id_erpify.get_note_for_approver_erpify())
        holiday.activity_schedule(
            'hr_holidays.mail_act_leave_approval',
            note=self.comments if self.comments else note,
            user_id=self.user_id.id)
        holiday.message_post(body='@' + self.env.user.name + ' chose ' + self.user_id.name +' to approve this leave.',
                          subject='Approver Selection')
        return True


class AttachedDocs(models.Model):
    _name = 'leave.attached.docs.erpify'

    name = fields.Char('Document Name')
    is_uploaded = fields.Boolean('Is Uploaded?', compute='_check_uploaded')
    doc_lines = fields.One2many('ir.attachment', 'attached_leave_doc_id_erpify', string="Docs Upload")
    leave_id = fields.Many2one('hr.leave')

    @api.depends('doc_lines')
    def _check_uploaded(self):
        for doc in self:
            if doc.doc_lines:
                doc.is_uploaded = True
            else:
                doc.is_uploaded = False


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    attached_leave_doc_id_erpify = fields.Many2one('leave.attached.docs.erpify')


class ApprovalHistory(models.Model):
    _name = 'approval.history.erpify'

    name = fields.Char('Approval Type')
    sequence = fields.Integer('Sequence')
    date_done = fields.Datetime('Approved At')
    approved_by = fields.Many2one('res.users', string='Approved By')
    leave_id = fields.Many2one('hr.leave')


class ActualLeave(models.Model):
    _inherit = "hr.leave"

    @api.model
    def default_get(self, fields_list):
        defaults = super(ActualLeave, self).default_get(fields_list)
        defaults = self._default_get_request_parameters(defaults)

        LeaveType = self.env['hr.leave.type'].with_context(employee_id=defaults.get('employee_id'),
                                                           default_date_from=defaults.get('date_from',
                                                                                          fields.Datetime.now()))
        lt = LeaveType.search([('valid', '=', True)], limit=1)

        defaults['holiday_status_id'] = lt.id if lt else defaults.get('holiday_status_id')
        defaults['state'] = 'draft'
        return defaults

    @api.depends('attached_leave_docs_erpify')
    def _compute_attached_leave_docs_erpify(self):
        for rec in self:
            if not rec.attached_leave_docs_erpify:
                rec.is_documents_attached = False
            else:
                rec.is_documents_attached = all(rec.attached_leave_docs_erpify.mapped('is_uploaded'))

    attached_leave_docs_erpify = fields.One2many('leave.attached.docs.erpify', 'leave_id')
    is_documents_attached = fields.Boolean('Documents Attached?', compute='_compute_attached_leave_docs_erpify', store=True)
    ongoing_approval = fields.Integer()
    kanban_state = fields.Selection([
        ('normal', 'To Submit'),
        ('done', 'All Approvals Done'),
        ('blocked', 'Waiting Approval(s)')
    ], string='Kanban State', default='normal', tracking=True, copy=False)
    approval_history_ids = fields.One2many('approval.history.erpify', 'leave_id', 'Leave Approvals')
    dynamic_approver_responsible_erpify = fields.Many2one('res.users')
    can_assign_dynamic_approver = fields.Boolean(compute='_can_assign_dynamic_approver_erpify')
    employee_was_on_probation = fields.Boolean()

    @api.depends('state', 'employee_id', 'ongoing_approval')
    def _can_assign_dynamic_approver_erpify(self):
        self.can_assign_dynamic_approver = False
        if self.holiday_status_id.leave_rules_lines_erpify:
            approval = self.holiday_status_id.leave_rules_lines_erpify.filtered(
                lambda r: r.sequence == self.ongoing_approval)
            if approval.type == 'dynamic' and approval.user_id.id == self.env.uid:
                self.can_assign_dynamic_approver = True

    def get_note_for_approver_erpify(self):
        if self.holiday_status_id.leave_rules_lines_erpify:
            approval = self.holiday_status_id.leave_rules_lines_erpify.filtered(
                lambda r: r.sequence == self.ongoing_approval)
            return approval.message
        else:
            return False

    def check_employee_probation_erpify(self):
        if self.sudo().employee_id.contract_id and self.sudo().employee_id.contract_id.trial_date_end:
            if self.date_to.date() <= self.sudo().employee_id.contract_id.trial_date_end:
                return True
        return False

    @api.model
    def create(self, vals):
        leave = super(ActualLeave, self).create(vals)
        leave.employee_was_on_probation = leave.check_employee_probation_erpify()
        if leave.holiday_status_id.only_once_erpify:
            found = self.env['hr.leave'].search(
                [('employee_id', '=', leave.employee_id.id), ('holiday_status_id', '=', leave.holiday_status_id.id),
                 ('state', 'not in', ['cancel', 'refuse'])])
            if found:
                raise ValidationError("Sorry, you have already applied for this leave, so you can not apply again. This leave is allowed only once in your service.")
        if leave.holiday_status_id.depends_erpify:
            history_usage = self.env['hr.leave.report'].search(
                [('employee_id', '=', leave.employee_id.id), ('holiday_status_id', '=', leave.holiday_status_id.depends_leave_type_erpify.id),
                 ('state', '=', 'validate')])
            remaining_found = sum(history_usage.mapped('number_of_days'))
            if remaining_found > 0:
                raise ValidationError("Sorry, you have " + leave.holiday_status_id.depends_leave_type_erpify.name + " available. Please utilize it first before applying to this category.")
        if leave.holiday_status_id.restrict_continous_leaves_upto and leave.number_of_days > leave.holiday_status_id.restrict_continous_leaves_upto:
            raise ValidationError(
                "Sorry, you can not apply for " + leave.holiday_status_id.name + " continuously for more than " + str(leave.holiday_status_id.restrict_continous_leaves_upto) + " day(s). Please try with any other leave type.")

        docs = self.env['leave.docs.management.erpify'].search([('leave_type_id', '=', leave.holiday_status_id.id)])
        for d in docs:
            self.env['leave.attached.docs.erpify'].create({
                'name': d.name,
                'leave_id': leave.id,
            })
        for line in leave.holiday_status_id.leave_rules_lines_erpify:
            self.env['approval.history.erpify'].create({
                'name': erpify_dict[line.type],
                'sequence': line.sequence,
                'leave_id': leave.id,
            })
        return leave

    def _get_responsible_for_approval(self):
        self.ensure_one()
        if self.holiday_status_id.leave_rules_lines_erpify:
            responsible = self._get_responsible_for_approval_erpify()
            return responsible
        responsible = super(ActualLeave, self)._get_responsible_for_approval()
        return responsible

    def _get_responsible_for_approval_erpify(self):
        approval = self.holiday_status_id.leave_rules_lines_erpify.filtered(
            lambda r: r.sequence == self.ongoing_approval)
        if approval.type in ['person', 'dynamic']:
            return approval.user_id
        elif approval.type == 'manager':
            if self.sudo().employee_id.parent_id:
                return self.sudo().employee_id.parent_id.user_id
            else:
                self.message_post(body='No direct manager found for this employee,'
                                       ' system is moving to the next approval.', subject=approval.name)
                self.sudo().action_approve_erpify()
                return False
        elif approval.type == '2nd_manager':
            if self.sudo().employee_id.parent_id and self.sudo().employee_id.parent_id.parent_id:
                return self.sudo().employee_id.parent_id.parent_id.user_id
            else:
                self.message_post(body='No higher manager found for this employee,'
                                       ' system is moving to the next approval.', subject=approval.name)
                self.sudo().action_approve_erpify()
                return False
        elif approval.type == 'dynamic':
            self.message_post(body='@'+approval.user_id.name+' needs to assign the next approver.', subject=approval.name)
            return False
        else:
            return approval.group_id.users

    def activity_update(self):
        if self.holiday_status_id.leave_rules_lines_erpify:
            self.activity_update_erpify()
        else:
            super(ActualLeave, self).activity_update()

    def activity_update_erpify(self):
        to_clean, to_do = self.env['hr.leave'], self.env['hr.leave']
        for holiday in self:
            note = _('New %s Request created by %s from %s to %s.'
                     '\n Please read the following instructions:\n %s') % (
                       holiday.holiday_status_id.name, holiday.create_uid.name,
                       fields.Datetime.to_string(holiday.date_from),
                       fields.Datetime.to_string(holiday.date_to), self.get_note_for_approver_erpify())
            # if holiday.state == 'draft':
            #     to_clean |= holiday
            if holiday.state in ['confirm', 'draft']:
                responsibles = self._get_responsible_for_approval_erpify()
                if responsibles:
                    for responsible in responsibles:
                        holiday.activity_schedule(
                            'hr_holidays.mail_act_leave_approval',
                            note=note,
                            user_id=responsible.id)
            elif holiday.state == 'validate':
                to_do |= holiday
            elif holiday.state == 'refuse':
                to_clean |= holiday
        if to_clean:
            to_clean.sudo().activity_unlink(
                ['hr_holidays.mail_act_leave_approval', 'hr_holidays.mail_act_leave_second_approval'])
        if to_do:
            to_do.sudo().activity_feedback(
                ['hr_holidays.mail_act_leave_approval', 'hr_holidays.mail_act_leave_second_approval'])

    def action_approve(self):
        # if validation_type == 'both': this method is the first approval approval
        # if validation_type != 'both': this method calls action_validate() below
        if self.holiday_status_id.leave_rules_lines_erpify:
            self.action_approve_erpify()
            return True
        if any(holiday.state != 'confirm' for holiday in self):
            raise UserError(_('Time off request must be confirmed ("To Approve") in order to approve it.'))

        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        self.filtered(lambda hol: hol.validation_type == 'both').write(
            {'state': 'validate1', 'first_approver_id': current_employee.id})

        # Post a second message, more verbose than the tracking message
        for holiday in self.filtered(lambda holiday: holiday.employee_id.user_id):
            holiday.message_post(
                body=_('Your %s planned on %s has been accepted' % (
                holiday.holiday_status_id.display_name, holiday.date_from)),
                partner_ids=holiday.employee_id.user_id.partner_id.ids)

        self.filtered(lambda hol: not hol.validation_type == 'both').action_validate()
        if not self.env.context.get('leave_fast_create'):
            self.activity_update()
        return True

    def action_approve_erpify(self):
        max_approval = max(self.holiday_status_id.leave_rules_lines_erpify.mapped('sequence'))
        if self.ongoing_approval >= max_approval:
            if not all(self.attached_leave_docs_erpify.mapped('is_uploaded')):
                raise ValidationError('All the required documents are needed to be uploaded before the final approval.')
            history = self.approval_history_ids.filtered(
                lambda r: r.sequence == self.ongoing_approval)
            history.date_done = datetime.now()
            history.approved_by = self.env.uid
            self.action_validate()
            self.kanban_state = 'done'
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=self.request_date_to,
                note='To report in when the leave period is completed.',
                user_id=self.employee_id.user_id.id)
        else:
            history = self.approval_history_ids.filtered(lambda r: r.sequence == self.ongoing_approval)
            history.date_done = datetime.now()
            history.approved_by = self.env.uid
            self.ongoing_approval += 1
            self.activity_update_erpify()

    @api.depends('state', 'employee_id', 'department_id')
    def _compute_can_approve(self):
        for holiday in self:
            if holiday.holiday_status_id.leave_rules_lines_erpify:
                self._compute_can_approve_erpify(holiday)
                continue
            try:
                if holiday.state == 'confirm' and holiday.holiday_status_id.validation_type == 'both':
                    holiday._check_approval_update('validate1')
                else:
                    holiday._check_approval_update('validate')
            except (AccessError, UserError):
                holiday.can_approve = False
            else:
                holiday.can_approve = True

    def _compute_can_approve_erpify(self, leave):
        approval = leave.holiday_status_id.leave_rules_lines_erpify.filtered(
            lambda r: r.sequence == leave.ongoing_approval)
        if approval.type == 'person':
            if self.env.uid == approval.user_id.id:
                leave.can_approve = True
            else:
                leave.can_approve = False
        elif approval.type == 'group':
            if approval.group_id.id in self.env.user.groups_id.ids:
                leave.can_approve = True
            else:
                leave.can_approve = False
        elif approval.type == 'manager':
            if leave.sudo().employee_id.parent_id and leave.sudo().employee_id.parent_id.user_id.id == self.env.uid:
                leave.can_approve = True
            else:
                leave.can_approve = False
        elif approval.type == 'dynamic':
            if leave.dynamic_approver_responsible_erpify and leave.dynamic_approver_responsible_erpify.id == self.env.uid:
                leave.can_approve = True
            else:
                leave.can_approve = False
        else:
            if leave.sudo().employee_id.parent_id and leave.sudo().employee_id.parent_id.parent_id and leave.sudo().employee_id.parent_id.parent_id.user_id.id == self.env.uid:
                leave.can_approve = True
            else:
                leave.can_approve = False

    def action_confirm(self):
        res = super(ActualLeave, self).action_confirm()
        self.kanban_state = 'blocked'

    def action_assign_dynamic_approver_erpify(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign a new Approver'),
            'res_model': 'dynamic.approver.selector.erpify',
            'view_mode': 'form',
            'target': 'new',
            'context':  {
                'default_leave_id_erpify': self.id,
            },
        }

    def master_approve_erpify(self):
        if not self.name:
            raise UserError('Please add a description first!')
        self.action_validate()
        self.message_post(body='This request has been approved by the master user ' + self.env.user.name + '. Thanks!',
                          subject='Forced Approval!')


class DocsManagement(models.Model):
    _name = 'leave.docs.management.erpify'

    name = fields.Char('Document Name', required=True)
    leave_type_id = fields.Many2one('hr.leave.type')
