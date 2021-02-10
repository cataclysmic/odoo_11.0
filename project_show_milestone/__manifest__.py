# -*- coding: utf-8 -*-
{
    'name': "project_show_milestone",

    'summary': """
    Define different Type of milestones and colorize the kanban view accordingly.
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Felix Albrecht",
    'website': "http://",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project','mail','project_native'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'security/security.xml',
        'views/views.xml',
        'views/javascript.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
