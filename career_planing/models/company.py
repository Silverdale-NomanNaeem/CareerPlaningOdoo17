from odoo import models, fields, api


class Company(models.Model):
    _inherit = 'res.company'
    _description = 'Company want to Settle'

    company_rating = fields.Float(string='Company Rating', compute='_compute_rating')
    feedback_id = fields.One2many('employee.feedback', 'company_id', string="Feedback")
    numbers_of_reviews = fields.Integer(string="Number of Reviews", readonly=True)

    @api.depends('feedback_id')
    def _compute_rating(self):
        for rec in self:
            ratings = []
            num_of_reviews = 0
            for feedback in rec.feedback_id:
                try:
                    ratings.append(int(feedback.rating))
                    num_of_reviews += 1
                except ValueError:
                    continue  # Skip if the rating cannot be converted to an integer

            total_sum = sum(ratings)
            average = total_sum / len(ratings) if ratings else 0

            rec.company_rating = float(average)
            rec.numbers_of_reviews = num_of_reviews
