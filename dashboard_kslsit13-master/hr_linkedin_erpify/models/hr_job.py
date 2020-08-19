# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning


class SocialAccount(models.Model):
    _inherit = 'social.account'

    use_for_job_posting_erpify = fields.Boolean('Use for job posting?')


class HrJobShare(models.Model):
    _inherit = 'hr.job'

    update_key = fields.Char(string='Update Key')

    def form_message_erpify(self):
        msg = '''
        We are hiring '%s', for our %s department.
        Here is the job description and other details.
        
        Job Description:
        %s
        
        No of Vacancies: %s
        
        Please check out the link below to apply for this opportunity.
        %s
        ''' % (self.name, self.department_id.name if self.department_id else '',
               self.description, self.no_of_recruitment, self.env['ir.config_parameter'].sudo().get_param('web.base.url') + self.website_url)
        return msg

    def share_linkedin(self):
        """ Button function for sharing post """
        account_ids = self.env['social.account'].search([('use_for_job_posting_erpify', '=', True)]).ids
        if not account_ids:
            raise ValidationError('Please set up a job posting account first.')
        social_post = self.env['social.post'].create({
            'image_ids': [(6, 0, self.document_ids.ids)],
            'message': self.form_message_erpify(),
            'account_ids': [(6, 0, account_ids)],
        })
        social_post.action_post()
        self.website_published = self.is_published = self.update_key = True
