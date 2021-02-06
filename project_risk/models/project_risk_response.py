# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProjectRiskResponse(models.Model):
    _name = 'project.risk.response'

    project_risk_id = fields.Many2one(
        comodel_name='project.risk.response'
    )

    sequence = fields.Integer()

    name = fields.Char(string='Bezeichnung')

    description = fields.Char(string='Beschreibung')

    create_date = fields.Date(string='Erstellt am',
                              compute='_compute_create_date',
                              store=True)

    l
