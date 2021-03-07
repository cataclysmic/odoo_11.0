{
    'name': 'Project Risk',
    'summary': 'MOR risk management method',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/project',
    'category': 'Project Management',
    'version': '11.0.1.0.0',
    'depends': [
        'base',
        'project',
        'project_show_milestone',
        'html_field_in_tree_view',
        'piece_accounting'
    ],
    'data': [
        'security/ir_model_access.xml',

        'data/project_risk_response_category_data.xml',
        'data/project_risk_category_data.xml',

        'views/project_risk_response_category_view.xml',
        'views/project_risk_category_view.xml',
        'views/project_risk_view.xml',
        'views/project_risk_task_view.xml',

        'menuitems.xml',

        'views/css.xml',
    ],
    'installable': True,
}
