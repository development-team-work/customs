# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv.expression import get_unaccent_wrapper
import datetime
import re

from odoo.addons.base.models.res_partner import Partner


class PersonalDetails(models.Model):
    _inherit = 'res.partner'
    _description = "force member's personal Details for ribbon, medal, cap, belt, ranks etc"
    is_force=fields.Boolean("Is a Force",default=False )
    force_id = fields.Many2one("ribbon.force","Force")
    id_no=fields.Char("ID No")
    rank = fields.Many2one("ribbon.rank","Rank")
    unit=fields.Many2one("ribbon.force.unit",string="Force Unit",domain="[('force_name','=',force_id)]")
    post=fields.Many2one("ribbon.post",string="Post")
    joining=fields.Date("Joining Date")
    bcs=fields.Boolean("BCS ?")
    retired=fields.Date("Retiered Date")
    service_year=fields.Integer("Service Year")
    service_month=fields.Integer("Service Month")
    service_day=fields.Integer("Service Day")
    service_length=fields.Char("Service Length",compute="calculate_service_length")
    cap=fields.Char("Cap")
    belt=fields.Char("Belt")
    name_tag_eng=fields.Char("Name Tag")
    name_tag_bn=fields.Char("নাম ফলক")
    note=fields.Char("note")
    conf_note=fields.Char("confidential")
    freedom_f=fields.Boolean("Freedom Fighter")
    nirapotta=fields.Boolean("Nirapotta")
    bpa=fields.Boolean("Police Academy")
    psc=fields.Boolean("Staff College")
    rab=fields.Boolean("RAB")
    missions=fields.One2many("ribbon.personal.mission",'partner_id')
    services=fields.One2many("ribbon.personal.service",'partner_id')
    awards=fields.One2many("ribbon.personal.award",'partner_id')

    custom_acquired_ribbons = fields.Many2many("ribbon.customs.acquired.ribbon")

    acquired_ribbons = fields.Many2many("ribbon.acquired.ribbon")
    ribbon_set_image = fields.Html("Ribbons Immage", compute="getRibonImage")
    ribbon_point_size = fields.Integer("Point Size", default='15')
    ribbon_point_unit = fields.Selection(string='Unit', selection=[
            ('vw', 'Screen Width (vw)'),
            ('vh', 'Screen Height(vh)'),
            ('px', 'Point (px)'), ],
             help='You can set here the size depends on screen.', default='px')
    #Start
    def get_partners_service_ribbons(self,partner_id):
        partner=self.env['res.partner'].search([('id','=',partner_id)])
        if partner.retired:
            ribbon_for_age = self.env["ribbon.regulation"].search([('force_id', '=', partner.force_id.id),
                                                                   ('acquisition.id', '=', "1"),
                                                                   ('service_length', '<=',
                                                                    partner.service_year),
                                                                   ("shedule_date", "<=", partner.retired)])
        else:
            ribbon_for_age = partner.env["ribbon.regulation"].search([('force_id', '=', partner.force_id.id),
                                                                   ('acquisition.id', '=', "1"),
                                                                   ('service_length', '<=',self.service_year)])
        return ribbon_for_age

    def get_partners_awards_ribbons(self,partner_id):
        partner=self.env['res.partner'].search([('id','=',partner_id)])
        ribbon_for_awards = self.env["ribbon.personal.award"].search([("partner_id", "=", partner_id)])
        return ribbon_for_awards

    def get_partners_mission_ribbons(self,partner_id):
        ribbon_for_mission = self.env["ribbon.personal.mission"].search(
            [("partner_id", "=", partner_id)])
        return ribbon_for_mission

    def get_partners_in_service_ribbons(self,partner_id):
        partner = self.env['res.partner'].search([('id', '=', partner_id)])
        if partner.retired:
            in_service_ribbons = self.env["ribbon.regulation"].search([('force_id', '=', partner.force_id.id),
                                                                   ('acquisition.name', '=', "In-service"),
                                                                   ('shedule_date', '>=',partner.joining), ('shedule_date', '<=',partner.retired)])
        else:
            in_service_ribbons = self.env["ribbon.regulation"].search([('force_id', '=', partner.force_id.id),
                                                                       ('acquisition.name', '=', "In-service"),
                                                                       ('shedule_date', '>=', partner.joining)])

        return in_service_ribbons

    @api.onchange('missions', 'services', 'awards')
    def get_acquired_ribbons(self):
        acq_ribbons=self.env['ribbon.acquired.ribbon'].search([('partner_id','=',self.id)])
        for rec in acq_ribbons:
            rec.unlink()
        if self.retired:
            ribbon_for_age = self.env["ribbon.regulation"].search([('force_id', '=', self.force_id.id),
                                                                   ('acquisition.name', '=', "Service Age"),
                                                                   ('service_length', '<=',
                                                                    self.service_year),
                                                                   ("shedule_date", "<=", self.retired)])
        else:
            ribbon_for_age = self.env["ribbon.regulation"].search([('force_id', '=', self.force_id.id),
                                                                   ('acquisition.name', '=', "Service Age"),
                                                                   ('service_length', '<=',
                                                                    self.service_year),
                                                                   ])
