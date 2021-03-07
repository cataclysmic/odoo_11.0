# -*- coding: utf-8 -*-
{
    'name': "piece_accounting",

    'summary': """
        Ermöglicht die Kalkulation von Arbeitsstunden gegeben einer Fallzahl""",

    'description': """
        Long description of module's purpose
    """,

    'author': "StaLA Sachsen-Anhalt",
    'website': "hobby",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','hr_timesheet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
