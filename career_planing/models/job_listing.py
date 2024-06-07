from odoo import models, fields, api
import pyttsx3


class JobListing(models.Model):
    _name = 'job.listing'
    _description = 'Job Listing'
    _rec_name = 'job_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # name = fields.Char(string='Job Title', required=True)
    job_id = fields.Many2one('hr.job', 'Job Position', required=True)

    description = fields.Text(string='Job Description', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, tracking=True)
    location = fields.Char(string='Location', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency',tracking=True,defaul="USD")
    salary = fields.Monetary(string='Salary', tracking=True)
    job_type = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract')
    ], string='Job Type', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='State', default='draft', required=True, tracking=True)

    def correct_grammar(self):
        api = "AIzaSyAwnk6DKf5wE3X7QNC0AVoD_L9htTuAaMo"
        import google.generativeai as genai
        genai.configure(api_key=api)
        model = genai.GenerativeModel('gemini-pro')
        text = self.description + "\n Correct Grammar"
        response = model.generate_content(text)
        print(response.text)
        self.description = response.text
        print("response is:", response.text)
        return


    def text_to_speech(self):
        engine = pyttsx3.init()
        for record in self:
            if record.description:
                engine.setProperty('rate', 125)

                voices = engine.getProperty('voices')  # getting details of current voice

                engine.say(record.description)
                engine.runAndWait()

    def action_open(self):
        self.state = 'open'

    def action_closed(self):
        self.state = 'closed'

    def action_draft(self):
        self.state = 'draft'


class JobApplication(models.Model):
    _name = 'job.application'
    _description = 'Job Application'
    _rec_name = 'job_listing_id'

    job_listing_id = fields.Many2one('job.listing', string='Job', required=True)
    applicant_id = fields.Many2one('res.partner', string='Applicant', required=True)
    application_date = fields.Date(string='Application Date', default=fields.Date.today)
    state = fields.Selection([
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired')
    ], string='State', default='applied', required=True)

    def action_applied(self):
        self.state = 'applied'

    def action_shortlist(self):
        self.state = 'shortlisted'

    def action_interview(self):
        self.state = 'interview'

    def action_offer(self):
        self.state = 'offered'

    def action_reject(self):
        self.state = 'rejected'

    def action_hire(self):
        self.state = 'hired'
