from odoo import models, fields, api, _
from datetime import date
from dateutil import relativedelta
import re
from odoo.exceptions import ValidationError


class EmployeeProfile(models.Model):
    _name = 'employee.profile'
    _description = 'Employee Profile'
    # inherit this for chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']
    email_regex = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    phone_number_regex = r'^(\+?\d{1,2}\s?)?\d{3}\d{3}\d{4}$'

    name = fields.Char(string='Name', required=True, tracking=True)
    job_title = fields.Char(string='Job Title', tracking=True)
    # department = fields.Char(string='Department',tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True, default="male")
    email = fields.Char(string='Email', tracking=True, required=True)
    phone_number = fields.Char(string='Phone Number', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    joining_date = fields.Date(string='Joining Date', tracking=True)
    education = fields.Text(string='Education', tracking=True)
    skill_id = fields.Many2many('employee.skill', tracking=True, string="Skills")
    career_plans = fields.One2many('career.plan', 'employee', string='Career Plans', tracking=True)
    image = fields.Binary(string='Image', tracking=True)
    # age = fields.Integer(string="Age", tracking=True,search='_search_age' ,compute='_compute_age', inverse='_inverse_compute_age')
    age = fields.Integer(string="Age", tracking=True, compute='_compute_age', inverse='_inverse_compute_age',
                         store=True)
    goal_id = fields.Many2many('career.goal', string="Goals", tracking=True)
    job_id = fields.Many2one('hr.job', 'Job Position', tracking=True)
    department_id = fields.Many2one('hr.department', 'Department', tracking=True)
    color = fields.Integer(string="Color")
    feedback_id = fields.Many2one('employee.feedback', string="Feedback")
    course_id = fields.Many2many("slide.channel", 'employee_id',string='Courses')


    def _get_report_base_filename(self):
        return self.name
    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    @api.constrains('joining_date')
    def check_joining_date(self):
        for rec in self:
            if rec.joining_date and rec.joining_date >= fields.Date.today():
                raise ValidationError(_("Entered date of joining is not acceptable"))

    @api.constrains('date_of_birth')
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth >= fields.Date.today():
                raise ValidationError(_("Entered date of birth is not acceptable"))

    # validating email
    # overriding default create method

    @api.model
    def create(self, vals):
        if 'email' in vals:
            if not re.match(self.email_regex, vals['email']):
                raise ValidationError('Not a valid email ID')
        if 'phone_number' in vals:
            if not re.match(self.phone_number_regex, vals['phone_number']):
                raise ValidationError('Not a valid Phone Number')

        return super(EmployeeProfile, self).create(vals)

    def write(self, vals):
        if 'email' in vals:
            if not re.match(self.email_regex, vals['email']):
                raise ValidationError('Not a valid email ID')
        if 'phone_number' in vals:
            if not re.match(self.phone_number_regex, vals['phone_number']):
                raise ValidationError('Not a valid Phone Number')
        return super(EmployeeProfile, self).write(vals)

    def send_career_plan_email(self):
        mail_template = self.env.ref('career_planing.mail_template_career_plan')
        for employee in self:
            if mail_template:
                mail_template.send_mail(employee.id, force_send=True)
class CareerPlan(models.Model):
    _name = 'career.plan'
    _description = 'Career Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'employee'

    employee = fields.Many2one('employee.profile', string='Employee', required=True, tracking=True)
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    goals_id = fields.Many2many('career.goal', string='Goals', tracking=True)
    career_path_id = fields.One2many('career.path', 'career_plan', string='Career Path', tracking=True)


class CareerPath(models.Model):
    _name = 'career.path'
    _description = 'Career Path'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    career_plan = fields.Many2one('career.plan', string='Career Plan', tracking=True)
    description = fields.Text(string='Description', tracking=True)
    required_skills = fields.Many2many('employee.skill', string='Required Skills', tracking=True)
    promotion_criteria = fields.Text(string='Promotion Criteria', tracking=True)


class Goal(models.Model):
    _name = 'career.goal'
    _description = 'Career Goal'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Goal', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    # career_plan = fields.Many2one('career.plan', string='Career Plan', required=True, tracking=True)
    priority = fields.Selection(selection=[('0', 'vLow'), ('1', 'Low'), ('2', 'Medium'), ('3', 'High')],
                                string='Priority',
                                default='1', tracking=True)
    state = fields.Selection(
        selection=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'),
                   ('draft', 'Draft')],
        string='Status', default='pending', readonly=True, tracking=True)
    color = fields.Integer(string="Color", )

    def button_in_progress(self):
        for rec in self:
            rec.state = "in_progress"

    def button_complete(self):
        for rec in self:
            rec.state = "completed"

    def button_reset_to_draft(self):
        for rec in self:
            rec.state = "draft"

    def button_pending(self):
        for rec in self:
            rec.state = "pending"
