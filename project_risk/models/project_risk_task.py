# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.task'

    project_risk_ids = fields.Many2many(
        comodel_name='project.risk',
        inverse_name='project_task_ids'
    )


