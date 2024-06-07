from odoo import http
from odoo.http import request
import xlsxwriter
from io import BytesIO
import base64

class MldataReportController(http.Controller):

    @http.route('/ml_data/report', type='http', auth='user')
    def get_Mldata_report(self, **kwargs):
        # Fetch attendance records
        attendance_records = request.env['career.ml'].search([])
        # attendance_records = request.env['mohsin.student.attendance'].search([])

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Employee_data Report')

        # Add a bold format for headers
        bold = workbook.add_format({'bold': True})

        # Write the headers
        headers = {
            "Logical quotient rating",
            "hackathons",
            "coding skills rating",
            "public speaking points",
            "self-learning capability?",
            "Extra-courses did",
            "interested career area",  # lowercase the name
            "Type of company want to settle in?",  # typo corrected
            "Taken inputs from seniors or elders",
            "worked in teams ever?",
            "Introvert",
        }

        # headers = ['Roll Number', 'Student Name', 'Attendance Date', 'Course', 'Batch', 'Attendance Sheet', 'Attendance Type']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, bold)

        # Write the data
        row = 1
        for record in attendance_records:
            worksheet.write(row, 0, record.employee_id.name)
            worksheet.write(row, 1, record.logical_quotient_rating)
            worksheet.write(row, 2, str(record.hackathons))
            worksheet.write(row, 3, str(record.coding_skills_rating))
            worksheet.write(row, 4, str(record.public_speaking_points))
            worksheet.write(row, 5, str(record.self_learning_capability))
            worksheet.write(row, 6, str(record.extra_courses))
            worksheet.write(row, 7, str(record.interested_career_area.name))
            worksheet.write(row, 8, str(record.company_preferencee.name))
            worksheet.write(row, 9, str(record.inputs_from_elders))
            worksheet.write(row, 10, record.worked_in_teams)
            worksheet.write(row, 11, str(record.introvert))
            worksheet.write(row, 12, record.suggested_job_role)
            row += 1

        workbook.close()

        output.seek(0)
        file_data = output.read()
        output.close()

        # Return the file as a response
        response = request.make_response(
            file_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=Employee_Data_Report.xlsx;')
            ]
        )
        return response


