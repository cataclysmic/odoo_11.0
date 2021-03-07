# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PieceAccounting(models.Model):
     _inherit = 'project.task'

     pieces_total = fields.Integer(string="Fallzahl (gesamt)")

     pieces_done = fields.Integer(string="Fallzahl (erledigt)", default="0")

     piece_time = fields.Integer(string="Bearbeitungszeit pro Fall in Min.")

     fortschritt = fields.Float(string="Fortschritt", default="0", digits=(4,1))

     @api.onchange('piece_time')
     def _total_time_estim(self):
         if self.piece_time and self.pieces_total:
            self.planned_hours = float((self.pieces_total * self.piece_time)/60)


     @api.onchange('pieces_done')
     def _pieces_fortschritt(self):
          if self.pieces_total and self.pieces_done:
               self.fortschritt = (self.pieces_done / float(self.pieces_total)) * 100
