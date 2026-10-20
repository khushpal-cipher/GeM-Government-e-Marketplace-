"""Step 1.1: the profile details later checks need, saved, proposed by chat, and warned about."""

from __future__ import annotations

import sqlite3
from datetime import date

import pytest
from fastapi.testclient import TestClient

from gem_assistant.api.app import create_app
from gem_assistant.domain.models import SellerProfile
from gem_assistant.domain.profile_warnings import profile_warnings
from gem_assistant.infrastructure.database import MIGRATIONS, Database
from gem_assistant.services.chat_tools import ChatTools

TODAY = date(2026, 10, 20)


@pytest.fixture
def client(container):
    return TestClient(create_app(container, allowed_hosts=frozenset({"testserver"})))


def test_the_new_details_survive_a_save(container):
    container.profiles.save(SellerProfile(
        gem_registered_on=date(2023, 5, 1), itr_filed_on_gem=True, pfms_bank_verified=False,
        oem_products=["office chair"], own_made_products=["office chair"]))
    saved = container.profiles.get()
    assert (saved.gem_registered_on, saved.itr_filed_on_gem, saved.pfms_bank_verified) == (
        date(2023, 5, 1), True, False)
    assert (saved.oem_products, saved.own_made_products) == (["office chair"], ["office chair"])


def test_a_profile_saved_before_these_details_still_loads(tmp_path):
    db = Database(tmp_path / "old.sqlite3")
    conn = sqlite3.connect(db.path)
    for index, script in enumerate(MIGRATIONS[:5], start=1):  # the schema as it was before step 1.1
        conn.executescript(f"BEGIN;\n{script}\nPRAGMA user_version = {index};\nCOMMIT;")
    conn.execute("INSERT INTO seller_profile (id, business_name, is_mse, is_startup, is_oem, categories_json,"
                 " certifications_json, states_json, updated_at) VALUES (1, 'Old Traders', 1, 0, 0, '[\"chair\"]', '[]', '[]', '2026-01-01T00:00:00+00:00')")
    conn.commit()
    conn.close()
    db.migrate()
    from gem_assistant.infrastructure.sqlite_repositories import SqliteProfileRepository
    profile = SqliteProfileRepository(db).get()
    assert (profile.business_name, profile.itr_filed_on_gem, profile.oem_products) == ("Old Traders", None, [])


def test_over_24_months_without_an_itr_on_gem_warns():
    profile = SellerProfile(gem_registered_on=date(2024, 10, 19), itr_filed_on_gem=False)
    (warning,) = profile_warnings(profile, TODAY)
    assert "more than 24 months" in warning and "ITR" in warning and "19 Oct 2024" in warning


def test_over_24_months_with_the_itr_not_known_asks():
    (warning,) = profile_warnings(SellerProfile(gem_registered_on=date(2020, 1, 1)), TODAY)
    assert "don't know" in warning


def test_under_24_months_or_with_the_itr_filed_does_not_warn():
    assert profile_warnings(SellerProfile(gem_registered_on=date(2024, 10, 21)), TODAY) == []
    assert profile_warnings(SellerProfile(gem_registered_on=date(2020, 1, 1), itr_filed_on_gem=True), TODAY) == []


def test_an_unverified_bank_warns_but_an_unknown_one_does_not():
    assert len(profile_warnings(SellerProfile(pfms_bank_verified=False), TODAY)) == 1
    assert profile_warnings(SellerProfile(), TODAY) == []


def test_an_mse_who_makes_nothing_himself_is_told_the_emd_exemption_does_not_apply():
    (warning,) = profile_warnings(SellerProfile(is_mse=True, categories=["chair"]), TODAY)
    assert "EMD" in warning
    assert profile_warnings(SellerProfile(is_mse=True, categories=["chair"], own_made_products=["chair"]), TODAY) == []


def test_the_chat_can_propose_the_new_details_and_the_model_is_told_the_warnings(container):
    result = ChatTools(container).call("propose_profile_update", {
        "gem_registered_on": "2023-05-01", "itr_filed_on_gem": False, "oem_products": ["chair"]})
    proposed = result.card["profile"]
    assert (proposed["gem_registered_on"], proposed["itr_filed_on_gem"], proposed["oem_products"]) == (
        "2023-05-01", False, ["chair"])
    container.profiles.save(SellerProfile(gem_registered_on=date(2020, 1, 1), itr_filed_on_gem=False))
    assert any("ITR" in w for w in ChatTools(container).profile()["warnings"])


def test_the_api_lists_the_warnings(client):
    client.put("/api/profile", json={"gem_registered_on": "2020-01-01", "itr_filed_on_gem": False})
    assert any("ITR" in w for w in client.get("/api/profile/warnings").json())
    assert client.get("/api/profile").json()["itr_filed_on_gem"] is False
