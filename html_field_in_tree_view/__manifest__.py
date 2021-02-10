# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HTML field in Tree View',
    'version': '1.1',
    'category': 'Web',
    'summary': 'User interface in Tree view',
    'description': """
        This module use for dispaly HTML filed without html tags on Tree view table.
    """,
    'author':'SprintErp',
    'website':'sprinterp.com',
    'depends': ['base','web'],
    'data': [
        'views/asset_backend.xml',
    ],
    'installable': True,
    'auto_install': True,
}
