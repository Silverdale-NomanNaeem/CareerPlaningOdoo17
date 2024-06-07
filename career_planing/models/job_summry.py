from odoo import models, fields, api

class JobSummary(models.TransientModel):
    _name = 'job.summary'
    _description = 'Job Summary'

    job_listing_id = fields.Many2one('job.listing', string='Job Listing', required=True)
    summary = fields.Text(string='Summary')

    @api.model
    def default_get(self, fields_list):
        res = super(JobSummary, self).default_get(fields_list)
        if self.env.context.get('active_id'):
            job_listing = self.env['job.listing'].browse(self.env.context['active_id'])
            res['job_listing_id'] = job_listing.id
            res['summary'] = self.summarize(job_listing.description)
        return res

    def summarize(self, text):
        api = "AIzaSyAwnk6DKf5wE3X7QNC0AVoD_L9htTuAaMo"
        import google.generativeai as genai
        genai.configure(api_key=api)
        model = genai.GenerativeModel('gemini-pro')
        text = text + "\n summrize this text my 1/3"
        response = model.generate_content(text)

        return response.text
