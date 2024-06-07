# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Career Portal',
    'version': '1.0',
    'category': 'Portal',
    'sequence': 15,
    'summary': 'Portal',
    'description': "",
    'website': 'https://www.odoo.com/page/Portal',
    'depends': ['career_planing', 'portal'],
    'data': [
        "views/portal_template.xml",

    ],
    'demo': [

    ],
    # 'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False
}
