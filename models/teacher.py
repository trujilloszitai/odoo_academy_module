from odoo import api, fields, models

class Teacher(models.Model):
    _name = 'academy.teacher'
    _description = 'Profesor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _res_name = 'partner_id'
    _rec_name = 'partner_id'
    _sql_constraints = [
        ('file_unique', 'unique (file)', 'The file must be unique!'),
    ]
    
    partner_id = fields.Many2one('res.partner', required = True, ondelete='restrict')
    # name = fields.Char(string='Nombre Completo', compute='_compute_name', store=True)
    file = fields.Char(string='Matrícula', required=True)
    subject_ids = fields.Many2many('academy.subject', string='Asignaturas')
    specialty = fields.Char(string='Especialidad')
    hire_date = fields.Date(string='Fecha de Contratación', default=fields.Date.context_today)

    # @api.depends('partner_id.name')
    # def _compute_name(self):
    #     for student in self:
    #         student.name = student.partner_id.name if student.partner_id else ''