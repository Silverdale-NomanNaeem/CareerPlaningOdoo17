from odoo import models, fields , api
from dateutil.relativedelta import relativedelta
class TrainingProgram(models.Model):
    _name = 'training.program'
    _description = 'Training Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "title"

    title = fields.Char(string='Title')
    description = fields.Text(string='Description')
    duration = fields.Integer(string='Duration (in days)',compute='_compute_duration')
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)
    cost = fields.Monetary(string="Cost", currency_field='currency_id', tracking=True)
    # cost = fields.Float(string='Cost')
    location = fields.Char(string='Location')
    employees_attending = fields.Many2many('employee.profile', string='Employees Attending')
    skills_covered = fields.Many2many('employee.skill', string='Skills Covered')
    start_date = fields.Date(string='StartDate')
    end_date = fields.Date(string='EndDate')
    def _get_report_values(self, docids, data=None):
        docs = self.env['training.program'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'training.program',
            'docs': docs,
        }
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                delta = rec.end_date - rec.start_date
                rec.duration = delta.days
            else:
                rec.duration = 0
class Skill(models.Model):
    _name = 'employee.skill'
    _description = 'Skill'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Skill')
    description = fields.Text(string='Description')
    color = fields.Integer(string="Color", )
    color_2 = fields.Char(string="Color 2", )


class Course(models.Model):
    # _name = 'training.course'
    _inherit = "slide.channel"

    skills = fields.Many2many('employee.skill', string='Skills Covered')
    employee_id = fields.Many2many('employee.profile','course_id',string="Employee")
#     invoice_id = fields.One2many('account.move', string='Invoice')
#
# class Invoice(models.Model):
#     _inherit = 'account.move'
#
#     course_id = fields.Many2one("slide.channel","Course")
#
