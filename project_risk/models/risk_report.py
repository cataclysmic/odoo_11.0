# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class RiskXlsx(models.AbstractModel):
    _name = 'report.project_risk.risks_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, tasks):
        imgpath = "/mnt/extra-addons/"
        sheet = workbook.add_worksheet('Risiken')
        sheetdash = workbook.add_worksheet('Dashboard')
        sheethist = workbook.add_worksheet('Historie')
        row = 0
        col = 0
        sheetheader = workbook.add_format({'bold': True, 'font_size':13})
        sheet.write(row, col, 'Zensus 2021 - Projekt : Risiken', sheetheader)

        dgreen = workbook.add_format({'bold': True, 'bg_color':'#2ca05a', 'font_size':11, 'align':'center', 'valign':'center'})
        lgreen = workbook.add_format({'bold': True, 'bg_color':'#87deaa', 'font_size':11, 'align':'center', 'valign':'center'})
        yellow = workbook.add_format({'bold': True, 'bg_color':'#ffdd55', 'font_size':11, 'align':'center', 'valign':'center'})
        orange = workbook.add_format({'bold': True, 'bg_color':'#ff9955', 'font_size':11, 'align':'center', 'valign':'center'})
        red    = workbook.add_format({'bold': True, 'bg_color':'#d35f5f', 'font_size':11, 'align':'center', 'valign':'center'})
        violet = workbook.add_format({'bold': True, 'bg_color':'#892ca0', 'font_size':11, 'align':'center', 'valign':'center'})

        header = workbook.add_format({'bold': True, 'font_size':11})
        tabhead = workbook.add_format({'bold':True, 'font_size':11, }) # rotate text
        tabhead.set_rotation(90)

        # list title
        row = 3
        sheet.write(row, 1, "Teilprojekt", header)
        sheet.write(row, 2, "Aufgabe", header)
        sheet.write(row, 3, "Deadline", header)
        sheet.write(row, 4, "Ursache", header)
        sheet.write(row, 5, "Primäre Auswirkung", header)
        sheet.write(row, 6, "(A)", header)
        sheet.write(row, 7, "(P)", header)
        sheet.write(row, 8, "Änderung", header)
        sheet.write(row, 9, "Beschreibung", header)
        sheet.write(row, 10, "Gegenmaßnahmen", header)

        # list content
        risk_matrix = {
            11:0, 21:0, 31:0, 41:0, 51:0,
            12:0, 22:0, 32:0, 42:0, 52:0,
            13:0, 23:0, 33:0, 43:0, 53:0,
            14:0, 24:0, 34:0, 44:0, 54:0,
        }

        upsamedown = {-1 : 0, 0 : 0, 1 : 0}  #dictionary for changes

        row += 1
        sortedtasks = tasks.sorted(key=lambda x: x.probclass, reverse=True)
        for el in sortedtasks:
            if el.probclass != 0:  # checking that probclass exists
                if el.probclass in (11, 12, 21):
                    sheet.write(row, col, " ", dgreen)
                elif el.probclass in (13, 22, 31):
                    sheet.write(row, col, " ", lgreen)
                elif el.probclass in (14, 23, 32, 41):
                    sheet.write(row, col, " ", yellow)
                elif el.probclass in (24, 33, 43):
                    sheet.write(row, col, " ", orange)
                elif el.probclass in (34, 43, 44):
                    sheet.write(row, col, " ", red)
                elif el.probclass > 50:
                    sheet.write(row, col, " ", violet)
                col += 1
                sheet.write(row, col, el.project_id.name)
                col += 1
                sheet.write(row, col, el.name)
                col += 1
                sheet.write(row, col, el.date_deadline)
                col += 1
                sheet.write(row, col, el.risk_cause)
                col += 1
                sheet.write(row, col, el.impact_type)
                col += 1
                sheet.write(row, col, el.impact)
                col += 1
                sheet.write(row, col, el.probability)
                col += 1
                if el.probclass_history > 0:
                    sheet.insert_image(row, col, imgpath + 'risk_matrix/static/img/arrowup.png',
                                       {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
                elif el.probclass_history < 0:
                    sheet.insert_image(row, col, imgpath + 'risk_matrix/static/img/arrowdown.png',
                                       {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
                else:
                    sheet.insert_image(row, col, imgpath + 'risk_matrix/static/img/arrowsame.png',
                                       {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
                col += 1
                sheet.write(row, col, el.risk_description)
                col += 1
                sheet.write(row, col, el.counter_measure)
                col = 0
                row += 1

                risk_matrix[el.probclass] = risk_matrix[el.probclass] + 1

                # dashboard
                upsamedown[el.probclass_history] = upsamedown[el.probclass_history] + 1


                # history sheet
                histrow = 0
                histcol = 0
                sheethist.write(histrow, histcol, "Aufgabe", header)
                histcol += 1
                sheethist.write(histrow, histcol, "Risikomelder", header)
                histcol += 1
                sheethist.write(histrow, histcol, "Datum", header)
                histcol += 1
                sheethist.write(histrow, histcol, "Log", header)

                for msg in el.message_ids:
                    if msg.message_type == 'notification' and el.risk_history == True:
                        histrow += 1
                        histcol = 0
                        sheethist.write(histrow, histcol, el.name)
                        histcol += 1
                        sheethist.write(histrow, histcol, msg.email_from)
                        histcol += 1
                        sheethist.write(histrow, histcol, msg.date)
                        histcol += 1
                        for msgvals in msg.sudo().tracking_value_ids:
                            if msgvals.new_value_char:
                                field_value = msgvals.new_value_char
                            elif msgvals.new_value_datetime:
                                field_value = msgvals.new_value_datetime
                            elif msgvals.new_value_float:
                                field_value = msgvals.new_value_float
                            elif msgvals.new_value_integer:
                                field_value = msgvals.new_value_integer
                            elif msgvals.new_value_monetary:
                                field_value = msgvals.new_value_monetary
                            elif msgvals.new_value_text:
                                field_value = msgvals.new_value_text
                            sheethist.write(histrow, histcol, str(msgvals.field_desc) + ': ' + str(field_value))
                            histcol += 1


        ## dashboard sheet
        sheetdash.write(0, 0, 'Projektrisiken Überblick', sheetheader)
        date_time = datetime.now()
        sheetdash.write(0, 6, "Exportdatum:")
        formatdate = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        sheetdash.write_datetime(0, 7, date_time, formatdate)

        ## --- changes
        sheetdash.write(3, 1, "Änderungen kumuliert", header)
        sheetdash.insert_image(2, 2, imgpath + 'risk_matrix/static/img/arrowup.png',
                           {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
        sheetdash.write(3, 2, upsamedown[1], header)
        sheetdash.insert_image(2, 3, imgpath + 'risk_matrix/static/img/arrowsame.png',
                           {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
        sheetdash.write(3, 3, upsamedown[0], header)
        sheetdash.insert_image(2, 4, imgpath + 'risk_matrix/static/img/arrowdown.png',
                           {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
        sheetdash.write(3, 4, upsamedown[-1], header)

        ## --- risk matrix
        sheetdash.write(5, 0, "Auswirkung (A)", header)
        # extrem row
        sheetdash.write(6, 0, "4 - extrem")
        sheetdash.write(6, 1, risk_matrix[14], yellow)
        sheetdash.write(6, 2, risk_matrix[24], orange)
        sheetdash.write(6, 3, risk_matrix[34], red)
        sheetdash.write(6, 4, risk_matrix[44], red)
        sheetdash.write(6, 5, risk_matrix[54], violet)
        # beeinträchtigend row
        sheetdash.write(7, 0, "3 - beeinträchtigend")
        sheetdash.write(7, 1, risk_matrix[13], lgreen)
        sheetdash.write(7, 2, risk_matrix[23], yellow)
        sheetdash.write(7, 3, risk_matrix[33], orange)
        sheetdash.write(7, 4, risk_matrix[43], red)
        sheetdash.write(7, 5, risk_matrix[53], violet)
        # spürbar row
        sheetdash.write(8, 0, "2 - spürbar")
        sheetdash.write(8, 1, risk_matrix[12], dgreen)
        sheetdash.write(8, 2, risk_matrix[22], lgreen)
        sheetdash.write(8, 3, risk_matrix[32], yellow)
        sheetdash.write(8, 4, risk_matrix[42], orange)
        sheetdash.write(8, 5, risk_matrix[52], violet)
        # beeinträchtigend row
        sheetdash.write(9, 0, "1 - minimal")
        sheetdash.write(9, 1, risk_matrix[11], dgreen)
        sheetdash.write(9, 2, risk_matrix[21], dgreen)
        sheetdash.write(9, 3, risk_matrix[31], lgreen)
        sheetdash.write(9, 4, risk_matrix[41], yellow)
        sheetdash.write(9, 5, risk_matrix[51], violet)
        # x-axis
        sheetdash.write(10, 1, "0<x<=25")
        sheetdash.write(10, 2, "25<x<=50")
        sheetdash.write(10, 3, "50<x<=75")
        sheetdash.write(10, 4, "75<x<100")
        sheetdash.write(10, 5, "100")
        # x-axis label
        sheetdash.write(11, 1, "Eintrittswahrscheinlichkeit (P)", header)

        row = 14
        col = 0
        sheetdash.write(row, 0, "Top 10 - Risiken", header)
        row += 1
        sheetdash.write(row, 1, "Änderung", header)
        sheetdash.write(row, 2, "Teilprojekt", header)
        sheetdash.write(row, 3, "Aufgabe", header)
        sheetdash.write(row, 4, "(A)", header)
        sheetdash.write(row, 5, "(P)", header)
        sheetdash.write(row, 6, "Beschreibung", header)
        row += 1

        sortedtasks = tasks.sorted(key=lambda x: x.probclass, reverse=True)
        count = 0
        for el in sortedtasks:
            if count > 9:
                break  # 10 risks
            if el.probclass != 0:  # checking that probclass exists
                if el.probclass in (11, 12, 21):
                    sheetdash.write(row, col, " ", dgreen)
                elif el.probclass in (13, 22, 31):
                    sheetdash.write(row, col, " ", lgreen)
                elif el.probclass in (14, 23, 32, 41):
                    sheetdash.write(row, col, " ", yellow)
                elif el.probclass in (24, 33, 43):
                    sheetdash.write(row, col, " ", orange)
                elif el.probclass in (34, 43, 44):
                    sheetdash.write(row, col, " ", red)
                elif el.probclass > 50:
                    sheetdash.write(row, col, " ", violet)
                col += 1
                if el.probclass_history > 0:
                    sheetdash.insert_image(row, col, imgpath + 'risk_matrix/static/img/arrowup.png',
                                       {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
                elif el.probclass_history < 0:
                    sheetdash.insert_image(row, col, imgpath + 'risk_matrix/static/img/arrowdown.png',
                                       {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
                else:
                    sheetdash.insert_image(row, col, imgpath + 'risk_matrix/static/img/arrowsame.png',
                                       {'x_scale':2, 'y_scale': 2, 'x_offset': 30})
                col += 1
                sheetdash.write(row, col, el.project_id.name)
                col += 1
                sheetdash.write(row, col, el.name)
                col += 1
                sheetdash.write(row, col, el.impact)
                col += 1
                sheetdash.write(row, col, el.probability)
                col += 1
                sheetdash.write(row, col, el.risk_description)
                col = 0
                row += 1

