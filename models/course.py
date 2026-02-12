from odoo import api, fields, models

class Course(models.Model):
    _name = 'academy.course'
    _description = 'Comisión'
    _rec_name = 'code'
    _res_name = 'code'
    _sql_constraints = [
    ('code_unique', 'unique (code)', 'The code must be unique!'),
]
    
    subject_id = fields.Many2one('academy.subject', string='Asignatura', required=True, ondelete='restrict')
    teacher_id = fields.Many2one('academy.teacher', string='Profesor', required=True, ondelete='restrict')
    student_ids = fields.Many2many('academy.student', string='Estudiantes', compute='_compute_student_ids')

    enrollment_ids = fields.One2many('academy.enrollment', 'course_id', string='Inscripciones')
    code = fields.Char(string='Código', required=True)
    start_date = fields.Date(string='Fecha de Inicio', required=True)
    end_date = fields.Date(string='Fecha de Fin', required=True)
    schedule = fields.Char(string='Horario')
    room = fields.Char(string='Aula')
    
    @api.depends('enrollment_ids.student_id')
    def _compute_student_ids(self):
        for course in self:
            course.student_ids = course.enrollment_ids.mapped('student_id')