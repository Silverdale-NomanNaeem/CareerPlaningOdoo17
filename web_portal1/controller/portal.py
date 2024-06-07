from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from odoo import http, _
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


class EmployeePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        rtn = super(EmployeePortal, self)._prepare_home_portal_values(counters)
        print('_prepare_home_portal_values called ..... ', rtn)
        rtn['employee_counts'] = request.env['employee.profile'].search_count([])
        return rtn

    @http.route(['/my/employee', '/my/employee/page/<int:page>'], auth="user", type='http', website=True)
    def EmployeePortalListView(self, page=1, sortby='id', search="", search_in='All', groupby="none", **kw):
        if not groupby:
            groupby = "none"

        sorted_list = {
            'id': {'label': 'ID Desc', 'order': 'id desc'},
            'name': {'label': 'Name', 'order': 'name'},
            'email': {'label': 'Email', 'order': 'email'},
        }
        search_list = {
            'All': {'label': 'All', 'input': 'All', 'domain': []},
            'name': {'label': 'Name', 'input': 'name', 'domain': [('name', 'ilike', search)]},
            'email': {'label': 'Email', 'input': 'email', 'domain': [('email', 'ilike', search)]},
        }
        groupby_list = {
            'none': {'input': 'None', 'label': _('None'), 'domain': []},
            'skill_id': {'input': 'skill_id', 'label': _('Skill'), 'domain': []},
            'goal_id': {'input': 'goal_id', 'label': _('Goal'), 'domain': []},
        }

        employee_group_by = groupby_list.get(groupby, {}).get('input', '')

        search_domain = search_list[search_in]['domain']
        default_order_by = sorted_list[sortby]['order']
        employee_obj = request.env['employee.profile']
        total_employee = employee_obj.sudo().search_count(search_domain)
        employee_url = '/my/employee'
        page_detail = pager(url=employee_url,
                            total=total_employee,
                            page=page,
                            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby},
                            step=5
                            )
        employees = employee_obj.sudo().search(search_domain, limit=5, order=default_order_by,
                                               offset=page_detail['offset'])

        if groupby != 'none':
            employee_group_list = {}
            for emp in employees:
                key = getattr(emp, groupby)
                if key not in employee_group_list:
                    employee_group_list[key] = {'employee': []}
                employee_group_list[key]['employee'].append(emp)
            employee_group_list = [{'employee': v['employee']} for k, v in employee_group_list.items()]
        else:
            employee_group_list = [{'employee': employees}]

        vals = {
            'group_employee': employee_group_list,
            'page_name': 'employee_list_view',
            'pager': page_detail,
            'default_url': employee_url,
            'groupby': groupby,
            'sortby': sortby,
            'searchbar_sortings': sorted_list,
            'searchbar_groupby': groupby_list,
            'search_in': search_in,
            'searchbar_inputs': search_list,
            'search': search
        }

        return request.render('web_portal1.employee_list_view_portal', vals)

    @http.route('/my/employee/<model("employee.profile"):employee_id>', auth="user", type='http', website=True)
    def EmployeePortalFormView(self, employee_id, **kw):
        print("form view is called with id ", employee_id)
        vals = {'employee': employee_id, 'page_name': 'employee_form_view'}
        employee_record = request.env['employee.profile'].search([])
        employee_ids = employee_record.ids
        employee_index = employee_ids.index(employee_id.id)
        print(employee_ids)
        print(employee_index)

        if employee_index != 0 and employee_ids[employee_index - 1]:
            vals['prev_record'] = '/my/employee/{}'.format(employee_ids[employee_index - 1])
        if employee_index < len(employee_ids) - 1 and employee_ids[employee_index + 1]:
            vals['next_record'] = '/my/employee/{}'.format(employee_ids[employee_index + 1])
        print(vals)
        return request.render("web_portal1.employee_form_view_portal", vals)

    @http.route("/my/employee/print/<model('employee.profile'):employee_id>", auth="user", type='http', website=True)
    def PrintEmployeeResume(self, employee_id, **kw):
        print("print controller is called with id ", employee_id)
        return

    @http.route("/my/employee/print/<model('employee.profile'):employee_id>", auth="user", type="http",
                website=True)
    def EmployeeResumePrint(self, employee_id, **kw):
        print("Hello this is called ", employee_id)
        return self._show_report(model=employee_id, report_type='pdf',
                                 report_ref='career_planing.action_employee_resume_report',
                                 download=True)
