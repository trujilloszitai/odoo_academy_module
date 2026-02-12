from odoo import api, fields, models

class Student(models.Model):
    _name = 'academy.student'
    _description = 'Estudiante'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _res_name = 'partner_id'
    _rec_name = 'partner_id'
    _sql_constraints = [
        ('file_unique', 'unique (file)', 'The file must be unique!'),
    ]

    partner_id = fields.Many2one('res.partner', required = True, ondelete='restrict')
    grade_ids = fields.One2many('academy.grade', 'student_id', string='Calificaciones')
    enrollment_ids = fields.One2many('academy.enrollment', 'student_id', string='Inscripciones')
    course_ids = fields.Many2many('academy.course', string='Comisiones', compute='_compute_course_ids')
    
    file = fields.Char(string='Legajo', required=True)
    enrollment_date = fields.Date(string='Fecha de Inscripción', default=fields.Date.context_today)
    avg_grade = fields.Float(string='Promedio', compute='_compute_avg_grade', store=True)
    completed_asignatures = fields.Integer(string='Asignaturas Completadas', compute='_compute_completed_asignatures')
        
    @api.depends('grade_ids.value')
    def _compute_avg_grade(self):
        if not self:
            return

        for student in self:
            grades = student.grade_ids
            student.avg_grade = (
                sum(grades.mapped('value')) / len(grades)
                if grades else 0.0
            )

    # @api.depends('partner_id.name')
    # def _compute_name(self):
    #     for student in self:
    #         student.name = student.partner_id.name if student.partner_id else ''
    
    @api.depends('enrollment_ids.course_id')
    def _compute_course_ids(self):
        for student in self:
            student.course_ids = student.enrollment_ids.mapped('course_id')
    
    @api.depends('enrollment_ids')
    def _compute_completed_asignatures(self):
        for student in self:
            completed_courses = student.enrollment_ids.filtered(lambda e: e.status == 'completed').mapped('course_id')
            student.completed_asignatures = len(completed_courses)