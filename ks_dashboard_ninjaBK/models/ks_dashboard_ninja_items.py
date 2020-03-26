# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
from datetime import datetime
from ..lib.ks_date_filter_selections import ks_get_date


class KsDashboardNinjaItems(models.Model):
    _name = 'ks_dashboard_ninja.item'

    name = fields.Char(string="Name", size=256)
    ks_model_id = fields.Many2one('ir.model', string='Model', required=True,
                                  domain="[('access_ids','!=',False),('transient','=',False),('model','not ilike','base_import%'),('model','not ilike','ir.%'),('model','not ilike','web_editor.%'),('model','not ilike','web_tour.%'),('model','!=','mail.thread'),('model','not ilike','ks_dash%')]")
    ks_domain = fields.Char(string="Domain")

    ks_model_id_2 = fields.Many2one('ir.model', string='Model',
                                    domain="[('access_ids','!=',False),('transient','=',False),('model','not ilike','base_import%'),('model','not ilike','ir.%'),('model','not ilike','web_editor.%'),('model','not ilike','web_tour.%'),('model','!=','mail.thread'),('model','not ilike','ks_dash%')]")

    ks_model_name_2 = fields.Char(related='ks_model_id_2.model')

    # This field main purpose is to store %UID as current user id. Mainly used in JS file as container.
    ks_domain_temp = fields.Char(string="Domain Substitute")
    ks_background_color = fields.Char(string="Background Color",
                                      default="#ffffff,0.99")
    ks_icon = fields.Binary(string="Icon", attachment=True)
    ks_default_icon = fields.Char(string="Icon", default="bar-chart")
    ks_default_icon_color = fields.Char(default="#ffffff,0.99", string="Icon Color")
    ks_icon_select = fields.Char(string="Icon Option", default="Default")
    ks_font_color = fields.Char(default="#ffffff,0.99", string="Font Color")
    ks_dashboard_item_theme = fields.Char(string="Theme", default="white")
    ks_layout = fields.Selection([('layout1', 'Layout 1'),
                                  ('layout2', 'Layout 2'),
                                  ('layout3', 'Layout 3'),
                                  ('layout4', 'Layout 4'),
                                  ('layout5', 'Layout 5'),
                                  ('layout6', 'Layout 6'),
                                  ], default=('layout1'), required=True, string="Layout")
    ks_preview = fields.Integer(default=1, string="Preview")
    ks_model_name = fields.Char(related='ks_model_id.model')

    ks_record_count_type_2 = fields.Selection([('count', 'Count'),
                                               ('sum', 'Sum'),
                                               ('average', 'Average')], string="Record Type", default="sum")
    ks_record_field_2 = fields.Many2one('ir.model.fields',
                                        domain="[('model_id','=',ks_model_id_2),('name','!=','id'),'|','|',('ttype','=','integer'),('ttype','=','float'),('ttype','=','monetary')]",
                                        string="Record Field")
    ks_record_count_type = fields.Selection([('count', 'Count'),
                                             ('sum', 'Sum'),
                                             ('average', 'Average')], string="Record Type", default="count")
    ks_record_count = fields.Float(string="Record Count", compute='ks_get_record_count', readonly=True)
    ks_record_field = fields.Many2one('ir.model.fields',
                                      domain="[('model_id','=',ks_model_id),('name','!=','id'),'|','|',('ttype','=','integer'),('ttype','=','float'),('ttype','=','monetary')]",
                                      string="Record Field")

    # Date Filter Fields
    # Condition to tell if date filter is applied or not
    ks_isDateFilterApplied = fields.Boolean(default=False)

    # ---------------------------- Date Filter Fields ------------------------------------------
    ks_date_filter_field = fields.Many2one('ir.model.fields',
                                           domain="[('model_id','=',ks_model_id),'|',('ttype','=','date'),('ttype','=','datetime')]",
                                           string="Date Filter Field")
    ks_date_filter_selection = fields.Selection([
        ('l_none', 'None'),
        ('l_day', 'Today'),
        ('t_week', 'This Week'),
        ('t_month', 'This Month'),
        ('t_quarter', 'This Quarter'),
        ('t_year', 'This Year'),
        ('ls_day', 'Last Day'),
        ('ls_week', 'Last Week'),
        ('ls_month', 'Last Month'),
        ('ls_quarter', 'Last Quarter'),
        ('ls_year', 'Last Year'),
        ('l_week', 'Last 7 days'),
        ('l_month', 'Last 30 days'),
        ('l_quarter', 'Last 90 days'),
        ('l_year', 'Last 365 days'),
        ('l_custom', 'Custom Filter'),
    ], string="Date Filter Selection", default="l_none", required=True)

    ks_item_start_date = fields.Datetime(string="Start Date")
    ks_item_end_date = fields.Datetime(string="End Date")

    ks_date_filter_field_2 = fields.Many2one('ir.model.fields',
                                             domain="[('model_id','=',ks_model_id_2),'|',('ttype','=','date'),('ttype','=','datetime')]",
                                             string="Date Filter Field")

    ks_item_start_date_2 = fields.Datetime(string="Start Date")
    ks_item_end_date_2 = fields.Datetime(string="End Date")

    ks_domain_2 = fields.Char(string="Domain")

    ks_date_filter_selection_2 = fields.Selection([
        ('l_none', "None"),
        ('l_day', 'Today'),
        ('t_week', 'This Week'),
        ('t_month', 'This Month'),
        ('t_quarter', 'This Quarter'),
        ('t_year', 'This Year'),
        ('ls_day', 'Last Day'),
        ('ls_week', 'Last Week'),
        ('ls_month', 'Last Month'),
        ('ls_quarter', 'Last Quarter'),
        ('ls_year', 'Last Year'),
        ('l_week', 'Last 7 days'),
        ('l_month', 'Last 30 days'),
        ('l_quarter', 'Last 90 days'),
        ('l_year', 'Last 365 days'),
        ('l_custom', 'Custom Filter'),
    ], string="Date Filter Selection", required=True, default='l_none')

    ks_previous_period = fields.Boolean(string="Previous Period")

    # ------------------------ Pro Fields --------------------
    ks_dashboard_ninja_board_id = fields.Many2one('ks_dashboard_ninja.board',
                                                  default=lambda self: self._context[
                                                      'ks_dashboard_id'] if 'ks_dashboard_id' in self._context else False)

    # Chart related fields
    ks_dashboard_item_type = fields.Selection([('ks_tile', 'Tile'),
                                               ('ks_bar_chart', 'Bar Chart'),
                                               ('ks_horizontalBar_chart', 'Horizontal Bar Chart'),
                                               ('ks_line_chart', 'Line Chart'),
                                               ('ks_area_chart', 'Area Chart'),
                                               ('ks_pie_chart', 'Pie Chart'),
                                               ('ks_doughnut_chart', 'Doughnut Chart'),
                                               ('ks_polarArea_chart', 'Polar Area Chart'),
                                               ('ks_list_view', 'List View'),
                                               ('ks_kpi', 'KPI')
                                               ], default=lambda self: self._context.get('ks_dashboard_item_type',
                                                                                         'ks_tile'), required=True,
                                              string="Dashboard Item Type")
    ks_chart_groupby_type = fields.Char(compute='get_chart_groupby_type')
    ks_chart_sub_groupby_type = fields.Char(compute='get_chart_sub_groupby_type')
    ks_chart_relation_groupby = fields.Many2one('ir.model.fields',
                                                domain="[('model_id','=',ks_model_id),('name','!=','id'),('store','=',True),'|',"
                                                       "'|','|',('ttype','=','many2one'),('ttype','=','selection'),('ttype','=','date'),('ttype','=','datetime')]",
                                                string="Group By")
    ks_chart_relation_sub_groupby = fields.Many2one('ir.model.fields',
                                                    domain="[('model_id','=',ks_model_id),('name','!=','id'),('store','=',True),'|',"
                                                           "'|','|',('ttype','=','many2one'),('ttype','=','selection'),('ttype','=','date'),('ttype','=','datetime')]",
                                                    string=" Sub Group By")
    ks_chart_date_groupby = fields.Selection([('day', 'Day'),
                                              ('week', 'Week'),
                                              ('month', 'Month'),
                                              ('quarter', 'Quarter'),
                                              ('year', 'Year'),
                                              ], string="Dashboard Item Chart Group By Type")
    ks_chart_date_sub_groupby = fields.Selection([('day', 'Day'),
                                                  ('week', 'Week'),
                                                  ('month', 'Month'),
                                                  ('quarter', 'Quarter'),
                                                  ('year', 'Year'),
                                                  ], string="Dashboard Item Chart Sub Group By Type")
    ks_graph_preview = fields.Char(string="Preview", default="Graph Preview")
    ks_chart_data = fields.Char(string="Chart Data in string form", compute='ks_get_chart_data')
    ks_chart_data_count_type = fields.Selection([('count', 'Count'), ('sum', 'Sum'), ('average', 'Average')],
                                                string="Data Type", default="sum")
    ks_chart_measure_field = fields.Many2many('ir.model.fields', 'ks_dn_measure_field_rel', 'measure_field_id',
                                              'field_id',
                                              domain="[('model_id','=',ks_model_id),('name','!=','id'),('store','=',True),'|','|',"
                                                     "('ttype','=','integer'),('ttype','=','float'),"
                                                     "('ttype','=','monetary')]",
                                              string="Measure 1")

    ks_chart_measure_field_2 = fields.Many2many('ir.model.fields', 'ks_dn_measure_field_rel_2', 'measure_field_id_2',
                                                'field_id',
                                                domain="[('model_id','=',ks_model_id),('name','!=','id'),('store','=',True),'|','|',"
                                                       "('ttype','=','integer'),('ttype','=','float'),"
                                                       "('ttype','=','monetary')]",
                                                string="Line Measure")

    ks_bar_chart_stacked = fields.Boolean(string="Stacked Bar Chart")

    ks_semi_circle_chart = fields.Boolean(string="Semi Circle Chart")

    ks_sort_by_field = fields.Many2one('ir.model.fields',
                                       domain="[('model_id','=',ks_model_id),('name','!=','id'),('store','=',True),"
                                              "('ttype','!=','one2many'),('ttype','!=','many2one'),('ttype','!=','binary')]",
                                       string="Sort By Field")
    ks_sort_by_order = fields.Selection([('ASC', 'Ascending'), ('DESC', 'Descending')],
                                        string="Sort Order")
    ks_record_data_limit = fields.Integer(string="Record Limit")

    ks_list_view_preview = fields.Char(string="List View Preview", default="List View Preview")

    ks_kpi_preview = fields.Char(string="Preview", default="KPI Preview")

    ks_kpi_type = fields.Selection([
        ('layout_1', 'KPI With Target'),
        ('layout_2', 'Data Comparison'),
    ], string="Layout", default="layout_1")

    ks_target_view = fields.Char(string="View", default="Number")

    ks_data_comparison = fields.Char(string="Data Type", default="None")

    ks_kpi_data = fields.Char(string="KPI Data", compute="ks_get_kpi_data")

    ks_chart_item_color = fields.Selection(
        [('default', 'Default'), ('cool', 'Cool'), ('warm', 'Warm'), ('neon', 'Neon')],
        string="Chart Color Palette", default="default")

    # ------------------------ List View Fields ------------------------------

    ks_list_view_type = fields.Selection([('ungrouped', 'Un-Grouped'), ('grouped', 'Grouped')], default="ungrouped",
                                         string="List View Type", required=True)
    ks_list_view_fields = fields.Many2many('ir.model.fields', 'ks_dn_list_field_rel', 'list_field_id', 'field_id',
                                           domain="[('model_id','=',ks_model_id),('store','=',True),"
                                                  "('ttype','!=','one2many'),('ttype','!=','many2many'),('ttype','!=','binary')]",
                                           string="Fields to show in list")

    ks_list_view_group_fields = fields.Many2many('ir.model.fields', 'ks_dn_list_group_field_rel', 'list_field_id',
                                                 'field_id',
                                                 domain="[('model_id','=',ks_model_id),('name','!=','id'),('store','=',True),'|','|',"
                                                        "('ttype','=','integer'),('ttype','=','float'),"
                                                        "('ttype','=','monetary')]",
                                                 string="List View Grouped Fields")

    ks_list_view_data = fields.Char(string="List View Data in JSon", compute='ks_get_list_view_data')

    # -------------------- Multi Company Feature ---------------------
    ks_company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)

    # -------------------- Target Company Feature ---------------------
    ks_goal_enable = fields.Boolean(string="Enable Target")
    ks_goal_bar_line = fields.Boolean(string="Show Target As Line")
    ks_standard_goal_value = fields.Float(string="Standard Target")
    ks_goal_lines = fields.One2many('ks_dashboard_ninja.item_goal', 'ks_dashboard_item', string="Target Lines")


    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            if not name:
                name = rec.ks_model_id.name
            res.append((rec.id, name))

        return res

    @api.onchange('ks_layout')
    def layout_four_font_change(self):
        if self.ks_layout == 'layout4':
            self.ks_font_color = self.ks_background_color
            self.ks_default_icon_color = "#ffffff,0.99"
        elif self.ks_layout == 'layout6':
            self.ks_font_color = "#ffffff,0.99"
            self.ks_default_icon_color = self.ks_get_dark_color(self.ks_background_color.split(',')[0],
                                                                self.ks_background_color.split(',')[1])
        else:
            self.ks_default_icon_color = "#ffffff,0.99"
            self.ks_font_color = "#ffffff,0.99"

    # To convert color into 10% darker. Percentage amount is hardcoded. Change amt if want to change percentage.
    def ks_get_dark_color(self, color, opacity):
        num = int(color[1:], 16)
        amt = -25
        R = (num >> 16) + amt
        R = (255 if R > 255 else 0 if R < 0 else R) * 0x10000
        G = (num >> 8 & 0x00FF) + amt
        G = (255 if G > 255 else 0 if G < 0 else G) * 0x100
        B = (num & 0x0000FF) + amt
        B = (255 if B > 255 else 0 if B < 0 else B)
        return "#" + hex(0x1000000 + R + G + B).split('x')[1][1:] + "," + opacity

    @api.onchange('ks_model_id')
    def make_record_field_empty(self):
        for rec in self:
            rec.ks_record_field = False
            rec.ks_domain = False
            rec.ks_date_filter_field = False
            # To show "created on" by default on date filter field on model select.
            if rec.ks_model_id:
                datetime_field_list = rec.ks_date_filter_field.search(
                    [('model_id', '=', rec.ks_model_id.id), '|', ('ttype', '=', 'date'),
                     ('ttype', '=', 'datetime')]).read(['id', 'name'])
                for field in datetime_field_list:
                    if field['name'] == 'create_date':
                        rec.ks_date_filter_field = field['id']
            else:
                rec.ks_date_filter_field = False
            # Pro
            rec.ks_record_field = False
            rec.ks_chart_measure_field = False
            rec.ks_chart_measure_field_2 = False
            rec.ks_chart_relation_sub_groupby = False
            rec.ks_chart_relation_groupby = False
            rec.ks_chart_date_sub_groupby = False
            rec.ks_chart_date_groupby = False
            rec.ks_sort_by_field = False
            rec.ks_sort_by_order = False
            rec.ks_record_data_limit = False
            rec.ks_list_view_fields = False
            rec.ks_list_view_group_fields = False

    @api.onchange('ks_record_count', 'ks_layout', 'name', 'ks_model_id', 'ks_domain', 'ks_icon_select',
                  'ks_default_icon', 'ks_icon',
                  'ks_background_color', 'ks_font_color', 'ks_default_icon_color')
    def ks_preview_update(self):
        self.ks_preview += 1

    @api.onchange('ks_dashboard_item_theme')
    def change_dashboard_item_theme(self):
        if self.ks_dashboard_item_theme == "red":
            self.ks_background_color = "#d9534f,0.99"
            self.ks_default_icon_color = "#ffffff,0.99"
            self.ks_font_color = "#ffffff,0.99"
        elif self.ks_dashboard_item_theme == "blue":
            self.ks_background_color = "#337ab7,0.99"
            self.ks_default_icon_color = "#ffffff,0.99"
            self.ks_font_color = "#ffffff,0.99"
        elif self.ks_dashboard_item_theme == "yellow":
            self.ks_background_color = "#f0ad4e,0.99"
            self.ks_default_icon_color = "#ffffff,0.99"
            self.ks_font_color = "#ffffff,0.99"
        elif self.ks_dashboard_item_theme == "green":
            self.ks_background_color = "#5cb85c,0.99"
            self.ks_default_icon_color = "#ffffff,0.99"
            self.ks_font_color = "#ffffff,0.99"
        elif self.ks_dashboard_item_theme == "white":
            self.ks_background_color = "#ffffff,0.99"
            self.ks_default_icon_color = "#000000,0.99"
            self.ks_font_color = "#000000,0.99"

        if self.ks_layout == 'layout4':
            self.ks_font_color = self.ks_background_color

        elif self.ks_layout == 'layout6':
            self.ks_default_icon_color = self.ks_get_dark_color(self.ks_background_color.split(',')[0],
                                                                self.ks_background_color.split(',')[1])


    @api.depends('ks_record_count_type', 'ks_model_id', 'ks_domain', 'ks_record_field', 'ks_date_filter_field',
                 'ks_item_end_date', 'ks_item_start_date')
    def ks_get_record_count(self):
        for rec in self:
            if rec.ks_record_count_type == 'count':
                rec.ks_record_count = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search_count', rec)
            elif rec.ks_record_count_type == 'sum' and rec.ks_record_field:
                ks_records = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search', rec)
                for filtered_records in ks_records:
                    rec.ks_record_count += filtered_records[rec.ks_record_field.name]
            elif rec.ks_record_count_type == 'average' and rec.ks_record_field:
                ks_records = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search', rec)
                ks_record_count = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search_count', rec)
                for filtered_records in ks_records:
                    rec.ks_record_count += filtered_records[rec.ks_record_field.name]
                rec.ks_record_count = rec.ks_record_count / ks_record_count if ks_record_count else 0
            else:
                rec.ks_record_count = 0

    # Writing separate function to fetch dashboard item data
    def ks_fetch_model_data(self, ks_model_name, ks_domain, ks_func, rec):
        data = 0
        try:
            if ks_domain and ks_domain != '[]' and ks_model_name:
                proper_domain = self.ks_convert_into_proper_domain(ks_domain, rec)
                if ks_func == 'search_count':
                    data = self.env[ks_model_name].search_count(proper_domain)
                elif ks_func == 'search':
                    data = self.env[ks_model_name].search(proper_domain)
            elif ks_model_name:
                # Have to put extra if condition here because on load,model giving False value
                proper_domain = self.ks_convert_into_proper_domain(False, rec)
                if ks_func == 'search_count':
                    data = self.env[ks_model_name].search_count(proper_domain)

                elif ks_func == 'search':
                    data = self.env[ks_model_name].search(proper_domain)
            else:
                return []
        except Exception as e:
            return []
        return data

    def ks_convert_into_proper_domain(self, ks_domain, rec):
        if ks_domain and "%UID" in ks_domain:
            ks_domain = ks_domain.replace('"%UID"', str(self.env.user.id))
        if not rec.ks_date_filter_selection or rec.ks_date_filter_selection == "l_none":
            selected_start_date = rec.env["ks_dashboard_ninja.board"].browse(
                rec.ks_dashboard_ninja_board_id.id).ks_dashboard_start_date
            selected_end_date = rec.env["ks_dashboard_ninja.board"].browse(
                rec.ks_dashboard_ninja_board_id.id).ks_dashboard_end_date
        else:
            self.ks_set_date_filter()
            selected_start_date = rec.ks_item_start_date
            selected_end_date = rec.ks_item_end_date
        if ks_domain:
            # try:
            proper_domain = eval(ks_domain)
            if selected_start_date and selected_end_date and rec.ks_date_filter_field:
                proper_domain.extend([(rec.ks_date_filter_field.name, ">=", selected_start_date),
                                      (rec.ks_date_filter_field.name, "<=", selected_end_date)])
                rec.ks_isDateFilterApplied = True
            else:
                rec.ks_isDateFilterApplied = False
        else:
            if selected_start_date and selected_end_date and rec.ks_date_filter_field:
                proper_domain = [(rec.ks_date_filter_field.name, ">=", selected_start_date),
                                 (rec.ks_date_filter_field.name, "<=", selected_end_date)]
            else:
                proper_domain = []
        return proper_domain


    @api.onchange('ks_chart_relation_groupby')
    def get_chart_groupby_type(self):
        for rec in self:
            if rec.ks_chart_relation_groupby.ttype == 'datetime' or rec.ks_chart_relation_groupby.ttype == 'date':
                rec.ks_chart_groupby_type = 'date_type'
            elif rec.ks_chart_relation_groupby.ttype == 'many2one':
                rec.ks_chart_groupby_type = 'relational_type'
                rec.ks_chart_date_groupby = False
            elif rec.ks_chart_relation_groupby.ttype == 'selection':
                rec.ks_chart_groupby_type = 'selection'
                rec.ks_chart_date_groupby = False
            else:
                rec.ks_chart_groupby_type = 'none'
                rec.ks_chart_date_groupby = False


    @api.onchange('ks_chart_relation_sub_groupby')
    def get_chart_sub_groupby_type(self):
        for rec in self:
            if rec.ks_chart_relation_sub_groupby.ttype == 'datetime' or rec.ks_chart_relation_sub_groupby.ttype == 'date':
                rec.ks_chart_sub_groupby_type = 'date_type'
            elif rec.ks_chart_relation_sub_groupby.ttype == 'many2one':
                rec.ks_chart_sub_groupby_type = 'relational_type'
                rec.ks_chart_date_sub_groupby = False
            elif rec.ks_chart_relation_sub_groupby.ttype == 'selection':
                rec.ks_chart_sub_groupby_type = 'selection'
                rec.ks_chart_date_sub_groupby = False
            else:
                rec.ks_chart_sub_groupby_type = 'none'
                rec.ks_chart_date_sub_groupby = False

    # Using this function just to let js call rpc to load some data later
    @api.model
    def ks_chart_load(self):
        return True


    @api.depends('ks_chart_measure_field', 'ks_chart_relation_groupby', 'ks_chart_date_groupby', 'ks_domain',
                 'ks_dashboard_item_type', 'ks_model_id', 'ks_sort_by_field', 'ks_sort_by_order',
                 'ks_record_data_limit', 'ks_chart_data_count_type', 'ks_chart_measure_field_2', 'ks_goal_enable',
                 'ks_record_data_limit', 'ks_chart_data_count_type', 'ks_chart_measure_field_2',
                 'ks_standard_goal_value', 'ks_goal_bar_line', 'ks_chart_relation_sub_groupby',
                 'ks_chart_date_sub_groupby', 'ks_date_filter_field', 'ks_item_start_date', 'ks_item_end_date')
    def ks_get_chart_data(self):
        for rec in self:
            if not rec.ks_chart_relation_groupby or rec.ks_chart_groupby_type == "date_type" and not rec.ks_chart_date_groupby:
                rec.ks_chart_relation_sub_groupby = False
                rec.ks_chart_date_sub_groupby = False

            if rec.ks_dashboard_item_type and rec.ks_dashboard_item_type != 'ks_tile' and rec.ks_dashboard_item_type != 'ks_list_view' and rec.ks_model_id and rec.ks_chart_data_count_type:
                ks_chart_data = {'labels': [], 'datasets': [], 'ks_show_second_y_scale': False}

                ks_chart_measure_field = []
                ks_chart_measure_field_2 = []

                # If count chart data type:
                if rec.ks_chart_data_count_type == "count":
                    ks_chart_data['datasets'].append({'data': [], 'label': "Count"})
                else:
                    if rec.ks_dashboard_item_type == 'ks_bar_chart':
                        if rec.ks_chart_measure_field_2:
                            ks_chart_data['ks_show_second_y_scale'] = True

                        for res in rec.ks_chart_measure_field_2:
                            ks_chart_measure_field_2.append(res.name)
                            ks_chart_data['datasets'].append(
                                {'data': [], 'label': res.field_description, 'type': 'line', 'yAxisID': 'y-axis-1'})
                    for res in rec.ks_chart_measure_field:
                        ks_chart_measure_field.append(res.name)
                        ks_chart_data['datasets'].append({'data': [], 'label': res.field_description})

                # ks_chart_measure_field = [res.name for res in rec.ks_chart_measure_field]
                ks_chart_groupby_relation_field = rec.ks_chart_relation_groupby.name

                ks_chart_domain = self.ks_convert_into_proper_domain(rec.ks_domain, rec)
                orderby = rec.ks_sort_by_field.name if rec.ks_sort_by_field else "id"
                if rec.ks_sort_by_order:
                    orderby = orderby + " " + rec.ks_sort_by_order
                limit = rec.ks_record_data_limit if rec.ks_record_data_limit else False

                if ((rec.ks_chart_data_count_type != "count" and ks_chart_measure_field) or (
                        rec.ks_chart_data_count_type == "count" and not ks_chart_measure_field)) and not rec.ks_chart_relation_sub_groupby:
                    if rec.ks_chart_groupby_type == 'relational_type' and rec.ks_chart_relation_groupby:
                        ks_chart_data['groupByIds'] = []
                        ks_chart_records = self.env[rec.ks_model_name].read_group(ks_chart_domain, set(
                            ks_chart_measure_field + ks_chart_measure_field_2 + [ks_chart_groupby_relation_field]),
                                                                                  [ks_chart_groupby_relation_field],
                                                                                  orderby=orderby, limit=limit)

                        for res in ks_chart_records:
                            if res[ks_chart_groupby_relation_field] and all(
                                    measure_field in res for measure_field in ks_chart_measure_field):
                                ks_chart_data['labels'].append(res[ks_chart_groupby_relation_field][1]._value)
                                ks_chart_data['groupByIds'].append(res[ks_chart_groupby_relation_field][0])
                                counter = 0
                                if ks_chart_measure_field:
                                    if ks_chart_measure_field_2:
                                        for field_rec in ks_chart_measure_field_2:
                                            data = res[field_rec] if rec.ks_chart_data_count_type == 'sum' else res[
                                                                                                                    field_rec] / \
                                                                                                                res[
                                                                                                                    ks_chart_groupby_relation_field + "_count"]
                                            ks_chart_data['datasets'][counter]['data'].append(data)
                                            counter += 1
                                    for field_rec in ks_chart_measure_field:
                                        data = res[field_rec] if rec.ks_chart_data_count_type == 'sum' else res[
                                                                                                                field_rec] / \
                                                                                                            res[
                                                                                                                ks_chart_groupby_relation_field + "_count"]
                                        ks_chart_data['datasets'][counter]['data'].append(data)
                                        counter += 1

                                else:
                                    data = res[ks_chart_groupby_relation_field + "_count"]
                                    ks_chart_data['datasets'][0]['data'].append(data)

                        # if rec.ks_goal_enable and rec.ks_dashboard_item_type in ['ks_bar_chart','ks_horizontalBar_chart','ks_line_chart','ks_area_chart'] and rec.ks_chart_groupby_type == "date_type":
                        #     goal_dataset = []
                        #     if rec.ks_standard_goal_value:
                        #         length = len(ks_chart_data['datasets'][0]['data'])
                        #         for i in range(length):
                        #             goal_dataset.append(rec.ks_standard_goal_value)
                        #     ks_chart_data['datasets'].append({'label': 'Target', 'data': goal_dataset})


                    elif rec.ks_chart_groupby_type == 'date_type' and rec.ks_chart_date_groupby:
                        ks_chart_records = self.env[rec.ks_model_name].read_group(ks_chart_domain, set(
                            ks_chart_measure_field + ks_chart_measure_field_2 + [ks_chart_groupby_relation_field]),
                                                                                  [
                                                                                      ks_chart_groupby_relation_field + ":" + rec.ks_chart_date_groupby],
                                                                                  orderby=orderby, limit=limit)

                        for res in ks_chart_records:
                            if res[ks_chart_groupby_relation_field + ":" + rec.ks_chart_date_groupby] and all(
                                    measure_field in res for measure_field in ks_chart_measure_field):
                                ks_chart_data['labels'].append(
                                    res[ks_chart_groupby_relation_field + ":" + rec.ks_chart_date_groupby])
                                counter = 0
                                if ks_chart_measure_field and len(ks_chart_measure_field) != 0:
                                    if ks_chart_measure_field_2:
                                        for field_rec in ks_chart_measure_field_2:
                                            data = res[
                                                field_rec] if rec.ks_chart_data_count_type == 'sum' else res[
                                                                                                             field_rec] / \
                                                                                                         res[
                                                                                                             ks_chart_groupby_relation_field + "_count"]
                                            ks_chart_data['datasets'][counter]['data'].append(data)
                                            counter += 1
                                    for field_rec in ks_chart_measure_field:
                                        data = res[
                                            field_rec] if rec.ks_chart_data_count_type == 'sum' else res[field_rec] / \
                                                                                                     res[
                                                                                                         ks_chart_groupby_relation_field + "_count"]
                                        ks_chart_data['datasets'][counter]['data'].append(data)
                                        counter += 1
                                else:
                                    data = res[ks_chart_groupby_relation_field + "_count"]
                                    ks_chart_data['datasets'][0]['data'].append(data)

                        if rec.ks_goal_enable and rec.ks_dashboard_item_type in ['ks_bar_chart',
                                                                                 'ks_horizontalBar_chart',
                                                                                 'ks_line_chart',
                                                                                 'ks_area_chart'] and rec.ks_chart_groupby_type == "date_type":
                            if rec._context.get('current_id', False):
                                ks_item_id = rec._context['current_id']
                            else:
                                ks_item_id = rec.id

                            selected_start_date = rec.env["ks_dashboard_ninja.board"].browse(
                                rec.ks_dashboard_ninja_board_id.id).ks_dashboard_start_date
                            selected_end_date = rec.env["ks_dashboard_ninja.board"].browse(
                                rec.ks_dashboard_ninja_board_id.id).ks_dashboard_end_date

                            ksGoalDomain = [('ks_dashboard_item', '=', ks_item_id)]
                            if selected_start_date and selected_end_date:
                                ksGoalDomain.extend([('ks_goal_date', '>=', selected_start_date.date()),
                                                     ('ks_goal_date', '<=', selected_end_date.date())])

                            ks_goal_records = self.env['ks_dashboard_ninja.item_goal'].read_group(
                                ksGoalDomain, ['ks_goal_value'],
                                ['ks_goal_date' + ":" + rec.ks_chart_date_groupby], )
                            ks_goal_labels = []
                            ks_goal_dataset = []
                            goal_dataset = []

                            if rec.ks_goal_lines and len(rec.ks_goal_lines) != 0:
                                for res in ks_goal_records:
                                    if res['ks_goal_date' + ":" + rec.ks_chart_date_groupby]:
                                        ks_goal_labels.append(res['ks_goal_date' + ":" + rec.ks_chart_date_groupby])
                                        ks_goal_dataset.append(res['ks_goal_value'])

                                ks_chart_records_dates = ks_chart_data['labels'] + list(
                                    set(ks_goal_labels) - set(ks_chart_data['labels']))

                                if rec.ks_chart_date_groupby == 'day':
                                    ks_chart_records_dates.sort(key=lambda date: datetime.strptime(date, '%d %b %Y'))
                                elif rec.ks_chart_date_groupby == 'week':
                                    ks_chart_records_dates.sort(
                                        key=lambda date: datetime.strptime(date[1:] + " 0", '%W %Y %w'))
                                elif rec.ks_chart_date_groupby == 'month':
                                    ks_chart_records_dates.sort(key=lambda date: datetime.strptime(date, '%B %Y'))
                                elif rec.ks_chart_date_groupby == 'quarter':
                                    ks_chart_records_dates_2 = []
                                    for record in ks_chart_records_dates:
                                        if record[1] == '1':
                                            ks_chart_records_dates_2.append(record + ' Jan')
                                        elif record[1] == '2':
                                            ks_chart_records_dates_2.append(record + ' Apr')
                                        elif record[1] == '3':
                                            ks_chart_records_dates_2.append(record + ' Jul')
                                        elif record[1] == '4':
                                            ks_chart_records_dates_2.append(record + ' Oct')
                                    ks_chart_records_dates_2.sort(key=lambda date: datetime.strptime(date[3:], '%Y %b'))
                                    ks_chart_records_dates.clear()
                                    for record in ks_chart_records_dates_2:
                                        ks_chart_records_dates.append(record[0:7])

                                elif rec.ks_chart_date_groupby == 'year':
                                    ks_chart_records_dates.sort(key=lambda date: datetime.strptime(date, '%Y'))

                                datasets = []
                                for dataset in ks_chart_data['datasets']:
                                    datasets.append(dataset['data'].copy())

                                for dataset in ks_chart_data['datasets']:
                                    dataset['data'].clear()

                                for label in ks_chart_records_dates:
                                    counterr = 0
                                    if label in ks_chart_data['labels']:
                                        index = ks_chart_data['labels'].index(label)

                                        for dataset in ks_chart_data['datasets']:
                                            dataset['data'].append(datasets[counterr][index])
                                            counterr += 1
                                    else:
                                        for dataset in ks_chart_data['datasets']:
                                            dataset['data'].append(0.00)

                                    if label in ks_goal_labels:
                                        index = ks_goal_labels.index(label)
                                        goal_dataset.append(ks_goal_dataset[index])
                                    else:
                                        goal_dataset.append(0.00)

                                ks_chart_data['labels'] = ks_chart_records_dates
                            else:
                                if rec.ks_standard_goal_value:
                                    length = len(ks_chart_data['datasets'][0]['data'])
                                    for i in range(length):
                                        goal_dataset.append(rec.ks_standard_goal_value)
                            ks_goal_datasets = {
                                'label': 'Target',
                                'data': goal_dataset,
                            }
                            if rec.ks_goal_bar_line:
                                ks_goal_datasets['type'] = 'line'
                                ks_chart_data['datasets'].insert(0, ks_goal_datasets)
                            else:
                                ks_chart_data['datasets'].append(ks_goal_datasets)
                    elif rec.ks_chart_groupby_type == 'selection':
                        ks_chart_records = self.env[rec.ks_model_name].read_group(ks_chart_domain, set(
                            ks_chart_measure_field + ks_chart_measure_field_2 + [ks_chart_groupby_relation_field]),
                                                                                  [ks_chart_groupby_relation_field],
                                                                                  orderby=orderby, limit=limit)

                        for res in ks_chart_records:
                            selection = res[ks_chart_groupby_relation_field]
                            if res[ks_chart_groupby_relation_field] and all(
                                    measure_field in res for measure_field in ks_chart_measure_field):
                                ks_chart_data['labels'].append(dict(
                                    self.env[rec.ks_model_name].fields_get(allfields=[ks_chart_groupby_relation_field])
                                    [ks_chart_groupby_relation_field]['selection'])[selection])
                                counter = 0
                                if ks_chart_measure_field and len(ks_chart_measure_field) != 0:
                                    if ks_chart_measure_field_2:
                                        for field_rec in ks_chart_measure_field_2:
                                            data = res[
                                                field_rec] if rec.ks_chart_data_count_type == 'sum' else res[
                                                                                                             field_rec] / \
                                                                                                         res[
                                                                                                             ks_chart_groupby_relation_field + "_count"]
                                            ks_chart_data['datasets'][counter]['data'].append(data)
                                            counter += 1
                                    for field_rec in ks_chart_measure_field:
                                        data = res[
                                            field_rec] if rec.ks_chart_data_count_type == 'sum' else res[field_rec] / \
                                                                                                     res[
                                                                                                         ks_chart_groupby_relation_field + "_count"]
                                        ks_chart_data['datasets'][counter]['data'].append(data)
                                        counter += 1
                                else:
                                    data = res[ks_chart_groupby_relation_field + "_count"]
                                    ks_chart_data['datasets'][0]['data'].append(data)

                elif rec.ks_chart_relation_sub_groupby and ((rec.ks_chart_sub_groupby_type == 'relational_type') or
                                                            (rec.ks_chart_sub_groupby_type == 'selection') or (
                                                                    rec.ks_chart_sub_groupby_type == 'date_type'
                                                                    and rec.ks_chart_date_sub_groupby)):
                    if len(ks_chart_measure_field) != 0 or rec.ks_chart_data_count_type == 'count':
                        if rec.ks_chart_groupby_type == 'date_type' and rec.ks_chart_date_groupby:
                            ks_chart_group = rec.ks_chart_relation_groupby.name + ":" + rec.ks_chart_date_groupby
                        else:
                            ks_chart_group = rec.ks_chart_relation_groupby.name

                        if rec.ks_chart_sub_groupby_type == 'date_type' and rec.ks_chart_date_sub_groupby:
                            ks_chart_sub_groupby_field = rec.ks_chart_relation_sub_groupby.name + ":" + \
                                                         rec.ks_chart_date_sub_groupby
                        else:
                            ks_chart_sub_groupby_field = rec.ks_chart_relation_sub_groupby.name

                        ks_chart_groupby_relation_fields = [ks_chart_group, ks_chart_sub_groupby_field]
                        ks_chart_record = self.env[rec.ks_model_name].read_group(ks_chart_domain,
                                                                                 set(ks_chart_measure_field
                                                                                     + ks_chart_measure_field_2 + [
                                                                                         ks_chart_groupby_relation_field,
                                                                                         rec.ks_chart_relation_sub_groupby.name]),
                                                                                 ks_chart_groupby_relation_fields,
                                                                                 orderby=orderby, limit=limit,
                                                                                 lazy=False)
                        chart_data = []
                        chart_sub_data = []
                        for res in ks_chart_record:

                            if res[ks_chart_groupby_relation_fields[0]] and res[ks_chart_groupby_relation_fields[1]]:
                                if rec.ks_chart_groupby_type == 'date_type':
                                    label = res[ks_chart_groupby_relation_fields[0]].split(" ")[0]
                                elif rec.ks_chart_groupby_type == 'selection':
                                    selection = res[ks_chart_groupby_relation_fields[0]]
                                    label = dict(self.env[rec.ks_model_name].fields_get(
                                        allfields=[ks_chart_groupby_relation_fields[0]])
                                                 [ks_chart_groupby_relation_fields[0]]['selection'])[selection]
                                else:
                                    label = res[ks_chart_groupby_relation_fields[0]][1]._value
                                labels = []
                                value = []
                                value_2 = []
                                labels_2 = []
                                if rec.ks_chart_data_count_type != 'count':
                                    for ress in rec.ks_chart_measure_field:
                                        if rec.ks_chart_sub_groupby_type == 'date_type':
                                            labels.append(res[ks_chart_groupby_relation_fields[1]].split(" ")[
                                                              0] + " " + ress.field_description)
                                        elif rec.ks_chart_sub_groupby_type == 'selection':
                                            selection = res[ks_chart_groupby_relation_fields[1]]
                                            labels.append(dict(self.env[rec.ks_model_name].fields_get(
                                                allfields=[ks_chart_groupby_relation_fields[1]])
                                                               [ks_chart_groupby_relation_fields[1]]['selection'])[
                                                              selection]
                                                          + " " + ress.field_description)
                                        else:
                                            labels.append(res[ks_chart_groupby_relation_fields[1]][1]._value
                                                          + " " + ress.field_description)
                                        value.append(res[ress.name])
                                    if rec.ks_chart_measure_field_2 and rec.ks_dashboard_item_type == 'ks_bar_chart':
                                        for ress in rec.ks_chart_measure_field_2:
                                            if rec.ks_chart_sub_groupby_type == 'date_type':
                                                labels_2.append(
                                                    res[ks_chart_groupby_relation_fields[1]].split(" ")[0] + " "
                                                    + ress.field_description)
                                            elif rec.ks_chart_sub_groupby_type == 'selection':
                                                selection = res[ks_chart_groupby_relation_fields[1]]
                                                labels_2.append(dict(self.env[rec.ks_model_name].fields_get(
                                                    allfields=[ks_chart_groupby_relation_fields[1]])
                                                                   [ks_chart_groupby_relation_fields[1]]['selection'])[
                                                                  selection] + " " + ress.field_description)
                                            else:
                                                labels_2.append(
                                                    res[ks_chart_groupby_relation_fields[1]][1]._value + " " +
                                                    ress.field_description)
                                            value_2.append(res[ress.name])

                                        chart_sub_data.append({
                                            'value': value_2,
                                            'labels': label,
                                            'series': labels_2
                                        })
                                else:
                                    if rec.ks_chart_sub_groupby_type == 'date_type':
                                        labels.append(res[ks_chart_groupby_relation_fields[1]].split(" ")[0])
                                    elif rec.ks_chart_sub_groupby_type == 'selection':
                                        selection = res[ks_chart_groupby_relation_fields[1]]
                                        labels.append(dict(self.env[rec.ks_model_name].fields_get(
                                            allfields=[ks_chart_groupby_relation_fields[1]])
                                                           [ks_chart_groupby_relation_fields[1]]['selection'])[
                                                          selection])
                                    else:
                                        labels.append(res[ks_chart_groupby_relation_fields[1]][1]._value)
                                    value.append(res['__count'])

                                chart_data.append({
                                    'value': value,
                                    'labels': label,
                                    'series': labels
                                })

                        xlabels = []
                        series = []
                        values = {}
                        for data in chart_data:
                            label = data['labels']
                            serie = data['series']

                            if (len(xlabels) == 0) or (label not in xlabels):
                                xlabels.append(label)

                            series = series + serie
                            value = data['value']
                            counter = 0
                            for seri in serie:
                                if seri not in values:
                                    values[seri] = {}
                                values[seri][label] = value[counter]
                                counter = +1

                        final_datasets = []
                        for serie in series:
                            if serie not in final_datasets:
                                final_datasets.append(serie)

                        ks_data = []
                        for dataset in final_datasets:
                            ks_dataset = {
                                'value': [],
                                'key': dataset
                            }
                            for label in xlabels:
                                ks_dataset['value'].append({
                                    'x': label,
                                    'y': values[dataset][label] if label in values[dataset] else 0
                                })
                            ks_data.append(ks_dataset)

                        ks_chart_data = {
                            'labels': [],
                            'datasets': []
                        }
                        if len(ks_data) != 0:
                            for res in ks_data[0]['value']:
                                ks_chart_data['labels'].append(res['x'])
                            if rec.ks_chart_measure_field_2 and rec.ks_dashboard_item_type == 'ks_bar_chart':
                                values_2 = {}
                                series_2 = []
                                for data in chart_sub_data:
                                    label = data['labels']
                                    serie = data['series']
                                    series_2 = series_2 + serie
                                    value = data['value']

                                    counter = 0
                                    for seri in serie:
                                        if seri not in values_2:
                                            values_2[seri] = {}

                                        values_2[seri][label] = value[counter]
                                        counter = +1
                                final_datasets_2 = []
                                for serie in series_2:
                                    if serie not in final_datasets_2:
                                        final_datasets_2.append(serie)
                                ks_data_2 = []
                                for dataset in final_datasets_2:
                                    ks_dataset = {
                                        'value': [],
                                        'key': dataset
                                    }
                                    for label in xlabels:
                                        ks_dataset['value'].append({
                                            'x': label,
                                            'y': values_2[dataset][label] if label in values_2[dataset] else 0
                                        })
                                    ks_data_2.append(ks_dataset)

                                for ks_dat in ks_data_2:
                                    dataset = {
                                        'label': ks_dat['key'],
                                        'data': [],
                                        'type': 'line'
                                    }
                                    for res in ks_dat['value']:
                                        dataset['data'].append(res['y'])

                                    ks_chart_data['datasets'].append(dataset)
                            for ks_dat in ks_data:
                                dataset = {
                                    'label': ks_dat['key'],
                                    'data': []
                                }
                                for res in ks_dat['value']:
                                    dataset['data'].append(res['y'])

                                ks_chart_data['datasets'].append(dataset)
                    else:
                        ks_chart_data = False

                rec.ks_chart_data = json.dumps(ks_chart_data)
            elif not rec.ks_dashboard_item_type or rec.ks_dashboard_item_type == 'ks_tile':
                rec.ks_chart_measure_field = False
                rec.ks_chart_measure_field_2 = False
                rec.ks_chart_relation_groupby = False


    @api.depends('ks_domain', 'ks_dashboard_item_type', 'ks_model_id', 'ks_sort_by_field', 'ks_sort_by_order',
                 'ks_record_data_limit', 'ks_list_view_fields', 'ks_list_view_type', 'ks_list_view_group_fields',
                 'ks_chart_groupby_type', 'ks_chart_date_groupby', 'ks_date_filter_field', 'ks_item_end_date',
                 'ks_item_start_date')
    def ks_get_list_view_data(self):
        for rec in self:
            if rec.ks_list_view_type and rec.ks_dashboard_item_type and rec.ks_dashboard_item_type == 'ks_list_view' and \
                    rec.ks_model_id:
                ks_list_view_data = {'label': [],
                                     'data_rows': [], 'model': rec.ks_model_name}

                ks_chart_domain = self.ks_convert_into_proper_domain(rec.ks_domain, rec)
                orderby = rec.ks_sort_by_field.name if rec.ks_sort_by_field else "id"
                if rec.ks_sort_by_order:
                    orderby = orderby + " " + rec.ks_sort_by_order
                limit = rec.ks_record_data_limit if rec.ks_record_data_limit else False

                if rec.ks_list_view_type == "ungrouped" and rec.ks_list_view_fields:
                    ks_list_view_data['list_view_type'] = 'none'
                    ks_list_view_data['groupby'] = False
                    ks_list_view_data['label'] = []
                    ks_list_view_data['date_index'] = []
                    for res in rec.ks_list_view_fields:
                        if (res.ttype == "datetime" or res.ttype == "date"):
                            index = len(ks_list_view_data['label'])
                            ks_list_view_data['label'].append(res.field_description)
                            ks_list_view_data['date_index'].append(index)
                        else:
                            ks_list_view_data['label'].append(res.field_description)

                    ks_list_view_fields = [res.name for res in rec.ks_list_view_fields]
                    ks_list_view_field_type = [res.ttype for res in rec.ks_list_view_fields]
                    try :
                        ks_list_view_records = self.env[rec.ks_model_name].search_read(ks_chart_domain,
                                                                                              ks_list_view_fields,
                                                                                              order=orderby, limit=limit)
                    except Exception as e:
                        rec.ks_list_view_data = False
                        return 0
                    for res in ks_list_view_records:
                        counter = 0
                        data_row = {'id': res['id'], 'data': []}
                        for field_rec in ks_list_view_fields:
                            if type(res[field_rec]) == fields.datetime or type(res[field_rec]) == fields.date:
                                res[field_rec] = res[field_rec].strftime("%D %T")
                            elif ks_list_view_field_type[counter] == "many2one":
                                if res[field_rec]:
                                    res[field_rec] = res[field_rec][1]
                            data_row['data'].append(res[field_rec])
                            counter += 1
                        ks_list_view_data['data_rows'].append(data_row)

                elif rec.ks_list_view_type == "grouped" and rec.ks_list_view_group_fields and rec.ks_chart_relation_groupby:
                    ks_list_fields = []

                    if rec.ks_chart_groupby_type == 'relational_type':
                        ks_list_view_data['list_view_type'] = 'relational_type'
                        ks_list_view_data['groupby'] = rec.ks_chart_relation_groupby.name
                        ks_list_fields.append(rec.ks_chart_relation_groupby.name)
                        ks_list_view_data['label'].append(rec.ks_chart_relation_groupby.field_description)
                        for res in rec.ks_list_view_group_fields:
                            ks_list_fields.append(res.name)
                            ks_list_view_data['label'].append(res.field_description)

                        ks_list_view_records = self.env[rec.ks_model_name].read_group(ks_chart_domain, ks_list_fields,
                                                                                      [
                                                                                          rec.ks_chart_relation_groupby.name],
                                                                                      orderby=orderby, limit=limit)
                        for res in ks_list_view_records:
                            if all(list_fields in res for list_fields in ks_list_fields) and res[
                                rec.ks_chart_relation_groupby.name]:
                                counter = 0
                                data_row = {'id': res[rec.ks_chart_relation_groupby.name][0], 'data': []}
                                for field_rec in ks_list_fields:
                                    if counter == 0:
                                        data_row['data'].append(res[field_rec][1]._value)
                                    else:
                                        data_row['data'].append(res[field_rec])
                                    counter += 1
                                ks_list_view_data['data_rows'].append(data_row)

                    elif rec.ks_chart_groupby_type == 'date_type' and rec.ks_chart_date_groupby:
                        ks_list_view_data['list_view_type'] = 'date_type'
                        ks_list_field = []
                        ks_list_view_data[
                            'groupby'] = rec.ks_chart_relation_groupby.name + ':' + rec.ks_chart_date_groupby
                        ks_list_field.append(rec.ks_chart_relation_groupby.name)
                        ks_list_fields.append(rec.ks_chart_relation_groupby.name + ':' + rec.ks_chart_date_groupby)
                        ks_list_view_data['label'].append(
                            rec.ks_chart_relation_groupby.field_description + ' : ' + rec.ks_chart_date_groupby.capitalize())
                        for res in rec.ks_list_view_group_fields:
                            ks_list_fields.append(res.name)
                            ks_list_field.append(res.name)
                            ks_list_view_data['label'].append(res.field_description)

                        ks_list_view_records = self.env[rec.ks_model_name].read_group(ks_chart_domain, ks_list_field,
                                                                                      [
                                                                                          rec.ks_chart_relation_groupby.name + ':' + rec.ks_chart_date_groupby],
                                                                                      orderby=orderby, limit=limit)
                        for res in ks_list_view_records:
                            if all(list_fields in res for list_fields in ks_list_fields):
                                counter = 0
                                data_row = {'id': 0, 'data': []}
                                for field_rec in ks_list_fields:
                                    data_row['data'].append(res[field_rec])
                                ks_list_view_data['data_rows'].append(data_row)

                    elif rec.ks_chart_groupby_type == 'selection':
                        ks_list_view_data['list_view_type'] = 'selection'
                        ks_list_view_data['groupby'] = rec.ks_chart_relation_groupby.name
                        ks_selection_field = rec.ks_chart_relation_groupby.name
                        ks_list_view_data['label'].append(rec.ks_chart_relation_groupby.field_description)
                        for res in rec.ks_list_view_group_fields:
                            ks_list_fields.append(res.name)
                            ks_list_view_data['label'].append(res.field_description)

                        ks_list_view_records = self.env[rec.ks_model_name].read_group(ks_chart_domain, ks_list_fields,
                                                                                      [
                                                                                          rec.ks_chart_relation_groupby.name],
                                                                                      orderby=orderby, limit=limit)
                        for res in ks_list_view_records:
                            if all(list_fields in res for list_fields in ks_list_fields):
                                counter = 0
                                data_row = {'id': 0, 'data': []}
                                data_row['data'].append(dict(
                                    self.env[rec.ks_model_name].fields_get(allfields=ks_selection_field)
                                    [ks_selection_field]['selection'])[res[ks_selection_field]])
                                for field_rec in ks_list_fields:
                                    data_row['data'].append(res[field_rec])
                                ks_list_view_data['data_rows'].append(data_row)

                rec.ks_list_view_data = json.dumps(ks_list_view_data)


    @api.onchange('ks_dashboard_item_type')
    def set_color_palette(self):
        for rec in self:
            if rec.ks_dashboard_item_type == "ks_bar_chart" or rec.ks_dashboard_item_type == "ks_horizontalBar_chart" or rec.ks_dashboard_item_type == "ks_line_chart" or rec.ks_dashboard_item_type == "ks_area_chart":
                rec.ks_chart_item_color = "cool"
            else:
                rec.ks_chart_item_color = "default"

    #  Time Filter Calculation

    @api.onchange('ks_date_filter_selection')
    def ks_set_date_filter(self):
        for rec in self:
            if (not rec.ks_date_filter_selection) or rec.ks_date_filter_selection == "l_none":
                rec.ks_item_start_date = rec.ks_item_end_date = False
            elif rec.ks_date_filter_selection != 'l_custom':
                ks_date_data = ks_get_date(rec.ks_date_filter_selection)
                rec.ks_item_start_date = ks_date_data["selected_start_date"]
                rec.ks_item_end_date = ks_date_data["selected_end_date"]


    @api.depends('ks_dashboard_item_type', 'ks_model_id', 'ks_model_id_2', 'ks_record_field', 'ks_goal_enable',
                 'ks_standard_goal_value', 'ks_record_field_2', 'ks_record_count_type_2', 'ks_domain', 'ks_domain_2',
                 'ks_date_filter_selection', 'ks_item_start_date', 'ks_record_count_type',
                 'ks_item_end_date', 'ks_previous_period', 'ks_item_start_date_2', 'ks_item_end_date')
    def ks_get_kpi_data(self):
        for rec in self:
            if rec.ks_dashboard_item_type and rec.ks_dashboard_item_type == 'ks_kpi' and rec.ks_model_id:
                ks_kpi_data = []
                ks_record_count = 0.0
                ks_kpi_data_model_1 = {}
                if rec.ks_record_count_type == 'count':
                    ks_record_count = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search_count', rec)
                elif rec.ks_record_count_type == 'sum' and rec.ks_record_field:
                    ks_records = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search', rec)
                    for filtered_records in ks_records:
                        ks_record_count += filtered_records[rec.ks_record_field.name]
                elif rec.ks_record_count_type == 'average' and rec.ks_record_field:
                    ks_records = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search', rec)
                    ks_record_counts = rec.ks_fetch_model_data(rec.ks_model_name, rec.ks_domain, 'search_count', rec)
                    for filtered_records in ks_records:
                        ks_record_count += filtered_records[rec.ks_record_field.name]
                    ks_record_count = ks_record_count / ks_record_counts if ks_record_count else 0
                else:
                    ks_record_count = 0
                ks_kpi_data_model_1['model'] = rec.ks_model_name
                ks_kpi_data_model_1['record_field'] = rec.ks_record_field.field_description
                ks_kpi_data_model_1['record_data'] = ks_record_count

                if rec.ks_goal_enable:
                    ks_kpi_data_model_1['target'] = rec.ks_standard_goal_value
                ks_kpi_data.append(ks_kpi_data_model_1)

                if rec.ks_previous_period:
                    ks_previous_period_data = rec.ks_get_previous_period_data(rec)
                    ks_kpi_data_model_1['previous_period'] = ks_previous_period_data

                if rec.ks_model_id_2 and rec.ks_record_count_type_2:
                    ks_kpi_data_model_2 = rec.ks_get_model_2_data(rec.ks_model_name_2, rec.ks_record_count_type_2,
                                                                  rec.ks_record_field_2, rec.ks_domain_2, rec)
                    ks_kpi_data.append(ks_kpi_data_model_2)

                rec.ks_kpi_data = json.dumps(ks_kpi_data)

    # writing separate function for fetching previous period data
    def ks_get_previous_period_data(self, rec):
        switcher = {
            'l_day': "ks_get_date('ls_day')",
            't_week': "ks_get_date('ls_week')",
            't_month': "ks_get_date('ls_month')",
            't_quarter': "ks_get_date('ls_quarter')",
            't_year': "ks_get_date('ls_year')",
        }

        if rec.ks_date_filter_selection =="l_none":
            date_filter_selection = rec.ks_dashboard_ninja_board_id.ks_date_filter_selection
        else:
            date_filter_selection = rec.ks_date_filter_selection
        ks_date_data = eval(switcher.get(date_filter_selection, "False"))

        if (ks_date_data):
            previous_period_start_date = ks_date_data["selected_start_date"]
            previous_period_end_date = ks_date_data["selected_end_date"]
            proper_domain = rec.ks_get_previous_period_domain(rec.ks_domain, previous_period_start_date,
                                                              previous_period_end_date, rec.ks_date_filter_field)
            ks_record_count = 0.0

            if rec.ks_record_count_type == 'count':
                ks_record_count = self.env[rec.ks_model_name].search_count(proper_domain)
                return ks_record_count
            elif rec.ks_record_field:
                data = self.env[rec.ks_model_name].search(proper_domain)
                for filtered_records in data:
                    ks_record_count += filtered_records[rec.ks_record_field.name]
                if rec.ks_record_count_type == 'sum':
                    return ks_record_count
                else:
                    data_count = self.env[rec.ks_model_name].search_count(proper_domain)
                    ks_record_count = ks_record_count / data_count if data_count != 0 else 0
                    return ks_record_count
            else:
                return False
        else:
            return False

    def ks_get_previous_period_domain(self, ks_domain, ks_start_date, ks_end_date, date_filter_field):
        if ks_domain and "%UID" in ks_domain:
            ks_domain = ks_domain.replace('"%UID"', str(self.env.user.id))
        if ks_domain:
            # try:
            proper_domain = eval(ks_domain)
            if ks_start_date and ks_end_date and date_filter_field:
                proper_domain.extend([(date_filter_field.name, ">=", ks_start_date),
                                      (date_filter_field.name, "<=", ks_end_date)])

        else:
            if ks_start_date and ks_end_date and date_filter_field:
                proper_domain = ([(date_filter_field.name, ">=", ks_start_date),
                                  (date_filter_field.name, "<=", ks_end_date)])
            else:
                proper_domain = []
        return proper_domain

    def ks_get_model_2_data(self, ks_model_name_2, ks_record_count_type_2, ks_record_field_2, ks_domain, rec):
        if rec.ks_record_count_type_2 == 'count':
            ks_record_count = rec.ks_fetch_model_data_2(ks_model_name_2, ks_domain, 'search_count', rec)
        elif ks_record_count_type_2 == 'sum' and ks_record_field_2:
            ks_records = rec.ks_fetch_model_data_2(ks_model_name_2, ks_domain, 'search', rec)
            ks_record_count = 0
            for filtered_records in ks_records:
                ks_record_count += filtered_records[ks_record_field_2.name]
        elif ks_record_count_type_2 == 'average' and ks_record_field_2:
            ks_records = rec.ks_fetch_model_data_2(ks_model_name_2, ks_domain, 'search', rec)
            ks_record_counts = rec.ks_fetch_model_data_2(ks_model_name_2, ks_domain, 'search_count', rec)
            ks_record_count = 0
            for filtered_records in ks_records:
                ks_record_count += filtered_records[ks_record_field_2.name]
            ks_record_count = ks_record_count / ks_record_counts if ks_record_count else 0
        else:
            ks_record_count = False
        ks_kpi_data_model_2 = {}
        ks_kpi_data_model_2['model'] = rec.ks_model_name_2
        ks_kpi_data_model_2[
            'record_field'] = 'count' if ks_record_count_type_2 == 'count' else ks_record_field_2.field_description
        ks_kpi_data_model_2['record_data'] = ks_record_count

        return ks_kpi_data_model_2

    @api.onchange('ks_model_id_2')
    def make_record_field_empty_2(self):
        for rec in self:
            rec.ks_record_field_2 = False
            rec.ks_domain_2 = False
            rec.ks_date_filter_field_2 = False
            # To show "created on" by default on date filter field on model select.
            if rec.ks_model_id:
                datetime_field_list = rec.ks_date_filter_field_2.search(
                    [('model_id', '=', rec.ks_model_id.id), '|', ('ttype', '=', 'date'),
                     ('ttype', '=', 'datetime')]).read(['id', 'name'])
                for field in datetime_field_list:
                    if field['name'] == 'create_date':
                        rec.ks_date_filter_field_2 = field['id']
            else:
                rec.ks_date_filter_field_2 = False

    # Writing separate function to fetch dashboard item data
    def ks_fetch_model_data_2(self, ks_model_name, ks_domain, ks_func, rec):
        data = 0
        try:
            if ks_domain and ks_domain != '[]' and ks_model_name:
                proper_domain = self.ks_convert_into_proper_domain_2(ks_domain, rec)
                if ks_func == 'search_count':
                    data = self.env[ks_model_name].search_count(proper_domain)
                elif ks_func == 'search':
                    data = self.env[ks_model_name].search(proper_domain)
            elif ks_model_name:
                # Have to put extra if condition here because on load,model giving False value
                proper_domain = self.ks_convert_into_proper_domain_2(False, rec)
                if ks_func == 'search_count':
                    data = self.env[ks_model_name].search_count(proper_domain)

                elif ks_func == 'search':
                    data = self.env[ks_model_name].search(proper_domain)
            else:
                return []
        except Exception as e:
            return []
        return data


    @api.onchange('ks_date_filter_selection_2')
    def ks_set_date_filter_2(self):
        for rec in self:
            if (not rec.ks_date_filter_selection_2) or rec.ks_date_filter_selection_2 == "l_none":
                rec.ks_item_start_date_2 = rec.ks_item_end_date = False
            elif rec.ks_date_filter_selection_2 != 'l_custom':
                ks_date_data = ks_get_date(rec.ks_date_filter_selection_2)
                rec.ks_item_start_date_2 = ks_date_data["selected_start_date"]
                rec.ks_item_end_date_2 = ks_date_data["selected_end_date"]

    def ks_convert_into_proper_domain_2(self, ks_domain_2, rec):
        if ks_domain_2 and "%UID" in ks_domain_2:
            ks_domain_2 = ks_domain_2.replace('"%UID"', str(self.env.user.id))
        if (not rec.ks_date_filter_selection_2) or rec.ks_date_filter_selection_2 == "l_none":
            selected_start_date = rec.env["ks_dashboard_ninja.board"].browse(
                rec.ks_dashboard_ninja_board_id.id).ks_dashboard_start_date
            selected_end_date = rec.env["ks_dashboard_ninja.board"].browse(
                rec.ks_dashboard_ninja_board_id.id).ks_dashboard_end_date
        else:
            self.ks_set_date_filter_2()
            selected_start_date = rec.ks_item_start_date_2
            selected_end_date = rec.ks_item_end_date_2
        if ks_domain_2:
            # try:
            proper_domain = eval(ks_domain_2)
            if selected_start_date and selected_end_date and rec.ks_date_filter_field:
                proper_domain.extend([(rec.ks_date_filter_field_2.name, ">=", selected_start_date),
                                      (rec.ks_date_filter_field_2.name, "<=", selected_end_date)])
                rec.ks_isDateFilterApplied = True
            else:
                rec.ks_isDateFilterApplied = False
        else:
            if selected_start_date and selected_end_date and rec.ks_date_filter_field:
                proper_domain = [(rec.ks_date_filter_field_2.name, ">=", selected_start_date),
                                 (rec.ks_date_filter_field_2.name, "<=", selected_end_date)]
            else:
                proper_domain = []
        return proper_domain


class KsDashboardItemsGoal(models.Model):
    _name = 'ks_dashboard_ninja.item_goal'

    ks_goal_date = fields.Date(string="Date")
    ks_goal_value = fields.Float(string="Value")

    ks_dashboard_item = fields.Many2one('ks_dashboard_ninja.item', string="Dashboard Item")
