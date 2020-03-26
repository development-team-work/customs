# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime

class PersonalDetails(models.Model):
    _inherit = 'res.partner'
    _description = "force member's personal Details for ribbon_bk, medal, cap, belt, ranks etc"
    is_force=fields.Boolean("Is a Force",default=False , translate=True)
    force_id = fields.Many2one("ribbon_bk.force","Force")
    id_no=fields.Char("ID No")
    rank = fields.Many2one("ribbon_bk.rank","Rank",translate=True)
    unit=fields.Many2one("ribbon_bk.force.unit",string="Unit",translate=True ,domain="[('force_name','=',force_id)]")
    post=fields.Many2one("ribbon_bk.post",string="Post",translate=True)
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
    missions=fields.One2many("ribbon_bk.personal.mission",'partner_id')
    services=fields.One2many("ribbon_bk.personal.service",'partner_id')
    awards=fields.One2many("ribbon_bk.personal.award",'partner_id')

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

class RibbonMedalPersonalacquisition(models.Model):
    _name="ribbon_bk.personal.acquisition"
    _description="list of Personal Acquisition"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon_bk.regulation")
    extension = fields.Many2one("ribbon_bk.extension")
    serial = fields.Integer("serial")
class RibbonMedalPersonalAward(models.Model):
    _name="ribbon_bk.personal.award"
    _description="list of Personal Award"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon_bk.regulation")
    extension = fields.Many2one("ribbon_bk.extension")
    serial = fields.Integer("serial")
class RibbonMedalPersonalMission(models.Model):
    _name="ribbon_bk.personal.mission"
    _description="list of Personal Mission"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon_bk.regulation")
    extension = fields.Many2one("ribbon_bk.extension")
    serial = fields.Integer("serial")
class RibbonMedalPersonalservice(models.Model):
    _name="ribbon_bk.personal.service"
    _description="list of Personal service"
    partner_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon_bk.regulation")
    extension = fields.Many2one("ribbon_bk.extension")
    serial = fields.Integer("serial")