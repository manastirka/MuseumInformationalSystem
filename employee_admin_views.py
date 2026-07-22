"""Shared route implementations for employee admin views."""

from flask import flash, redirect, render_template, request, url_for

import audit_support


def render_employees_database(*, get_employee_directory):
    """Render the employee directory database."""
    employees_list = get_employee_directory()
    return render_template(
        'admin_employees_database.html',
        employees=employees_list,
        total_employees=len(employees_list),
    )


def render_employee_profiles_database(*, get_employee_directory):
    """Render the employee profiles database."""
    employees = get_employee_directory()
    employees_list = [emp for emp in employees if emp.get('description')]

    total_profiles = len(employees_list)
    total_directory = len(employees)
    with_descriptions = len([emp for emp in employees if emp.get('description')])
    departments = len({emp['department'] for emp in employees_list if emp.get('department')})

    statistics = {
        'total_profiles': total_profiles,
        'with_descriptions': with_descriptions,
        'total_departments': departments,
        'completion_rate': round((with_descriptions / total_directory * 100), 1)
        if total_directory > 0
        else 0,
    }

    return render_template(
        'admin_employee_profiles_database.html',
        employees=employees_list,
        statistics=statistics,
        total_profiles=total_profiles,
    )


def handle_add_user(*, get_museum_employees, get_employee_directory, password_hasher):
    """Handle rendering and submission of the add-user form."""
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        department = request.form.get('department')
        position = request.form.get('position')
        role = request.form.get('role', 'employee')
        password = request.form.get('password', '')

        if not all([email, full_name, department, position]):
            flash('Сви поља су обавезна.', 'error')
            return redirect(url_for('add_user'))

        if not password or len(password) < 8:
            flash('Лозинка је обавезна и мора имати најмање 8 карактера.', 'error')
            return redirect(url_for('add_user'))

        employees = get_museum_employees()
        if email in employees:
            flash('Корисник са овом е-mail адресом већ постоји.', 'error')
            return redirect(url_for('add_user'))

        # Persist to PostgreSQL via the canonical auth path. create_user hashes
        # the password, resolves role_id, sets is_first_login and lets the
        # database assign the id (no more max() over an empty fallback dict).
        from postgres_auth import get_postgres_auth

        new_user_id = get_postgres_auth().create_user(
            email=email,
            password=password,
            full_name=full_name,
            role=role,
            position=position,
        )
        if not new_user_id:
            flash('Грешка при чувању корисника у базу. Корисник није додат.', 'error')
            return redirect(url_for('add_user'))

        audit_support.record_audit(
            action=audit_support.ACTION_USER_CREATE,
            entity_type='user',
            entity_id=new_user_id,
            summary=f'Креиран корисник {full_name} <{email}> (улога: {role})',
            new_values={
                'id': new_user_id, 'email': email, 'full_name': full_name,
                'role': role, 'department': department, 'position': position,
            },
        )
        flash(
            (
                f'Корисник {full_name} је успешно додат у систем. '
                'Корисник мора да промени лозинку при првој пријави.'
            ),
            'success',
        )
        return redirect(url_for('employees_database'))

    directory = get_employee_directory()
    if directory:
        departments = sorted({emp['department'] for emp in directory if emp.get('department')})
    else:
        departments = sorted(
            {
                emp['department']
                for emp in get_museum_employees().values()
                if emp.get('department')
            }
        )

    return render_template('admin_add_user.html', departments=departments)
