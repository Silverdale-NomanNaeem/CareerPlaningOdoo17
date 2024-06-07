/** @odoo-module **/
import { Component, mount, useState } from 'owl';
import { useWillStart } from 'web.core';


class EmployeeProfile extends Component {
    static template = 'career_planning.employee_profile_template';

    constructor() {
        super(...arguments);
        this.state = useState({
            profiles: [],
            filter: '',
        });
    }

    async willStart() {
        const profiles = await this.fetchProfiles();
        this.state.profiles = profiles;
    }

    async fetchProfiles() {
        const response = await fetch('/employee_profiles');
        return await response.json();
    }

    get filteredProfiles() {
        const filter = this.state.filter.toLowerCase();
        return this.state.profiles.filter(profile =>
            profile.name.toLowerCase().includes(filter) ||
            profile.job_title.toLowerCase().includes(filter) ||
            profile.department.toLowerCase().includes(filter)
        );
    }
}

// Wait for the DOM to be ready before mounting the component
document.addEventListener('DOMContentLoaded', () => {
    mount(EmployeeProfile, { target: document.getElementById('employee_profile_app') });
});
