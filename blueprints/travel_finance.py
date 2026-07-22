"""Travel, requests, and finance routes extracted from app.py."""

from flask import Blueprint

import travel_finance_views
from security_utils import login_required


travel_finance_bp = Blueprint('travel_finance', __name__)


@travel_finance_bp.route('/zahtevi/finansijski')
@login_required
def finansijski_zahtevi():
    """Financial requests page."""
    return travel_finance_views.render_financial_requests_page()


@travel_finance_bp.route('/zahtevi/slobodan-dan')
@login_required
def zahtev_slobodan_dan():
    """Day off request page."""
    return travel_finance_views.render_day_off_request_page()


@travel_finance_bp.route('/zahtevi/godisnji-odmor')
@login_required
def zahtev_godisnji_odmor():
    """Vacation request page."""
    return travel_finance_views.render_vacation_request_page()


@travel_finance_bp.route('/zahtevi/razno')
@login_required
def zahtev_razno():
    """Miscellaneous request page."""
    return travel_finance_views.render_misc_request_page()


@travel_finance_bp.route('/finansije/plan')
@login_required
def finansijski_plan():
    """Financial plan page."""
    return travel_finance_views.render_financial_plan_page()


@travel_finance_bp.route('/finansije/nabavka')
@travel_finance_bp.route('/zahtevi/nabavka')
@login_required
def zahtev_nabavka():
    """Procurement request page."""
    return travel_finance_views.render_procurement_request_page()


@travel_finance_bp.route('/terenska-aktivnost')
@login_required
def terenska_aktivnost():
    """Field activity page."""
    return travel_finance_views.render_field_activity_page()


@travel_finance_bp.route('/zahtev-sluzbeni-put')
@login_required
def zahtev_sluzbeni_put():
    """Business trip request form with vehicle and timesheet integration."""
    import app as museum_app

    return travel_finance_views.render_business_trip_request_page(
        get_museum_vehicles=museum_app.get_museum_vehicles,
    )


@travel_finance_bp.route('/api/field-trip/create', methods=['POST'])
@login_required
def api_field_trip_create():
    """Create field trip request with vehicle reservation and timesheet entries."""
    return travel_finance_views.api_field_trip_create()


@travel_finance_bp.route('/api/route/calculate', methods=['POST'])
@login_required
def api_route_calculate():
    """Calculate route distance and toll from static database."""
    import app as museum_app

    return travel_finance_views.api_route_calculate(
        get_museum_vehicles=museum_app.get_museum_vehicles,
    )


@travel_finance_bp.route('/api/osm/route-preview', methods=['POST'])
@login_required
def api_osm_route_preview():
    """Proxy OSM geocoding and routing through the server."""
    return travel_finance_views.api_osm_route_preview()


@travel_finance_bp.route('/api/nabavka/save', methods=['POST'])
@login_required
def api_nabavka_save():
    """Save procurement request to database."""
    return travel_finance_views.api_nabavka_save()


@travel_finance_bp.route('/api/nabavka/list')
@login_required
def api_nabavka_list():
    """List procurement requests for current user."""
    return travel_finance_views.api_nabavka_list()


@travel_finance_bp.route('/api/nabavka/export-word', methods=['POST'])
@login_required
def api_nabavka_export_word():
    """Export procurement request to Word document."""
    return travel_finance_views.api_nabavka_export_word()


@travel_finance_bp.route('/api/nabavka/export-word/<int:request_id>')
@login_required
def api_nabavka_export_word_by_id(request_id):
    """Export saved procurement request to Word document by ID."""
    import app as museum_app

    return travel_finance_views.api_nabavka_export_word_by_id(
        request_id,
        can_access_owned_record=museum_app.can_access_owned_record,
    )


@travel_finance_bp.route('/api/finansijski-plan/save', methods=['POST'])
@login_required
def api_finansijski_plan_save():
    """Save financial plan to database."""
    import app as museum_app

    return travel_finance_views.api_finansijski_plan_save(
        get_postgres_connection=museum_app.get_postgres_connection,
    )


@travel_finance_bp.route('/api/finansijski-plan/list')
@login_required
def api_finansijski_plan_list():
    """List financial plans for current user."""
    import app as museum_app

    return travel_finance_views.api_finansijski_plan_list(
        get_postgres_connection=museum_app.get_postgres_connection,
        current_user_is_admin=museum_app.current_user_is_admin,
    )


@travel_finance_bp.route('/api/finansijski-plan/<int:plan_id>')
@login_required
def api_finansijski_plan_get(plan_id):
    """Load saved financial plan by ID."""
    import app as museum_app

    return travel_finance_views.api_finansijski_plan_get(
        plan_id,
        get_postgres_connection=museum_app.get_postgres_connection,
        can_access_owned_record=museum_app.can_access_owned_record,
    )


@travel_finance_bp.route('/api/finansijski-plan/export-word', methods=['POST'])
@login_required
def api_finansijski_plan_export_word():
    """Export financial plan to Word document."""
    return travel_finance_views.api_finansijski_plan_export_word()


@travel_finance_bp.route('/api/finansijski-plan/export-word/<int:plan_id>')
@login_required
def api_finansijski_plan_export_word_by_id(plan_id):
    """Export saved financial plan to Word document by ID."""
    import app as museum_app

    return travel_finance_views.api_finansijski_plan_export_word_by_id(
        plan_id,
        get_postgres_connection=museum_app.get_postgres_connection,
        can_access_owned_record=museum_app.can_access_owned_record,
    )
