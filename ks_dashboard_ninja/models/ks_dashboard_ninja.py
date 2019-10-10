# -*- coding: utf-8 -*-

from eagle import models, fields, api, _
from eagle.exceptions import ValidationError
import datetime
import json
from ..lib.ks_date_filter_selections import ks_get_date


class KsDashboardNinjaBoard(models.Model):
    _name = 'ks_dashboard_ninja.board'

    name = fields.Char(string="Dashboard Name", required=True, size=35)
    ks_dashboard_items_ids = fields.One2many('ks_dashboard_ninja.item', 'ks_dashboard_ninja_board_id',
                                             string='Dashboard Items')
    ks_dashboard_menu_name = fields.Char(string="Menu Name")
    ks_dashboard_top_menu_id = fields.Many2one('ir.ui.menu', domain="[('parent_id','=',False)]",
                                               string="Show Under Menu")
    ks_dashboard_client_action_id = fields.Many2one('ir.actions.client')
    ks_dashboard_menu_id = fields.Many2one('ir.ui.menu')
    ks_dashboard_state = fields.Char()
    ks_dashboard_active = fields.Boolean(string="Active", default=True)
    ks_dashboard_group_access = fields.Many2many('res.groups', string="Group Access")

    # DateFilter Fields
    ks_dashboard_start_date = fields.Datetime()
    ks_dashboard_end_date = fields.Datetime()
    ks_date_filter_selection = fields.Selection([
        ('l_none', 'All Time'),
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
    ], default='l_none')

    ks_gridstack_config = fields.Char('Item Configurations')
    ks_dashboard_default_template = fields.Many2one('ks_dashboard_ninja.board_template',
                                                    default=lambda self: self.env.ref('ks_dashboard_ninja.ks_blank',
                                                                                      False),
                                                    string="Dashboard Template", required=True)

    ks_set_interval = fields.Selection([
        (15000, '15 Seconds'),
        (30000, '30 Seconds'),
        (45000, '45 Seconds'),
        (60000, '1 minute'),
        (120000, '2 minute'),
        (300000, '5 minute'),
        (600000, '10 minute'),
    ], string="Update Interval")

    @api.model
    def create(self, vals):
        record = super(KsDashboardNinjaBoard, self).create(vals)
        if 'ks_dashboard_top_menu_id' in vals and 'ks_dashboard_menu_name' in vals:
            action_id = {
                'name': vals['ks_dashboard_menu_name'] + " Action",
                'res_model': 'ks_dashboard_ninja.board',
                'tag': 'ks_dashboard_ninja',
                'params': {'ks_dashboard_id': record.id},
            }
            record.ks_dashboard_client_action_id = self.env['ir.actions.client'].sudo().create(action_id)

            record.ks_dashboard_menu_id = self.env['ir.ui.menu'].sudo().create({
                'name': vals['ks_dashboard_menu_name'],
                'active': vals.get('ks_dashboard_active', True),
                'parent_id': vals['ks_dashboard_top_menu_id'],
                'action': "ir.actions.client," + str(record.ks_dashboard_client_action_id.id),
                'groups_id': vals.get('ks_dashboard_group_access', False),
            })

        if record.ks_dashboard_default_template.ks_item_count:
            ks_gridstack_config = {}
            template_data = json.loads(record.ks_dashboard_default_template.ks_gridstack_config)
            for item_data in template_data:
                dashboard_item = self.env.ref(item_data['item_id']).copy({'ks_dashboard_ninja_board_id': record.id})
                ks_gridstack_config[dashboard_item.id] = item_data['data']
            record.ks_gridstack_config = json.dumps(ks_gridstack_config)
        return record

    @api.multi
    def write(self, vals):
        record = super(KsDashboardNinjaBoard, self).write(vals)
        for rec in self:
            if 'ks_dashboard_menu_name' in vals:
                if self.env.ref('ks_dashboard_ninja.ks_my_default_dashboard_board') and self.env.ref(
                        'ks_dashboard_ninja.ks_my_default_dashboard_board').sudo().id == rec.id:
                    if self.env.ref('ks_dashboard_ninja.board_menu_root', False):
                        self.env.ref('ks_dashboard_ninja.board_menu_root').sudo().name = vals['ks_dashboard_menu_name']
                else:
                    rec.ks_dashboard_menu_id.sudo().name = vals['ks_dashboard_menu_name']
            if 'ks_dashboard_group_access' in vals:
                if self.env.ref('ks_dashboard_ninja.ks_my_default_dashboard_board').id == rec.id:
                    if self.env.ref('ks_dashboard_ninja.board_menu_root', False):
                        self.env.ref('ks_dashboard_ninja.board_menu_root').groups_id = vals['ks_dashboard_group_access']
                else:
                    rec.ks_dashboard_menu_id.sudo().groups_id = vals['ks_dashboard_group_access']
            if 'ks_dashboard_active' in vals and rec.ks_dashboard_menu_id:
                rec.ks_dashboard_menu_id.sudo().active = vals['ks_dashboard_active']

            if 'ks_dashboard_top_menu_id' in vals:
                rec.ks_dashboard_menu_id.write(
                    {'parent_id': vals['ks_dashboard_top_menu_id']}
                )

        return record

    @api.multi
    def unlink(self):
        if self.env.ref('ks_dashboard_ninja.ks_my_default_dashboard_board').id in self.ids:
            raise ValidationError(_("Default Dashboard can't be deleted."))
        else:
            for rec in self:
                rec.ks_dashboard_client_action_id.sudo().unlink()
                rec.ks_dashboard_menu_id.sudo().unlink()
        res = super(KsDashboardNinjaBoard, self).unlink()
        return res

    @api.model
    def ks_fetch_dashboard_data(self, ks_dashboard_id):
        self.ks_set_date(ks_dashboard_id)
        has_group_ks_dashboard_manager = self.env.user.has_group('ks_dashboard_ninja.ks_dashboard_ninja_group_manager')
        dashboard_data = {
            'name': self.browse(ks_dashboard_id).name,
            'ks_dashboard_manager': has_group_ks_dashboard_manager,
            'ks_dashboard_list': self.search_read([], ['id', 'name']),
            'ks_dashboard_start_date': self.browse(ks_dashboard_id).ks_dashboard_start_date,
            'ks_dashboard_end_date': self.browse(ks_dashboard_id).ks_dashboard_end_date,
            'ks_date_filter_selection': self.browse(ks_dashboard_id).ks_date_filter_selection,
            'ks_gridstack_config': self.browse(ks_dashboard_id).ks_gridstack_config,
            'ks_set_interval': self.browse(ks_dashboard_id).ks_set_interval,
        }

        if len(self.browse(ks_dashboard_id).ks_dashboard_items_ids) < 1:
            dashboard_data['ks_item_data'] = False
        else:
            items = self.ks_fetch_item(self.browse(ks_dashboard_id).ks_dashboard_items_ids.ids)
            dashboard_data['ks_item_data'] = items

        return dashboard_data

    @api.model
    def ks_fetch_item(self, item_list):
        """
        :rtype: object
        :param item_list: list of item ids.
        :return: {'id':[item_data]}
        """
        items = {}
        item_model = self.env['ks_dashboard_ninja.item']
        for item_id in item_list:
            item = self.ks_fetch_item_data(item_model.browse(item_id))
            items[item['id']] = item
        return items

    # fetching Item info (Divided to make function inherit easily)
    def ks_fetch_item_data(self, rec):
        """
        :rtype: object
        :param item_id: item object
        :return: object with formatted item data
        """
        item = {
            'name': rec.name if rec.name else rec.ks_model_id.name if rec.ks_model_id else "Name",
            'ks_background_color': rec.ks_background_color,
            'ks_font_color': rec.ks_font_color,
            # 'ks_domain': rec.ks_domain.replace('"%UID"', str(
            #     self.env.user.id)) if rec.ks_domain and "%UID" in rec.ks_domain else rec.ks_domain,
            'ks_domain': rec.ks_convert_into_proper_domain(rec.ks_domain,rec),
            'ks_icon': rec.ks_icon,
            'ks_model_id': rec.ks_model_id.id,
            'ks_model_name': rec.ks_model_name,
            'ks_model_display_name': rec.ks_model_id.name,
            'ks_record_count_type': rec.ks_record_count_type,
            'ks_record_count': rec.ks_record_count,
            'id': rec.id,
            'ks_layout': rec.ks_layout,
            'ks_icon_select': rec.ks_icon_select,
            'ks_default_icon': rec.ks_default_icon,
            'ks_default_icon_color': rec.ks_default_icon_color,
            # Pro Fields
            'ks_dashboard_item_type': rec.ks_dashboard_item_type,
            'ks_chart_item_color': rec.ks_chart_item_color,
            'ks_chart_groupby_type': rec.ks_chart_groupby_type,
            'ks_chart_relation_groupby': rec.ks_chart_relation_groupby.id,
            'ks_chart_relation_groupby_name': rec.ks_chart_relation_groupby.name,
            'ks_chart_date_groupby': rec.ks_chart_date_groupby,
            'ks_record_field': rec.ks_record_field.id if rec.ks_record_field else False,
            'ks_chart_data': rec.ks_chart_data,
            'ks_list_view_data': rec.ks_list_view_data,
            'ks_chart_data_count_type': rec.ks_chart_data_count_type,
            'ks_bar_chart_stacked': rec.ks_bar_chart_stacked,
            'ks_semi_circle_chart': rec.ks_semi_circle_chart,
            'ks_list_view_type': rec.ks_list_view_type,
            'ks_list_view_group_fields': rec.ks_list_view_group_fields.ids if rec.ks_list_view_group_fields else False,
            'ks_previous_period': rec.ks_previous_period,
            'ks_kpi_data': rec.ks_kpi_data,
            'ks_goal_enable': rec.ks_goal_enable,
            'ks_model_id_2': rec.ks_model_id_2.id,
            'ks_record_field_2': rec.ks_record_field_2.id,
            'ks_data_comparison': rec.ks_data_comparison,
            'ks_target_view': rec.ks_target_view,
            'ks_date_filter_selection': rec.ks_date_filter_selection,
        }
        return item

    def ks_set_date(self, ks_dashboard_id):
        ks_date_filter_selection = self.browse(ks_dashboard_id).ks_date_filter_selection

        if ks_date_filter_selection not in ['l_custom', 'l_none']:
            ks_date_data = ks_get_date(ks_date_filter_selection)

            self.browse(ks_dashboard_id).write({'ks_dashboard_end_date': ks_date_data["selected_end_date"],
                                                'ks_dashboard_start_date': ks_date_data["selected_start_date"]})

    @api.multi
    def load_previous_data(self):

        for rec in self:
            if rec.ks_dashboard_menu_id and rec.ks_dashboard_menu_id.action._table == 'ir_act_window':
                action_id = {
                    'name': rec['ks_dashboard_menu_name'] + " Action",
                    'res_model': 'ks_dashboard_ninja.board',
                    'tag': 'ks_dashboard_ninja',
                    'params': {'ks_dashboard_id': rec.id},
                }
                rec.ks_dashboard_client_action_id = self.env['ir.actions.client'].sudo().create(action_id)
                rec.ks_dashboard_menu_id.write(
                    {'action': "ir.actions.client," + str(rec.ks_dashboard_client_action_id.id)})

    # fetching Item info (Divided to make function inherit easily)
    def ks_export_item_data(self, rec):
        ks_chart_measure_field = []
        ks_chart_measure_field_2 = []
        for res in rec.ks_chart_measure_field:
            ks_chart_measure_field.append(res.name)
        for res in rec.ks_chart_measure_field_2:
            ks_chart_measure_field_2.append(res.name)

        ks_list_view_group_fields = []
        for res in rec.ks_list_view_group_fields:
            ks_list_view_group_fields.append(res.name)

        ks_goal_lines = []
        for res in rec.ks_goal_lines:
            goal_line = {
                'ks_goal_date': datetime.datetime.strftime(res.ks_goal_date, '%b %d, %Y'),
                'ks_goal_value': res.ks_goal_value
            }
            ks_goal_lines.append(goal_line)

        ks_list_view_field = []
        for res in rec.ks_list_view_fields:
            ks_list_view_field.append(res.name)
        item = {
            'name': rec.name if rec.name else rec.ks_model_id.name if rec.ks_model_id else "Name",
            'ks_background_color': rec.ks_background_color,
            'ks_font_color': rec.ks_font_color,
            'ks_domain': rec.ks_domain,
            'ks_icon': rec.ks_icon,
            'ks_id': rec.id,
            'ks_model_id': rec.ks_model_name,
            'ks_record_count': rec.ks_record_count,
            'ks_layout': rec.ks_layout,
            'ks_icon_select': rec.ks_icon_select,
            'ks_default_icon': rec.ks_default_icon,
            'ks_default_icon_color': rec.ks_default_icon_color,
            'ks_record_count_type': rec.ks_record_count_type,
            # Pro Fields
            'ks_dashboard_item_type': rec.ks_dashboard_item_type,
            'ks_chart_item_color': rec.ks_chart_item_color,
            'ks_chart_groupby_type': rec.ks_chart_groupby_type,
            'ks_chart_relation_groupby': rec.ks_chart_relation_groupby.name,
            'ks_chart_date_groupby': rec.ks_chart_date_groupby,
            'ks_record_field': rec.ks_record_field.name,
            'ks_chart_sub_groupby_type': rec.ks_chart_sub_groupby_type,
            'ks_chart_relation_sub_groupby': rec.ks_chart_relation_sub_groupby.name,
            'ks_chart_date_sub_groupby': rec.ks_chart_date_sub_groupby,
            'ks_chart_data_count_type': rec.ks_chart_data_count_type,
            'ks_chart_measure_field': ks_chart_measure_field,
            'ks_chart_measure_field_2': ks_chart_measure_field_2,
            'ks_list_view_fields': ks_list_view_field,
            'ks_list_view_group_fields': ks_list_view_group_fields,
            'ks_list_view_type': rec.ks_list_view_type,
            'ks_record_data_limit': rec.ks_record_data_limit,
            'ks_sort_by_order': rec.ks_sort_by_order,
            'ks_sort_by_field': rec.ks_sort_by_field.name,
            'ks_date_filter_field': rec.ks_date_filter_field.name,
            'ks_goal_enable': rec.ks_goal_enable,
            'ks_standard_goal_value': rec.ks_standard_goal_value,
            'ks_goal_liness': ks_goal_lines,
            'ks_date_filter_selection': rec.ks_date_filter_selection,
            'ks_item_start_date': datetime.datetime.strftime(rec.ks_item_start_date,
                                                             '%b %d, %Y') if rec.ks_item_start_date else False,
            'ks_item_end_date': datetime.datetime.strftime(rec.ks_item_end_date,
                                                           '%b %d, %Y') if rec.ks_item_end_date else False,
            'ks_date_filter_selection_2': rec.ks_date_filter_selection_2,
            'ks_item_start_date_2': datetime.datetime.strftime(rec.ks_item_start_date_2,
                                                             '%b %d, %Y') if rec.ks_item_start_date_2 else False,
            'ks_item_end_date_2': datetime.datetime.strftime(rec.ks_item_end_date_2,
                                                           '%b %d, %Y') if rec.ks_item_end_date_2 else False,
            'ks_previous_period': rec.ks_previous_period,
            'ks_target_view': rec.ks_target_view,
            'ks_data_comparison': rec.ks_data_comparison,
            'ks_record_count_type_2': rec.ks_record_count_type_2,
            'ks_record_field_2': rec.ks_record_field_2.name,
            'ks_model_id_2': rec.ks_model_id_2.model,
            'ks_date_filter_field_2': rec.ks_date_filter_field_2.name,
        }
        return item

    @api.model
    def ks_dashboard_export(self, ks_dashboard_ids):
        ks_dashboard_data = []
        ks_dashboard_export_data = {}
        ks_dashboard_ids = json.loads(ks_dashboard_ids)
        for ks_dashboard_id in ks_dashboard_ids:
            dashboard_data = {
                'name': self.browse(ks_dashboard_id).name,
                'ks_dashboard_menu_name': self.browse(ks_dashboard_id).ks_dashboard_menu_name,
                'ks_gridstack_config': self.browse(ks_dashboard_id).ks_gridstack_config,
            }
            if len(self.browse(ks_dashboard_id).ks_dashboard_items_ids) < 1:
                dashboard_data['ks_item_data'] = False
            else:
                items = []
                for rec in self.browse(ks_dashboard_id).ks_dashboard_items_ids:
                    item = self.ks_export_item_data(rec)
                    items.append(item)

                dashboard_data['ks_item_data'] = items

            ks_dashboard_data.append(dashboard_data)

            ks_dashboard_export_data = {
                'ks_file_format': 'ks_dashboard_ninja_export_file',
                'ks_dashboard_data': ks_dashboard_data
            }
        return ks_dashboard_export_data

    @api.model
    def ks_import_dashboard(self, file):
        try:
            # ks_dashboard_data = json.loads(file)
            ks_dashboard_file_read = json.loads(file)
        except:
            raise ValidationError(_("This file is not supported"))

        if 'ks_file_format' in ks_dashboard_file_read and ks_dashboard_file_read[
            'ks_file_format'] == 'ks_dashboard_ninja_export_file':
            ks_dashboard_data = ks_dashboard_file_read['ks_dashboard_data']
        else:
            raise ValidationError(_("Current Json File is not properly formatted according to Dashboard Ninja Model."))

        ks_dashboard_key = ['name', 'ks_dashboard_menu_name', 'ks_gridstack_config']
        ks_dashboard_item_key = ['ks_model_id', 'ks_chart_measure_field', 'ks_list_view_fields', 'ks_record_field',
                                 'ks_chart_relation_groupby', 'ks_id']

        # Fetching dashboard model info
        for data in ks_dashboard_data:
            if not all(key in data for key in ks_dashboard_key):
                raise ValidationError(
                    _("Current Json File is not properly formatted according to Dashboard Ninja Model."))
            vals = {
                'name': data['name'],
                'ks_dashboard_menu_name': data['ks_dashboard_menu_name'],
                'ks_dashboard_top_menu_id': self.env.ref("ks_dashboard_ninja.board_menu_root").id,
                'ks_dashboard_active': True,
                'ks_gridstack_config': data['ks_gridstack_config'],
                'ks_dashboard_default_template': self.env.ref("ks_dashboard_ninja.ks_blank").id,
                'ks_dashboard_group_access': False,

            }
            # Creating Dashboard
            dashboard_id = self.create(vals)

            if data['ks_gridstack_config']:
                ks_gridstack_config = eval(data['ks_gridstack_config'])
            ks_grid_stack_config = {}

            if data['ks_item_data']:
                # Fetching dashboard item info
                for item in data['ks_item_data']:
                    if not all(key in item for key in ks_dashboard_item_key):
                        raise ValidationError(
                            _("Current Json File is not properly formatted according to Dashboard Ninja Model."))

                    ks_model = item['ks_model_id'].replace(".", "_")

                    ks_measure_field_ids = []
                    ks_measure_field_2_ids = []

                    model = self.env['ir.model'].search([('model', '=', item['ks_model_id'])])



                    if not model:
                        raise ValidationError(_(
                            "Please Install the Module which contains the following Model : %s " % item['ks_model_id']))

                    if item['ks_model_id_2']:
                        model_2 = self.env['ir.model'].search([('model', '=', item['ks_model_id_2'])])
                        if not model_2:
                            raise ValidationError(_(
                                "Please Install the Module which contains the following Model : %s " % item['ks_model_id_2']))

                    for ks_measure in item['ks_chart_measure_field']:
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            measure_id = x + '.field_' + ks_model + "__" + ks_measure
                            ks_measure_id = self.env.ref(measure_id, False)
                            if ks_measure_id:
                                ks_measure_field_ids.append(ks_measure_id.id)
                    item['ks_chart_measure_field'] = [(6, 0, ks_measure_field_ids)]

                    for ks_measure in item['ks_chart_measure_field_2']:
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            measure_id = x + '.field_' + ks_model + "__" + ks_measure
                            ks_measure_id = self.env.ref(measure_id, False)
                            if ks_measure_id:
                                ks_measure_field_2_ids.append(ks_measure_id.id)
                    item['ks_chart_measure_field_2'] = [(6, 0, ks_measure_field_2_ids)]

                    ks_list_view_group_fields = []
                    for ks_measure in item['ks_list_view_group_fields']:
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            measure_id = x + '.field_' + ks_model + "__" + ks_measure
                            ks_measure_id = self.env.ref(measure_id, False)
                            if ks_measure_id:
                                ks_list_view_group_fields.append(ks_measure_id.id)
                    item['ks_list_view_group_fields'] = [(6, 0, ks_list_view_group_fields)]

                    ks_list_view_field_ids = []
                    for ks_list_field in item['ks_list_view_fields']:
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            list_field_id = x + '.field_' + ks_model + "__" + ks_list_field
                            ks_list_field_id = self.env.ref(list_field_id, False)
                            if ks_list_field_id:
                                ks_list_view_field_ids.append(ks_list_field_id.id)
                    item['ks_list_view_fields'] = [(6, 0, ks_list_view_field_ids)]

                    if item['ks_record_field']:
                        ks_record_field = item['ks_record_field']
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            record_id = x + '.field_' + ks_model + "__" + ks_record_field
                            ks_record_id = self.env.ref(record_id, False)
                            if ks_record_id:
                                item['ks_record_field'] = ks_record_id.id

                    if item['ks_date_filter_field']:
                        ks_date_filter_field = item['ks_date_filter_field']
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            record_id = x + '.field_' + ks_model + "__" + ks_date_filter_field
                            ks_record_id = self.env.ref(record_id, False)
                            if ks_record_id:
                                item['ks_date_filter_field'] = ks_record_id.id



                    if item['ks_chart_relation_groupby']:
                        ks_group_by = item['ks_chart_relation_groupby']
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            field_id = x + '.field_' + ks_model + "__" + ks_group_by
                            ks_chart_relation_groupby = self.env.ref(field_id, False)
                            if ks_chart_relation_groupby:
                                item['ks_chart_relation_groupby'] = ks_chart_relation_groupby.id

                    if item['ks_chart_relation_sub_groupby']:
                        ks_group_by = item['ks_chart_relation_sub_groupby']
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            field_id = x + '.field_' + ks_model + "__" + ks_group_by
                            ks_chart_relation_sub_groupby = self.env.ref(field_id, False)
                            if ks_chart_relation_sub_groupby:
                                item['ks_chart_relation_sub_groupby'] = ks_chart_relation_sub_groupby.id

                    # Sort by field : Many2one Entery
                    if item['ks_sort_by_field']:
                        ks_group_by = item['ks_sort_by_field']
                        for x in self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).modules.split(", "):
                            field_id = x + '.field_' + ks_model + "__" + ks_group_by
                            ks_sort_by_field = self.env.ref(field_id, False)
                            if ks_sort_by_field:
                                item['ks_sort_by_field'] = ks_sort_by_field.id

                    ks_model_id = self.env['ir.model'].search([('model', '=', item['ks_model_id'])]).id
                    if(item['ks_model_id_2']):
                        ks_model_2 = item['ks_model_id_2'].replace(".", "_")
                        ks_model_id_2 = self.env['ir.model'].search([('model', '=', item['ks_model_id_2'])]).id
                        if item['ks_record_field_2']:
                            ks_record_field = item['ks_record_field_2']
                            for x in self.env['ir.model'].search([('model', '=', item['ks_model_id_2'])]).modules.split(
                                    ", "):
                                record_id = x + '.field_' + ks_model_2 + "__" + ks_record_field
                                ks_record_id = self.env.ref(record_id, False)
                                if ks_record_id:
                                    item['ks_record_field_2'] = ks_record_id.id
                        if item['ks_date_filter_field_2']:
                            ks_date_filter_field = item['ks_date_filter_field_2']
                            for x in self.env['ir.model'].search([('model', '=', item['ks_model_id_2'])]).modules.split(
                                    ", "):
                                record_id = x + '.field_' + ks_model_2 + "__" + ks_date_filter_field
                                ks_record_id = self.env.ref(record_id, False)
                                if ks_record_id:
                                    item['ks_date_filter_field_2'] = ks_record_id.id
                        item['ks_model_id_2'] = ks_model_id_2
                    else:
                        item['ks_date_filter_field_2'] = False
                        item['ks_record_field_2'] = False

                    item['ks_model_id'] = ks_model_id
                    item['ks_dashboard_ninja_board_id'] = dashboard_id.id

                    ks_goal_lines = item['ks_goal_liness'].copy() if item.get('ks_goal_liness', False) else False
                    item['ks_goal_liness'] = False

                    item['ks_item_start_date'] = datetime.datetime.strptime(item['ks_item_start_date'], '%b %d, %Y') if \
                    item[
                        'ks_item_start_date'] else False
                    item['ks_item_end_date'] = datetime.datetime.strptime(item['ks_item_end_date'], '%b %d, %Y') if \
                    item[
                        'ks_item_end_date'] else False
                    item['ks_item_start_date_2'] = datetime.datetime.strptime(item['ks_item_start_date_2'], '%b %d, %Y') if \
                    item[
                        'ks_item_start_date_2'] else False
                    item['ks_item_end_date_2'] = datetime.datetime.strptime(item['ks_item_end_date_2'], '%b %d, %Y') if \
                    item[
                        'ks_item_end_date_2'] else False

                    # Creating dashboard items
                    ks_item = self.env['ks_dashboard_ninja.item'].create(item)
                    if ks_goal_lines and len(ks_goal_lines) != 0:
                        for line in ks_goal_lines:
                            line['ks_goal_date'] = datetime.datetime.strptime(line['ks_goal_date'], '%b %d, %Y')
                            line['ks_dashboard_item'] = ks_item.id
                            self.env['ks_dashboard_ninja.item_goal'].create(line)
                    if data['ks_gridstack_config'] and str(item['ks_id']) in ks_gridstack_config:
                        ks_grid_stack_config[str(ks_item.id)] = ks_gridstack_config[str(item['ks_id'])]

                self.browse(dashboard_id.id).write({
                    'ks_gridstack_config': json.dumps(ks_grid_stack_config)
                })

        return "Success"


class KsDashboardNinjaTemplate(models.Model):
    _name = 'ks_dashboard_ninja.board_template'

    name = fields.Char()
    ks_gridstack_config = fields.Char()
    ks_item_count = fields.Integer()
