from datetime import date, datetime, timezone

import pytest

from gem_assistant.domain.wording import DRAFT_NOTE, check_draft, deadline

NOW = datetime(2026, 10, 20, 6, 30, tzinfo=timezone.utc)  # Tue 20 Oct 2026, 12:00 PM in India


@pytest.mark.parametrize("due, expected", [
    # Timed deadlines are shown in Indian time, never UTC.
    (datetime(2026, 10, 23, 11, 30, tzinfo=timezone.utc), "by Fri 23 Oct 2026, 5:00 PM (3 days left)"),
    (datetime(2026, 10, 20, 12, 30, tzinfo=timezone.utc), "by today, 6:00 PM (6 hours left)"),
    (datetime(2026, 10, 20, 6, 50, tzinfo=timezone.utc), "by today, 12:20 PM (less than 1 hour left)"),
    (datetime(2026, 10, 21, 3, 30, tzinfo=timezone.utc), "by tomorrow, Wed 21 Oct 2026, 9:00 AM (21 hours left)"),
    (datetime(2026, 10, 19, 6, 30, tzinfo=timezone.utc), "missed: was due Mon 19 Oct 2026, 12:00 PM (1 day ago)"),
    # 6:00 PM UTC is already the next day in India.
    (datetime(2026, 10, 21, 18, 30, tzinfo=timezone.utc), "by Thu 22 Oct 2026, 12:00 AM (2 days left)"),
    # Date-only deadlines count whole days; "by" means the end of that day.
    (date(2026, 10, 30), "by Fri 30 Oct 2026 (10 days left)"),
    (date(2026, 10, 21), "by tomorrow, Wed 21 Oct 2026"),
    (date(2026, 10, 20), "by today, Tue 20 Oct 2026"),
    (date(2026, 10, 17), "missed: was due Sat 17 Oct 2026 (3 days ago)"),
])
def test_deadline_wording(due, expected):
    assert deadline(due, NOW) == expected


def test_deadline_refuses_a_time_without_a_zone():
    with pytest.raises(ValueError):
        deadline(datetime(2026, 10, 23, 17, 0), NOW)


GOOD = (f"{DRAFT_NOTE}\n\nTo: Buyer, Bid GEM/2026/B/1234567\n"
        "Subject: Documents asked in your clarification\n\n"
        "Please find attached [attach: OEM authorisation].")


def test_a_good_draft_passes():
    assert check_draft(GOOD) == []


def test_a_draft_must_start_with_the_draft_note():
    assert check_draft(GOOD.replace(DRAFT_NOTE, "")) == ["must start with the draft note"]


@pytest.mark.parametrize("phrase", [
    "We have submitted the documents for you.",
    "The app sent this to the buyer.",
    "Order accepted on your behalf.",
    "Uploaded automatically.",
    "You are eligible for this bid.",
    "You will definitely win.",
    "Payment is guaranteed by 30 Oct.",
    "This is 100% safe.",
])
def test_a_draft_must_not_claim_the_app_acted_or_promise(phrase):
    problems = check_draft(f"{GOOD}\n{phrase}")
    assert len(problems) == 1 and problems[0].startswith("says ")


def test_a_draft_must_not_carry_pan_or_bank_details():
    assert check_draft(f"{GOOD}\nPAN ABCDE1234F") == ["contains a PAN; leave it out, GeM already has it"]
    assert check_draft(f"{GOOD}\nIFSC SBIN0001234") == ["contains an IFSC/bank detail; leave it out"]
