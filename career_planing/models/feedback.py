from odoo import models, fields, api
import pickle
import nltk
from nltk.tokenize import word_tokenize
import string
import os


class Feedback(models.Model):
    _name = 'employee.feedback'
    _description = 'Feedback'
    _rec_name = 'sender'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sender = fields.Many2one('employee.profile', string='Sender', required=True)
    receiver = fields.Many2one('employee.profile', string='Receiver', required=True)
    company_id = fields.Many2one('res.company', "Company")
    date = fields.Date(string='Date')
    details = fields.Text(string='Feedback Details')
    rating = fields.Selection(selection=[('0', 'vLow'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                              string='Rating',
                              default='1', compute='_compute_rating', tracking=True)

    # Download NLTK resources only once
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(nltk.corpus.stopwords.words('english'))

    # Load the model, vectorizer, and label encoder once
    model_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'svm_model.pkl')
    with open(model_path, 'rb') as file:
        svm_model, vectorizer, encoder = pickle.load(file)

    def preprocess_text(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(filtered_tokens)

    @api.depends('details')
    def _compute_rating(self):
        for rec in self:
            if rec.details:
                processed_text = self.preprocess_text(rec.details)
                vectorized_text = self.vectorizer.transform([processed_text])
                predicted_rating = self.svm_model.predict(vectorized_text)
                predicted_rating_original = self.encoder.inverse_transform(predicted_rating)
                # Convert predicted rating to string to match selection field options
                rec.rating = str(predicted_rating_original[0])
            else:
                rec.rating = '1'

    def correct_grammar(self):
        api = "AIzaSyAwnk6DKf5wE3X7QNC0AVoD_L9htTuAaMo"
        import google.generativeai as genai
        genai.configure(api_key=api)
        model = genai.GenerativeModel('gemini-pro')
        text = self.details + "\n Correct Grammar"
        response = model.generate_content(text)
        self.details = response.text

        return


class PerformanceReview(models.Model):
    _name = 'employee.performance.review'
    _description = 'Performance Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee'

    employee = fields.Many2one('employee.profile', string='Employee', required=True)
    review_date = fields.Date(string='Review Date')
    reviewer = fields.Many2one('employee.profile', string='Reviewer')
    goals_achieved = fields.Many2many('career.goal', string='Goals Achieved')
    strengths = fields.Text(string='Strengths')
    areas_for_improvement = fields.Text(string='Areas for Improvement')
    overall_rating = fields.Selection(
        [('poor', 'Poor'), ('fair', 'Fair'), ('good', 'Good'), ('excellent', 'Excellent')], string='Overall Rating')
