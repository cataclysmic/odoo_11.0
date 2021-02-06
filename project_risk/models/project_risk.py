# Copyright 2019 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

PROBABILITY = [
    (10, '<=25%'),
    (20, '<=50%'),
    (30, '>50%'),
    (40, '>=75%'),
    (50, '100%')
]

IMPACT = {
    1: '1 - minimal',
    2: '2 - spürbar',
    3: '3 - beeinträchtigen',
    4: '4 - extrem'
}

class ProjectRisk(models.Model):
    _inherit = ['mail.thread']
    _name = 'project.risk'
    _description = 'Project Risk'

    #project_id = fields.Many2one(
    #    compute ='_compute_project',
    #)

    project_task_ids = fields.Many2many(
        comodel_name='project.task',
        required=True
    )

    project_risk_category_id = fields.Many2one(
        string='Kategorie',
        comodel_name='project.risk.category',
        required=True,
    )

    name = fields.Char(
        string="Bezeichnung",
        required=1
    )

    description = fields.Html()

    probability = fields.Selection(
        required=True,
        selection=PROBABILITY,
        track_visibility='onchange',
        string="Wahrscheinlichkeit"
    )

    impact = fields.Selection(
        required=True,
        selection=list(IMPACT.items()),
        track_visibility='onchange',
        string="Auswirkung"
    )

    rating = fields.Char( # Selection field?
        compute='_compute_rating',
        store=True,
        string="Klasse"
    )

    active = fields.Boolean(default=True)

    project_risk_response_category_id = fields.Many2one(
        comodel_name='project.risk.response.category',
        string='Steuerungstrategie'
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Geplant'),
            ('active', 'In Arbeit'),
            ('closed', 'Beendet')
        ],
        default='draft',
        track_visibility='onchange'
    )

    owner_id = fields.Many2one(
        string='Verantwortlicher',
        comodel_name='res.users',
        track_visibility='onchange'
    )

    project_task_response_ids = fields.Many2many(
        string='Gegenmaßnahme',
        comodel_name='project.task',
    )

    tags = fields.Many2many(related='project_task_ids.tag_ids')

    probclass_history = fields.Html(compute="_probclasshist", string="Änderung",
                                    store=True)

    probclass = fields.Integer(compute='_probclass', store=True)

    risk_history = fields.Boolean(compute='_probclass', string="Risikohistorie",
                                  store=True, track_visibility='onchange')

    risk_cat_icon = fields.Html(compute="_compute_rating", string='Klasse',
                                store=True)

    @api.multi
    @api.depends('probability', 'impact')
    def _compute_rating(self):
        for risk in self:
            risk.probclass = risk.probability + risk.impact

            risk.risk_history = True

            if risk.probability == 50:
                risk.rating = 'VI'
                risk.risk_cat_icon = '<div id="riskcat" style="background:#892ca0;font-weight:bold;text-align:center;color:white;"> ' + str(risk.rating) + ' </div>'

            elif risk.probclass in (34,43,44):
                risk.rating = 'V'
                risk.risk_cat_icon = '<div id="riskcat" style="background:#d35f5f;font-weight:bold;text-align:center;"> ' + str(risk.rating) + ' </div>'
            elif risk.probclass in (24,33,42):
                risk.rating = 'IV'
                risk.risk_cat_icon = '<div id="riskcat" style="background:#ff9955;font-weight:bold;text-align:center;"> ' + str(risk.rating) + ' </div>'
            elif risk.probclass in (14,23,32,14):
                risk.rating = 'III'
                risk.risk_cat_icon = '<div id="riskcat" style="background:#ffdd55;font-weight:bold;text-align:center;"> ' + str(risk.rating) + ' </div>'
            elif risk.probclass in (13,22,31):
                risk.rating = 'II'
                risk.risk_cat_icon = '<div id="riskcat" style="background:#87deaa;font-weight:bold;text-align:center;"> ' + str(risk.rating) + ' </div>'
            elif risk.probclass in (11,12,21):
                risk.rating = 'I'
                risk.risk_cat_icon = '<div id="riskcat" style="background:#2ca05a;font-weight:bold;text-align:center;color:white;"> ' + str(risk.rating) + ' </div>'

    @api.onchange('probability', 'impact')
    def _probclasshist(self):
        if self._origin:
            if self._origin.probability:
                prob_origin = self._origin.probability
                for rec in self:
                    if rec.probability > prob_origin:
                        rec.probclass_history = '<div id="riskhist" style="color:red;">erhöht</div>'
                    elif rec.probability < prob_origin:
                        rec.probclass_history = '<div id="riskhist" style="color:green;">vermindert</div>'


    @api.multi
    def write(self, vals):
        res = super(ProjectRisk, self).write(vals)
        if vals.get("owner_id"):
            self.message_subscribe_users(user_ids=[vals.get("owner_id")])
        return res

    @api.model
    def create(self, vals):
        res = super(ProjectRisk, self).create(vals)
        res.message_subscribe_users(user_ids=[
            res.owner_id.id
        ])
        return res
