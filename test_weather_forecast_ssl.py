"""Reproduces the broken weather forecast caused by RHMZ's new TLS root.

RHMZ (hidmet.gov.rs) certificates now chain to Let's Encrypt's new
'ISRG Root YR', which is absent from older system / certifi CA bundles. As a
result every ``requests.get`` against hidmet.gov.rs raised ``SSLError`` and the
dashboard forecast silently fell back to "Прогноза тренутно није доступна.".

These tests verify the real served certificate chain offline against the CA
bundle the application uses, so they need no network access.
"""

from pathlib import Path

import certifi
import pytest

from cryptography import x509
from cryptography.x509.general_name import DNSName
from cryptography.x509.verification import PolicyBuilder, Store, VerificationError

import dashboard_data_support as dds

_SERVED_CHAIN = Path(__file__).parent / 'tests' / 'fixtures' / 'hidmet_served_chain.pem'


def _load_served_chain():
    """Return (leaf, [intermediates]) exactly as hidmet.gov.rs presents them."""
    certs = x509.load_pem_x509_certificates(_SERVED_CHAIN.read_bytes())
    return certs[0], certs[1:]


def _verify_chain_with_bundle(bundle_path):
    """Verify the served hidmet chain against a CA bundle file (offline)."""
    leaf, intermediates = _load_served_chain()
    roots = x509.load_pem_x509_certificates(Path(bundle_path).read_bytes())
    store = Store(roots)
    # Pin verification to the midpoint of the leaf validity window so the stored
    # fixture keeps verifying after the live (90-day) certificate is renewed.
    window = leaf.not_valid_after_utc - leaf.not_valid_before_utc
    verification_time = leaf.not_valid_before_utc + window / 2
    verifier = (
        PolicyBuilder()
        .store(store)
        .time(verification_time)
        .build_server_verifier(DNSName('www.hidmet.gov.rs'))
    )
    verifier.verify(leaf, intermediates)


def _bundle_trusts_new_root(bundle_path):
    text = Path(bundle_path).read_text(errors='ignore')
    return 'Root YR' in text


def test_repo_bundles_new_isrg_gen_y_roots():
    roots = x509.load_pem_x509_certificates(dds._ISRG_GEN_Y_ROOTS_PATH.read_bytes())
    subjects = ' | '.join(c.subject.rfc4514_string() for c in roots)
    assert 'Root YR' in subjects, subjects
    assert 'Root YE' in subjects, subjects


def test_stock_system_bundle_rejects_hidmet_chain():
    """Documents the root cause on environments lacking the new ISRG root."""
    if _bundle_trusts_new_root(certifi.where()):
        pytest.skip('Stock CA bundle already trusts ISRG Root YR; bug cannot reproduce here.')
    with pytest.raises(VerificationError):
        _verify_chain_with_bundle(certifi.where())


def test_rhmz_ca_bundle_trusts_hidmet_chain():
    """The fix: the bundle used for RHMZ requests verifies the served chain."""
    bundle_path = dds._rhmz_ca_bundle()
    assert Path(bundle_path).exists()
    _verify_chain_with_bundle(bundle_path)
