from eagle import api, fields, models, _
import datetime


class RibbonMedalAcquisitionWizard(models.TransientModel):
    _name ='ribbon.acquisition.wizard'
    _description='Get acquired ribbons and medals by a force Member'
    ribbon_holder=fields.Many2one('res.partner',"Person")
    force_id=fields.Many2one("ribbon.force","Force Name",related="ribbon_holder.force_id")
    id_no=fields.Char("ID No",related="ribbon_holder.id_no")
    rank=fields.Many2one("ribbon.rank","Rank",related="ribbon_holder.rank")
    unit=fields.Many2one("ribbon.force.unit","Unit",related="ribbon_holder.unit")
    post=fields.Many2one("ribbon.post","Post",related="ribbon_holder.post")
    joining=fields.Date("Joining Date",related="ribbon_holder.joining")
    bcs=fields.Boolean("BCS ?",related="ribbon_holder.bcs")
    retired=fields.Date("Retired Date?",related="ribbon_holder.retired")
    service_length=fields.Char("Service Length",related="ribbon_holder.service_length")
    services=fields.Many2one("ribbon.personal.service")
    awards=fields.Many2many("ribbon.personal.award")
    missions=fields.Many2many("ribbon.personal.mission")
    acquired_ribbons=fields.Many2many("ribbon.acquired.ribbon.wizard","party_acquired_rel")
    ribbon_set_image=fields.Html("Ribbons Immage",compute="getRibonImage")
    ribbon_point_size=fields.Integer("Point Size",default='15')
    ribbon_point_unit=fields.Selection(string='Unit', selection=[
            ('vw', 'Screen Width (vw)'),
            ('vh', 'Screen Height(vh)'),
            ('px', 'Point (px)'),],
        help='You can set here the size depends on screen.',default='px')

    @api.onchange('ribbon_holder')
    def get_acquired_ribbons(self):
        if self.ribbon_holder.retired:
            ribbon_for_age=self.env["ribbon.regulation"].search([('force_id', '=', self.force_id.id),
                                                                         ('acquisition.name', '=', "Service Age"),
                                                                         ('service_length', '<=',self.ribbon_holder.service_year),("shedule_date","<=",self.ribbon_holder.retired)])
        else:
            ribbon_for_age = self.env["ribbon.regulation"].search([('force_id', '=', self.force_id.id),
                                                                         ('acquisition.name', '=', "Service Age"),
                                                                         ('service_length', '<=',
                                                                          self.ribbon_holder.service_year),
                                                                         ])
        #todo here to apply search for shedule_date between joining date and Retired date
        data=[]
        for rec in ribbon_for_age:
            input=self.env["ribbon.acquired.ribbon.wizard"].create({
            'force_member_id': self.ribbon_holder.id,
            'ribbon_id': rec.id,
            'extension': 1,
            'serial': rec.serial})
            data.append(input.id)
        self.acquired_ribbons=[(6,0,data)]
        ribbon_for_awards=self.env["ribbon.personal.award"].search([("partner_id","=",self.ribbon_holder.id)])
        for rec in ribbon_for_awards:
            input=self.env["ribbon.acquired.ribbon.wizard"].create({
                'force_member_id': self.ribbon_holder.id,
                'ribbon_id': rec.ribbon_id.id,
                'extension': rec.extension.id,
                'serial': rec.ribbon_id.serial})
            self.acquired_ribbons=[(4,input.id)]
        ribbon_for_missions = self.env["ribbon.personal.mission"].search(
            [("partner_id", "=", self.ribbon_holder.id)])
        for rec in ribbon_for_missions:
            input = self.env["ribbon.acquired.ribbon.wizard"].create({
                'force_member_id': self.ribbon_holder.id,
                'ribbon_id': rec.ribbon_id.id,
                'extension': rec.extension.id,
                'serial': rec.ribbon_id.serial})
            self.acquired_ribbons = [(4, input.id)]
    @api.onchange('ribbon_point_size','ribbon_point_unit','acquired_ribbons')
    def getRibonImage(self):
        point_unit=self.ribbon_point_unit
        pointsize=self.ribbon_point_size
        point_length=6*pointsize
        point_height=2*pointsize
        total_ribbon_point = len(self.acquired_ribbons)
        total_row=total_ribbon_point//4
        ribbon_point_remainder = total_ribbon_point
        first_row_point= total_ribbon_point % 4
        row_point=4
        row_no=1
        position_left=0
        position_height=0
        first_point=1
        image_set = '<div style = "width:100%; height=6'+ point_unit +';position:relative;  top:'+str((row_no-1)*point_height)+ point_unit +';  " >'+chr(10)
        if first_row_point>0:
            total_row=total_row+1

        for rec in self.acquired_ribbons:
            if first_point==1:
                # start div for the row if this is the first point of the row
                image_set=image_set +'<div style = "width:100%; height=6'+ point_unit +';position:absolute;  top:'+str((row_no-1)*point_height)+ point_unit +';  " >'+chr(10)
                if row_no==1:
                    if first_row_point>0:
                        position_left=point_length*(4-first_row_point)/2
                        row_point = first_row_point
            image_set = image_set + '<img style=" position:absolute;  left: '+str(position_left)+point_unit+';   width:'+str(point_length)+point_unit+';'\
                        + 'height:'+ str(point_height)+point_unit+';  border: 1px solid blue;z-index: 1;" src="../web/image/ribbon.extension/'+str(rec.extension.id)+'/image"/>'+chr(10)
            #here to impliment extension rule if extension exist!

            image_set=image_set+'<img style=" position:absolute;  left: '+str(position_left)+point_unit+';   width:'+str(point_length)+point_unit+';'\
                      + 'height:'+ str(point_height)+point_unit+';  border: 1px solid blue;z-index: 0;" src="../web/image/product.product/'+str(rec.ribbon_id.big_ribbon.id)+'/image"/>'+chr(10)
            row_point = row_point-1
            first_point = 0
            position_left = position_left+point_length
            if row_point==0:
                row_point = 4
                first_point = 1
                row_no = row_no+1
                position_left=0
                image_set=image_set+'</div>'+chr(10)
        image_set = image_set + '</div>'
        self.ribbon_set_image=image_set

