# -*- coding: utf-8 -*-
from odoo import http

# class ProjectShowMilestone(http.Controller):
#     @http.route('/project_show_milestone/project_show_milestone/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_show_milestone/project_show_milestone/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_show_milestone.listing', {
#             'root': '/project_show_milestone/project_show_milestone',
#             'objects': http.request.env['project_show_milestone.project_show_milestone'].search([]),
#         })

#     @http.route('/project_show_milestone/project_show_milestone/objects/<model("project_show_milestone.project_show_milestone"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_show_milestone.object', {
#             'object': obj
#         })