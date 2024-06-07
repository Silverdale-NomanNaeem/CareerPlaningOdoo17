from odoo import models, fields
import pickle
import pandas as pd
import os
class CareerMl(models.Model):
    _name = 'career.ml'
    _description = 'Career ML Model'

    # Inherit fields from employee.profile
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'employee_id'

    # Additional fields
    # name = fields.Char(string='Name', required=True)

    employee_id = fields.Many2one('employee.profile', string='Employee')
    logical_quotient_rating = fields.Float(string='Logical Quotient Rating')  # yes
    hackathons = fields.Integer(string='Hackathons')  # yes
    coding_skills_rating = fields.Float(string='Coding Skills Rating')  # yes
    public_speaking_points = fields.Integer(string='Public Speaking Points')  # yes
    self_learning_capability = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                string='Self-learning Capability')  # yes
    extra_courses = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Extra Courses')  # yes
    # interested_career_area = fields.Char(string='Interested Career Area')  # yes
    interested_career_area = fields.Many2one('career.path', string='Interested Career Area')  # yes
    company_preferencee = fields.Many2one('res.company', string='Type of Company Want to Settle In')
    # company_preference = fields.Selection(
    #     [('startup', 'Startup'), ('corporate', 'Corporate'), ('government', 'Government'),
    #      ('non_profit', 'Non-profit')], string='Type of Company Want to Settle In')  # yes
    inputs_from_elders = fields.Boolean(string='Taken Inputs from Seniors or Elders')  # yes
    worked_in_teams = fields.Boolean(string='Worked in Teams Ever?')  # yes
    introvert = fields.Boolean(string='Introvert')  # yes
    suggested_job_role = fields.Char(string='suggested_job_role', readonly=True)

    def action_prediction(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_path, '..', 'static', 'model1.pkl')
        model_path = os.path.normpath(model_path)

        with open(model_path, 'rb') as file:
        # with open('/opt/odoo17/custom_addons/career_planing/static/model1.pkl', 'rb') as file:
            model = pickle.load(file)




      # asds
        for rec in self:
            data = {
                "Logical quotient rating": rec.logical_quotient_rating,
                "hackathons": rec.hackathons,
                "coding skills rating": rec.coding_skills_rating,
                "public speaking points": rec.public_speaking_points,
                "self-learning capability?": rec.self_learning_capability,
                "Extra-courses did": rec.extra_courses,
                "interested career area": rec.interested_career_area.name.lower(),
                "Type of company want to settle in?": rec.company_preferencee.name,
                "Taken inputs from seniors or elders": rec.inputs_from_elders,
                "worked in teams ever?": rec.worked_in_teams,
                "Introvert": rec.introvert,
            }

            df = pd.DataFrame(data, index=[0])
            print(df)

            def convert_values(col):
                for i, val in enumerate(col):
                    if val == 'yes' or val == 'True':
                        col.iloc[i] = 1
                    elif val == 'no' or val == 'False':
                        col.iloc[i] = 0
                return col

            df = df.apply(convert_values, axis=1)

            category_cols = ['interested career area', 'Type of company want to settle in?']
            for col in category_cols:
                df[col] = df[col].astype('category').cat.codes

            feed = df[['Logical quotient rating', 'coding skills rating', 'hackathons', 'public speaking points',
                       'self-learning capability?', 'Extra-courses did', 'Taken inputs from seniors or elders',
                       'worked in teams ever?', 'Introvert']]

            predictions = model.predict(feed)
            self.suggested_job_role = predictions[0]
            # print("Suggestion is:", predictions)


class Career_Ask(models.Model):
    _name = 'career.ask'
    _description = 'Career Ask Model'
    _rec_name = 'asking'

    # Inherit fields from employee.profile
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Additional fields
    asking = fields.Text(string='Ask about your career', required=True)
    response = fields.Text(string="Response", readonly=True)

    def action_ask(self):
        api = "AIzaSyAwnk6DKf5wE3X7QNC0AVoD_L9htTuAaMo"

        import google.generativeai as genai

        genai.configure(api_key=api)

        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(self.asking)

        # text = response.get_generated_content()
        print(response.text)

        self.response = response.text
        print("response is:", response.text)
        return