class ribbonMedalAcquiredRibbonWizard(models.TransientModel):
    _name="ribbon.acquired.ribbon.wizard"
    _description = "list of acquired rebbon"
    _order = "serial desc"
    force_member_id = fields.Many2one("res.partner")
    ribbon_id = fields.Many2one("ribbon.regulation")
    image = fields.Binary(
        "Image", related="ribbon_id.big_ribbon.image")
    extension = fields.Many2one("ribbon.extension")
    serial = fields.Integer("serial")

class ribbonMedalquotation(models.TransientModel):
    _name="ribbon.quotation"
    force_member_id = fields.Many2one("res.partner")
    curiar_address = fields.Char('Address')
    curiar_Contact = fields.Char('Mobile')
    delivery_date = fields.Date('Delivery Date')
    ribbon_qty=fields.Integer("Ribbon Qty")
    pin_qty=fields.Integer("Safety Pin")
    vel_qty=fields.Integer("Velcro")
    ribbon_details=fields.One2many("ribbon.ribbon.quotation.details",'quotation_id')
    ribbon_price_per_set=fields.Float('price/set',compute="get_ribbon_per_set_price")
    ribbon_refund_price=fields.Float('Refund')
    ribbon_net_price=fields.Float('price')

    bmedal_qty=fields.Integer("Tunic Medal Qty")
    bmedal_details=fields.One2many("ribbon.ribbon.quotation.details",'quotation_id')
    bmedal_price_per_set=fields.Float('price/set',compute="get_bmedal_per_set_price")
    bmedal_refund_price=fields.Float('Refund')
    bmedal_net_price=fields.Float('price')

    smedal_qty=fields.Integer("Meskit Medal Qty")
    smedal_details = fields.One2many("ribbon.ribbon.quotation.details", 'quotation_id')
    smedal_price_per_set = fields.Float('price/set', compute="get_smedal_per_set_price")
    smedal_refund_price = fields.Float('Refund')
    smedal_net_price = fields.Float('price')

    @api.onchange("ribbon_qty")
    @api.multi
    def get_ribbon_per_set_price(self):
        set_price=0
        refund=0
        for rec in self.ribbon_details:
            set_price=set_price+rec.rate+rec.making
            refund=refund+(rec.rate*rec.ref_qty)
        self.ribbon_price_per_set=set_price
        self.ribbon_refund_price=refund
        self.ribbon_net_price=(self.ribbon_qty*set_price)-refund

    @api.onchange("bmedal_qty")
    @api.multi
    def get_bmedal_per_set_price(self):
        set_price=0
        refund=0
        for rec in self.bmedal_details:
            set_price=set_price+rec.rate+rec.making
            refund=refund+(rec.rate*rec.ref_qty)
        self.bmedal_price_per_set=set_price
        self.bmedal_refund_price=refund
        self.bmedal_net_price=(self.bmedal_qty*set_price)-refund

    @api.onchange("smedal_qty")
    @api.multi
    def get_smedal_per_set_price(self):
        set_price=0
        refund=0
        for rec in self.smedal_details:
            set_price=set_price+rec.rate+rec.making
            refund=refund+(rec.rate*rec.ref_qty)
        self.smedal_price_per_set=set_price
        self.smedal_refund_price=refund
        self.smedal_net_price=(self.smedal_qty*set_price)-refund

class  ribbonMedalribbonQuotationDetails(models.TransientModel):
    _name= "ribbon.ribbon.quotation.details"
    quotation_id=fields.Many2one('ribbon.quotation')
    product_id=fields.Many2one("product.product")
    req_qty=fields.Integer("Required",related="quotation_id.ribbon_qty")
    ref_qty= fields.Integer("Ref. Qty",help="Qty supplied by the customer")
    sale_qty=fields.Integer("Sale Qty",help="Qty sale to the customer")
    rate=fields.Float("rate")
    making=fields.Float("making")

class  ribbonMedalTunicMedalQuotationDetails(models.TransientModel):
    _name= "ribbon.bmedal.quotation.details"
    quotation_id=fields.Many2one('ribbon.quotation')
    product_id=fields.Many2one("product.product")
    req_qty=fields.Integer("Required",related="quotation_id.bmedal_qty")
    ref_qty= fields.Integer("Ref. Qty",help="Qty supplied by the customer")
    sale_qty=fields.Integer("Sale Qty",help="Qty sale to the customer")
    rate=fields.Float("rate")
    making=fields.Float("making")

class  ribbonMedalMeskitMedalQuotationDetails(models.TransientModel):
    _name= "ribbon.smedal.quotation.details"
    quotation_id=fields.Many2one('ribbon.quotation')
    product_id=fields.Many2one("product.product")
    req_qty=fields.Integer("Required",related="quotation_id.smedal_qty")
    ref_qty= fields.Integer("Ref. Qty",help="Qty supplied by the customer")
    sale_qty=fields.Integer("Sale Qty",help="Qty sale to the customer")
    rate=fields.Float("rate")
    making=fields.Float("making")

