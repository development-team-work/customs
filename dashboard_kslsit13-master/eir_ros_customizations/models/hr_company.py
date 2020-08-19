from odoo import api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import ValidationError, Warning


class Company(models.Model):
    _inherit = 'res.company'

    ros_certificate_file = fields.Binary('Certificate File')
    ros_password = fields.Char('Password')
    ros_connectivity_status = fields.Selection([('connected', 'Connected'), ('disconnected', 'Disconnected')], string='Connectivity Status')

    def connect_with_ros(self):
        if not self.ros_certificate_file and not self.ros_password:
            raise ValidationError('Please enter the certificate and password first!')