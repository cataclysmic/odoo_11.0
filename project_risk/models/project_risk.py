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
    4: 'minimal',
    3: 'spürbar',
    2: 'beeinträchtigen',
    1: 'extrem'
}

RATING = [
            (1,'I'),
            (2,'II'),
            (3,'III'),
            (4,'IV'),
            (5,'V'),
            (6,'VI')
        ]

CHANGE = [
    (1,'erhöht'),
    (2,'unverändert'),
    (3,'vermindert')
]

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

    rating = fields.Selection( # Selection field?
        selection=RATING,
        compute='_compute_rating',
        store=True,
        string="Klasse"
    )

    #rating = fields.Integer(string="Risikoklasse")

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

    risk_class = fields.Many2one(comodel_name="project.task.milestonetype",
                                 string="MS-Bezug")

    tags = fields.Many2many(related='project_task_ids.tag_ids',string="Stichwörter")

    probclass_history = fields.Html(compute="_probclasshist", string="Änderung",
                                    store=True)

    probclass = fields.Integer(compute='_probclass', store=True,string="Matrix-Code")

    risk_history = fields.Boolean(compute='_probclass', string="Vorgänger",
                                  store=True, track_visibility='onchange')

    rating_history = fields.Selection(string="Risikoänderung",
                                    selection = CHANGE,
                                    compute='_probclasshist',
                                    store = True
    )

    risk_cat_icon = fields.Html(compute="_compute_rating", string='Klasse',
                                store=True)

    @api.multi
    @api.depends('probability', 'impact')
    def _compute_rating(self):
        for risk in self:
            risk.probclass = risk.probability + risk.impact

            risk.risk_history = True

            if risk.probability == 50:
                risk.rating = 6
                risk.risk_cat_icon = '<div id="riskcat" style="background:#892ca0;font-weight:bold;text-align:center;color:white;"> ' + RATING[risk.rating-1][1] + ' </div>'
            elif risk.probclass in (31,42,41):
                risk.rating = 5
                risk.risk_cat_icon = '<div id="riskcat" style="background:#d35f5f;font-weight:bold;text-align:center;"> ' + RATING[risk.rating-1][1] + ' </div>'
            elif risk.probclass in (21,32,43):
                risk.rating = 4
                risk.risk_cat_icon = '<div id="riskcat" style="background:#ff9955;font-weight:bold;text-align:center;"> ' + RATING[risk.rating-1][1] + ' </div>'
            elif risk.probclass in (11,22,33,44):
                risk.rating = 3
                risk.risk_cat_icon = '<div id="riskcat" style="background:#ffdd55;font-weight:bold;text-align:center;"> ' + RATING[risk.rating-1][1] + ' </div>'
            elif risk.probclass in (12,23,34):
                risk.rating = 2
                risk.risk_cat_icon = '<div id="riskcat" style="background:#87deaa;font-weight:bold;text-align:center;"> ' + RATING[risk.rating-1][1] + ' </div>'
            elif risk.probclass in (14,13,24):
                risk.rating = 1
                risk.risk_cat_icon = '<div id="riskcat" style="background:#2ca05a;font-weight:bold;text-align:center;color:white;"> ' + RATING[risk.rating-1][1] + ' </div>'

    @api.onchange('probability', 'impact')
    def _probclasshist(self):
        if self._origin:
            if self._origin.rating:
                rating_origin = self._origin.rating
                for rec in self:
                    if rec.rating > rating_origin:
                        rec.probclass_history = '<div id="riskhist" style="color:red;">erhöht</div>'
                        rec.rating_history = 1
                    elif rec.rating < rating_origin:
                        rec.probclass_history = '<div id="riskhist" style="color:green;">vermindert</div>'
                        rec.rating_history = 3
                    else:
                        rec.probclass_history = '<div id="riskhist">unverändert</div>'
                        rec.rating_history = 2


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
