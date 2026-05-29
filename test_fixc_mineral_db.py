import os

os.environ.setdefault('FLASK_ENV', 'testing')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SESSION_TYPE', 'filesystem')
os.environ.setdefault('SESSION_FILE_DIR', '/tmp/museum-test-c-mineral-db')

import mineral_translator as m


class TestFuzzyPrefixHonestFlag:
    def test_fuzzy_prefix_guess_not_flagged_as_translated(self):
        # 'kalcXYZ' is not a real mineral; it only shares a 4-char prefix
        # with 'kalcedon'/'kalcit'. The heuristic guess must not claim a
        # confident translation.
        english, was_translated = m.translate_mineral_name('kalcXYZ')
        assert was_translated is False

    def test_fuzzy_prefix_guess_kvarcoid_not_flagged(self):
        english, was_translated = m.translate_mineral_name('kvarcoid')
        assert was_translated is False

    def test_exact_match_still_flagged_true(self):
        # A genuine dictionary match must still report was_translated=True.
        english, was_translated = m.translate_mineral_name('Kalcit')
        assert english == 'Calcite'
        assert was_translated is True

    def test_case_suffix_match_still_flagged_true(self):
        # Instrumental case form 'valentinitom' -> 'valentinit' must stay True.
        english, was_translated = m.translate_mineral_name('valentinitom')
        assert english == 'Valentinite'
        assert was_translated is True


class TestCapitalizedShortTokenExtraction:
    def test_capitalized_short_word_is_extracted(self):
        # 'Led' (capitalized, 3 letters, not in dictionary) was previously
        # dropped because the case check ran after lowercasing. With the
        # fix it should be treated as a candidate mineral token.
        result = m.extract_minerals_from_name('Crni Led')
        assert any(m.normalize_name(x) == 'led' for x in result)

    def test_lowercase_short_descriptor_still_dropped(self):
        # A lowercase short non-dictionary word stays filtered out.
        result = m.extract_minerals_from_name('crni led')
        assert all(m.normalize_name(x) != 'led' for x in result)

    def test_known_mineral_still_extracted(self):
        result = m.extract_minerals_from_name('Kalcit')
        assert any(m.normalize_name(x) == 'kalcit' for x in result)
