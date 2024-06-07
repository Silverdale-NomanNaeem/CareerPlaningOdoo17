# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Career Planning',
    'version': '1.0',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'description': "",
    'depends': ['mail', 'base', 'hr_recruitment', 'website_slides', 'xlsx_reporting','hr'],
    'data': [
        "security/ir.model.access.csv",
        "security/group.xml",
        "security/record_rules.xml",
        'data/mail_template_data.xml',
        "views/menu.xml",
        "views/job_listing_views.xml",
        "views/job_application_views.xml",
        "views/training_program_view.xml",
        "views/training_program_report.xml",
        "views/questions.xml",
        "report/xlsx_report.xml",
        "views/summry.xml",
        "views/quiz_response.xml",
        "views/quiz_response_line.xml",
        "views/company_view.xml",
        "views/quiz.xml",
        "views/questions_option.xml",
        "views/goals_view.xml",
        "views/course_view.xml",
        "views/feedback_view.xml",
        "views/employee_view.xml",
        "views/report_employee_resume_template.xml",
        "views/career_path_view.xml",
        "views/skills_view.xml",
        "views/career_plan_view.xml",
        "views/Perfromance_review.xml",
        "views/career_ask_view.xml",
        "views/career_ml_view.xml",
    ],
    'demo': [
    ],
    'assets': {

    },
    'installable': True,
    'application': True,
    'auto_install': False
}
