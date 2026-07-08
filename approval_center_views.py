"""Unified approval center and archive (Центар за одобравање / Архива).

One page for everything waiting on the caller's decision and one read-only
archive, each with a Захтеви / Документа tab. This is a presentation layer
only: the data comes from the owning modules (archive_signature_blueprint for
operational requests, document_library_views for the document library) and
every action keeps going through the existing endpoints, so the approval
flows themselves stay untouched.
"""

import logging

from flask import render_template, request

import archive_signature_blueprint
import document_library_views

logger = logging.getLogger(__name__)

# Canonical status vocabulary for the whole approval UI: request statuses
# (pending/in_review/approved/rejected/archived) and document statuses
# (nacrt/na_odobrenju/odobreno/arhivirano) map onto these five keys so every
# badge looks and reads the same.
UNIFIED_STATUS_LABELS = {
    'nacrt': 'Нацрт',
    'na_odobrenju': 'На одобрењу',
    'odobreno': 'Одобрено',
    'odbijeno': 'Одбијено',
    'arhivirano': 'Архивирано',
}

FINAL_DECISION_TO_UNIFIED = {
    'approved': 'odobreno',
    'rejected': 'odbijeno',
}

TABS = ('zahtevi', 'dokumenta')


def _active_tab():
    tab = request.args.get('tab', '')
    return tab if tab in TABS else 'zahtevi'


def render_approval_center():
    """Both approval queues on one page; a failure in one module degrades
    that tab instead of taking the whole center down."""
    zahtevi, zahtevi_error = [], False
    try:
        zahtevi = archive_signature_blueprint.pending_approvals_for_session()
    except Exception:
        logger.exception("Error loading pending requests for approval center")
        zahtevi_error = True

    dokumenta, dokumenta_error = [], False
    try:
        dokumenta = document_library_views.get_pending_document_versions()
    except Exception:
        logger.exception("Error loading pending document versions for approval center")
        dokumenta_error = True

    return render_template(
        'centar_odobravanje.html',
        active_tab=_active_tab(),
        zahtevi=zahtevi,
        zahtevi_error=zahtevi_error,
        dokumenta=dokumenta,
        dokumenta_error=dokumenta_error,
        request_type_labels=archive_signature_blueprint.REQUEST_TYPE_LABELS,
        categories=document_library_views.DOCUMENT_CATEGORIES,
    )


def render_archive_center():
    """Read-only archive of processed requests and archived document
    versions, with the request filters preserved from the old archive page."""
    filter_type = request.args.get('tip', '')
    filter_year = request.args.get('godina', '')
    filter_submitter = request.args.get('podnosilac', '')

    archived_requests, years, zahtevi_error = [], [], False
    try:
        archived_requests, years, filter_year = (
            archive_signature_blueprint.archived_requests_for_session(
                filter_type, filter_year, filter_submitter,
            )
        )
    except Exception:
        logger.exception("Error loading archived requests for unified archive")
        zahtevi_error = True

    for row in archived_requests:
        row['unified_status'] = FINAL_DECISION_TO_UNIFIED.get(
            row.get('final_decision'), 'arhivirano',
        )

    archived_documents, dokumenta_error = [], False
    try:
        archived_documents = document_library_views.get_archived_document_versions()
    except Exception:
        logger.exception("Error loading archived document versions for unified archive")
        dokumenta_error = True

    return render_template(
        'arhiva_centar.html',
        active_tab=_active_tab(),
        archived_requests=archived_requests,
        years=years,
        zahtevi_error=zahtevi_error,
        archived_documents=archived_documents,
        dokumenta_error=dokumenta_error,
        type_labels=archive_signature_blueprint.REQUEST_TYPE_LABELS,
        categories=document_library_views.DOCUMENT_CATEGORIES,
        filter_type=filter_type,
        filter_year=filter_year,
        filter_submitter=filter_submitter,
    )
