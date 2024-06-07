from odoo import models, fields, api

class Quiz(models.Model):
    _name = 'quiz.quiz'

    name = fields.Char(string="Quiz Title")
    description = fields.Text(string="Description")
    questions = fields.One2many('quiz.question', 'quiz_id', string="Questions")

class Question(models.Model):
    _name = 'quiz.question'
    _rec_name = 'question_text'

    quiz_id = fields.Many2one('quiz.quiz', string="Quiz")
    question_text = fields.Text(string="Question Text")
    options = fields.One2many('quiz.option', 'question_id', string="Options")

class Option(models.Model):
    _name = 'quiz.option'
    _rec_name = 'option_text'

    question_id = fields.Many2one('quiz.question', string="Question")
    option_text = fields.Text(string="Option Text")
    is_correct = fields.Boolean(string="Is Correct")

class QuizResponse(models.Model):
    _name = 'quiz.response'
    _rec_name = 'user_id'

    quiz_id = fields.Many2one('quiz.quiz', string="Quiz")
    user_id = fields.Many2one('res.users', string="User")
    responses = fields.One2many('quiz.response.line', 'response_id', string="Responses")
    score = fields.Float(string="Score", compute='_compute_score', store=True)

    @api.depends('responses.is_correct')
    def _compute_score(self):
        for response in self:
            total_questions = len(response.quiz_id.questions)
            if total_questions:
                correct_responses = sum(line.is_correct for line in response.responses)
                response.score = (correct_responses / total_questions) * 100
            else:
                response.score = 0.0



class QuizResponseLine(models.Model):
    _name = 'quiz.response.line'
    _rec_name = 'response_id'

    response_id = fields.Many2one('quiz.response', string="Response")
    # question_check = fields.Char(compute="_compute_question_check", store=True)
    question_id = fields.Many2one('quiz.question', string="Question")
    selected_option_id = fields.Many2one('quiz.option', string="Selected Option")
    is_correct = fields.Boolean(string="Is Correct", compute='_compute_is_correct', store=True)

    @api.depends('response_id.responses.question_id', 'response_id.quiz_id.questions')
    def _compute_question_check(self):
        for line in self:
            answered_question_ids = line.response_id.responses.mapped('question_id.id')
            all_question_ids = line.response_id.quiz_id.questions.ids
            available_questions = list(set(all_question_ids) - set(answered_question_ids))
            line.question_check = ','.join(map(str, available_questions))

    @api.depends('selected_option_id', 'question_id.options.is_correct')
    def _compute_is_correct(self):
        for line in self:
            line.is_correct = line.selected_option_id.is_correct if line.selected_option_id else False

    # Define a new compute method to return the list of available question IDs
    # @api.depends('question_check')
    # def _compute_question_ids(self):
    #     for record in self:
    #         if record.question_check:
    #             record.available_question_ids = [int(id_str) for id_str in record.question_check.split(',')]
    #
    # available_question_ids = fields.Many2many('quiz.question', compute='_compute_question_ids', string="Available Questions")