#         # todo here to apply search for shedule_date between joining date and Retired date
#         data = []
#         for rec in ribbon_for_age:
#             input = self.env["ribbon.acquired.ribbon"].create({
#                 'partner_id': self.id,
#                 'ribbon_id': rec.id,
#                 'extension': 1,
#                 'serial': rec.serial})
#             data.append(input.id)
#         self.acquired_ribbons = [(6, 0, data)]
#         ribbon_for_awards = self.env["ribbon.personal.award"].search([("partner_id", "=", self.id)])
#         for rec in ribbon_for_awards:
#             input = self.env["ribbon.acquired.ribbon"].create({
#                 'partner_id': self.id,
#                 'ribbon_id': rec.ribbon_id.id,
#                 'extension': rec.extension.id,
#                 'serial': rec.ribbon_id.serial})
#             self.acquired_ribbons = [(4, input.id)]
#         ribbon_for_missions = self.env["ribbon.personal.mission"].search(
#             [("partner_id", "=", self.id)])
#         for rec in ribbon_for_missions:
#             input = self.env["ribbon.acquired.ribbon"].create({
#                 'partner_id': self.id,
#                 'ribbon_id': rec.ribbon_id.id,
#                 'extension': rec.extension.id,
#                 'serial': rec.ribbon_id.serial})
#             self.acquired_ribbons = [(4, input.id)]
#
#     @api.onchange('ribbon_point_size', 'ribbon_point_unit', 'acquired_ribbons')
    def getRibonImage(self):
        # print("in service Ribbon= " )
        # print(self.get_partners_in_service_ribbons(self.id))

        point_unit = self.ribbon_point_unit
        pointsize = self.ribbon_point_size
        point_length = 6 * pointsize
        point_height = 2 * pointsize
        total_ribbon_point = len(self.acquired_ribbons)
        total_row = total_ribbon_point // 4
        ribbon_point_remainder = total_ribbon_point
        first_row_point = total_ribbon_point % 4
        row_point = 4
        row_no = 1
        position_left = 0
        position_height = 0
        first_point = 1
        image_set = '<div style = "width:100%; height=6' + point_unit + ';position:relative;  top:' + str(
            (row_no - 1) * point_height) + point_unit + ';  " >' + chr(10)
        if first_row_point > 0:
            total_row = total_row + 1
        acq_ribons=self.env['ribbon.acquired.ribbon'].search([('partner_id','=',self._origin.id)],order='serial')
        acq_ribbons = self.acquired_ribbons._origin
        acq_ribbons = acq_ribbons.sorted(key=lambda r: r.serial)
        for rec in acq_ribons:
            if first_point == 1:
                # start div for the row if this is the first point of the row
                image_set = image_set + '<div style = "width:100%; height=6' + point_unit + ';position:absolute;  top:' + str(
                    (row_no - 1) * point_height) + point_unit + ';  " >' + chr(10)
                if row_no == 1:
                    if first_row_point > 0:
                        position_left = point_length * (4 - first_row_point) / 2
                        row_point = first_row_point
            image_set = image_set + '<img style=" position:absolute;  left: ' + str(
                position_left) + point_unit + ';   width:' + str(point_length) + point_unit + ';' \
                        + 'height:' + str(
                point_height) + point_unit + ';  border: 1px solid blue;z-index: 1;" src="../web/image/ribbon.extension/' + str(
                rec.extension.id) + '/image"/>' + chr(10)
            # here to impliment extension rule if extension exist!

            image_set = image_set + '<img style=" position:absolute;  left: ' + str(
                position_left) + point_unit + ';   width:' + str(point_length) + point_unit + ';' \
                        + 'height:' + str(
                point_height) + point_unit + ';  border: 1px solid blue;z-index: 0;" src="../web/image/product.template/' + str(
                rec.ribbon_id.ribbon_tmpl_id.id) + '/image_1920"/>' + chr(10)
            row_point = row_point - 1
            first_point = 0
            position_left = position_left + point_length
            if row_point == 0:
                row_point = 4
                first_point = 1
                row_no = row_no + 1
                position_left = 0
                image_set = image_set + '</div>' + chr(10)
        image_set = image_set + '</div>'
        self.ribbon_set_image = image_set
    # End
    @api.onchange('joining',"retired")
    def calculate_service_length(self):
        currentDate=datetime.datetime.now()
        for rec in self:
            if rec.joining:
                if rec.retired:
                    curYear=rec.retired.year
                    curMonth=rec.retired.month
                    curDay=rec.retired.day
                else:
                    curYear = currentDate.year
                    curMonth = currentDate.month
                    curDay = currentDate.day

                lyear=rec.joining.year
                lmonth=rec.joining.month
                lday=rec.joining.day
                lday=curDay-lday
                lmonth=curMonth-lmonth
                lyear=curYear-lyear
                length_string=""
                if lday<0:
                    lday=lday+30
                    lmonth=lmonth-1
                if lmonth<0:
                    lmonth=lmonth+12
                    lyear=lyear-1
                if lyear>0:
                    length_string=length_string+ str(lyear) +" Year "
                if lmonth>0:
                    length_string=length_string+ str(lmonth) + " Month "
                if lday>0:
                    length_string=length_string+ str(lday) + " Day "
                rec.service_length=length_string
                rec.service_year=lyear
                rec.service_month=lmonth
                rec.service_day=lday
            else:
                rec.service_length = ""
                rec.service_year = 0
                rec.service_month =0
                rec.service_day = 0

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        self = self.with_user(name_get_uid or self.env.uid)
        # as the implementation is in SQL, we force the recompute of fields if necessary
        self.recompute(['display_name'])
        self.flush()
        if args is None:
            args = []
        order_by_rank = self.env.context.get('res_partner_search_mode')
        if (name or order_by_rank) and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            from_str = from_clause if from_clause else 'res_partner'
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

            fields = self._get_name_search_order_by_fields()

            query = """SELECT res_partner.id
                         FROM {from_str}
                      {where} ({email} {operator} {percent}
                           OR {display_name} {operator} {percent}
                           OR {mobile} {operator} {percent}
                           OR {phone} {operator} {percent}
                           OR {id_no} {operator} {percent}
                           OR {reference} {operator} {percent}
                           OR {vat} {operator} {percent})
                           -- don't panic, trust postgres bitmap
                     ORDER BY {fields} {display_name} {operator} {percent} desc,
                              {display_name}
                    """.format(from_str=from_str,
                               fields=fields,
                               where=where_str,
                               operator=operator,
                               email=unaccent('res_partner.email'),
                               display_name=unaccent('res_partner.display_name'),
                               mobile=unaccent('res_partner.mobile'),
                               phone=unaccent('res_partner.phone'),
                               id_no=unaccent('res_partner.id_no'),
                               reference=unaccent('res_partner.ref'),
                               percent=unaccent('%s'),
                               vat=unaccent('res_partner.vat'),)

            where_clause_params += [search_name]*6  # for email / display_name, reference/phone/mobile/id_no
            where_clause_params += [re.sub('[^a-zA-Z0-9]+', '', search_name) or None]  # for vat
            where_clause_params += [search_name]  # for order by
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            self.env.cr.execute(query, where_clause_params)
            return [row[0] for row in self.env.cr.fetchall()]

        return super(PersonalDetails, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)
