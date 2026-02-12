from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Grade(models.Model):
    _name = 'academy.grade'
    _description = 'Calificación'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _res_name = 'student_id'
    _rec_name = 'student_id'

    student_id = fields.Many2one('academy.student', required=True, ondelete='cascade')
    course_id = fields.Many2one('academy.course', required=True, ondelete='cascade')
    
    value = fields.Float(string='Calificación', required=True, default=1.0)
    type = fields.Selection([
        ('entrance', 'Examen de Ingreso'),
        ('assignment', 'Trabajo Práctico'),
        ('exam', 'Parcial'),
        ('resit', 'Recuperatorio'),
        ('final', 'Final'),
        ('thesis', 'Tesis'),
    ], string='Tipo de Calificación', required=True, default='exam')
    description = fields.Char(string='Descripción')

    @api.constrains('value')
    def _check_value_range(self):
        for record in self:
            if record.value < 1 or record.value > 10:
                raise ValidationError('La calificación debe estar entre 1 y 10.')
    
    @api.onchange('value')
    def _onchange_value(self):
        if self.value < 1 or self.value > 10:
            return {
                'warning': {
                    'title': 'Valor inválido',
                    'message': 'La calificación debe estar entre 1 y 10.',
                }
            }