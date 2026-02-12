from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Enrollment(models.Model):
    _name = 'academy.enrollment'
    _description = 'Inscripción'
    
    student_id = fields.Many2one('academy.student', string='Estudiante', required=True, ondelete='restrict')
    name = fields.Char(string='Nombre Completo del Estudiante', compute='_compute_name', store=True)
    course_id = fields.Many2one('academy.course', string='Comisión', required=True, ondelete='restrict')
    enrollment_date = fields.Date(string='Fecha de Inscripción', default=fields.Date.context_today)
    status = fields.Selection(
        [
            ('pending', 'A confirmar'),
            ('rejected', 'Rechazado'), 
            ('enrolled', 'Cursando'), 
            ('passed', 'Aprobado'), 
            ('dropped', 'Abandonado'), 
            ('failed', 'Reprobado'), 
            ('exempted', 'Promocionado')
            ], 
        string='Estado', 
        default='pending')
    
    @api.constrains('student_id', 'course_id')
    def _check_completed_subject(self):
        # avoid iterating over all student.enrollment_ids per record
        # relevant (student_id, subject_id) pairs for current records
        enrollment_pairs = {}
        for enrollment in self:
            student = enrollment.student_id
            course = enrollment.course_id
            subject = course.subject_id if course else False
            if student and subject:
                enrollment_pairs[enrollment.id] = (student.id, subject.id)
        if not enrollment_pairs:
            return

        # unique sets for the domain
        student_ids = list({pair[0] for pair in enrollment_pairs.values()})
        subject_ids = list({pair[1] for pair in enrollment_pairs.values()})

        # query once for all completed enrollments matching any of these (student, subject) pairs
        completed_data = self.env['academy.enrollment'].read_group(
            [
                ('student_id', 'in', student_ids),
                ('status', 'in', ['pending', 'enrolled', 'passed', 'exempted']),
                ('course_id.subject_id', 'in', subject_ids),
            ],
            ['student_id', 'course_id.subject_id'],
            ['student_id', 'course_id.subject_id'],
        )

        # set of (student_id, subject_id) pairs that already have a completed enrollment
        completed_pairs = {
            (data['student_id'][0], data['course_id.subject_id'][0])
            for data in completed_data
            if data.get('student_id') and data.get('course_id.subject_id')
        }

        # raise an error if any of the current enrollments tries to enroll a student in a subject they have already completed
        for enrollment in self:
            pair = enrollment_pairs.get(enrollment.id)
            if pair and pair in completed_pairs:
                raise ValidationError('El estudiante ya se ha inscripto o ha completado esta asignatura.')
    
    @api.depends('student_id.partner_id.name')
    def _compute_name(self):
        for enrollment in self:
            enrollment.name = enrollment.course_id.code + ' - ' + enrollment.student_id.file if enrollment.student_id and enrollment.course_id else ''
    