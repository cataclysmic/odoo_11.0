# -*- coding: utf-8 -*-

from odoo import models, fields, api

class project_show_milestone(models.Model):
    _inherit = 'project.task'

    milestonetype_id = fields.Many2one('project.task.milestonetype',
                                    string="Meilensteinklasse")

    ms_color = fields.Char(related="milestonetype_id.ms_color")

    ms_icon = fields.Html(related="milestonetype_id.ms_icon")

    date_deadline = fields.Date(string='Deadline', index=True, copy=False, track_visibility="onchange")


    @api.onchange('date_deadline')
    def _set_msdate(self):
        for rec in self:
            if rec.milestonetype_id:
                self.date_start = str(rec.date_deadline) + ' 18:00:00'
                self.date_end = str(rec.date_deadline) + ' 18:00:00'

    @api.onchange('milestonetype_id')
    def _set_milestone(self):
        for rec in self:
            if rec.milestonetype_id:
                self.is_milestone = True
            else:
                self.is_milestone = False

class project_task_milestonetypes(models.Model):
    _name = 'project.task.milestonetype'

    name = fields.Char(string="Bezeichnung")

    description = fields.Char(string="Beschreibung")

    ms_color = fields.Char(string="Kanbanfarbe")

    ms_icon = fields.Html(string="MS", compute = '_create_icon', store = True)

    @api.depends('ms_color')
    def _create_icon(self):
        for rec in self:
            rec.ms_icon = '<div id="mssymb" style="transform: rotate(45deg); width:12px; height:12px;background:' + str(rec.ms_color) + ';"></div>'
