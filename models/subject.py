from odoo import api, fields, models

class Subject(models.Model):
    _name = 'academy.subject'
    _description = 'Asignatura'
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'The name must be unique!'),
        ('code_unique', 'unique (code)', 'The code must be unique!'),
    ]

    name = fields.Char(string='Nombre de la Asignatura', required=True)
    code = fields.Char(string='Código', required=True)
    teacher_ids = fields.Many2many('academy.teacher', string='Profesores')
    description = fields.Text(string='Descripción')