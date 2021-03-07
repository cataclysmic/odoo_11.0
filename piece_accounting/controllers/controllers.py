# -*- coding: utf-8 -*-
from odoo import http

# class PieceAccounting(http.Controller):
#     @http.route('/piece_accounting/piece_accounting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/piece_accounting/piece_accounting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('piece_accounting.listing', {
#             'root': '/piece_accounting/piece_accounting',
#             'objects': http.request.env['piece_accounting.piece_accounting'].search([]),
#         })

#     @http.route('/piece_accounting/piece_accounting/objects/<model("piece_accounting.piece_accounting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('piece_accounting.object', {
#             'object': obj
#         })