#
class ribbonMedalAcquiredRibbon(models.Model):
    _name="ribbon.acquired.ribbon"
    _description = "list of acquired rebbon"
    _order = "serial"
    partner_id = fields.Many2one("res.partner")
    force_member_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.regulation")
    image = fields.Binary(
        "Image", related="ribbon_id.ribbon_tmpl_id.image_1920")
    extension = fields.Many2one("ribbon.extension")
    serial = fields.Integer("Serial")
class ribbonCustomAcquiredRibbon(models.Model):
    _name="ribbon.customs.acquired.ribbon"
    _description = "list of customs acquired rebbon"
    _order = "serial"
    partner_id = fields.Many2one("res.partner")
    force_member_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.regulation")
    image = fields.Binary(
        "Image", related="ribbon_id.ribbon_tmpl_id.image_1920")
    extension = fields.Many2one("ribbon.extension")
    serial = fields.Integer("Serial")
class RibbonMedalPersonalacquisition(models.Model):
    _name="ribbon.personal.acquisition"
    _description="list of Personal Acquisition"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.regulation")
    extension = fields.Many2one("ribbon.extension")
    serial = fields.Integer("serial")
class RibbonMedalPersonalAward(models.Model):
    _name="ribbon.personal.award"
    _description="list of Personal Award"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.regulation")
    extension = fields.Many2one("ribbon.extension")
    serial = fields.Integer("serial")
class RibbonMedalPersonalMission(models.Model):
    _name="ribbon.personal.mission"
    _description="list of Personal Mission"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.regulation")
    extension = fields.Many2one("ribbon.extension")
    serial = fields.Integer("serial")
class RibbonMedalPersonalservice(models.Model):
    _name="ribbon.personal.service"
    _description="list of Personal service"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.regulation")
    extension = fields.Many2one("ribbon.extension")
    serial = fields.Integer("serial")
