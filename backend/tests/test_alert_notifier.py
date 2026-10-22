"""Step 5.2: outside-the-app alerts. Channels are fakes; nothing is really sent."""

import json

import pytest

from gem_assistant.services import alert_notifier as mod
from gem_assistant.services.alert_notifier import AlertNotifier, channels_from_env


def _row(ref, due="2026-10-25"):
    return {"kind": "bid_closing", "ref": ref, "due": due, "label": "Bid closing soon", "due_text": "by Sun"}


def test_each_alert_is_announced_once_in_one_message(tmp_path):
    sent, rows = [], [_row("A"), _row("B")]
    notifier = AlertNotifier([lambda: rows], [lambda t, b: sent.append((t, b))], tmp_path / "seen.json")
    assert notifier.notify_new() == 2
    assert len(sent) == 1 and "2 new alerts" in sent[0][0] and "A" in sent[0][1] and "B" in sent[0][1]
    assert notifier.notify_new() == 0 and len(sent) == 1
    rows.append(_row("C"))
    assert notifier.notify_new() == 1 and "C" in sent[1][1] and "A" not in sent[1][1]


def test_a_failed_send_is_retried_and_one_bad_channel_does_not_hide_the_other(tmp_path):
    def broken(t, b):
        raise OSError("no network")
    sent = []
    only_broken = AlertNotifier([lambda: [_row("A")]], [broken], tmp_path / "s1.json")
    assert only_broken.notify_new() == 0 and not (tmp_path / "s1.json").exists()
    both = AlertNotifier([lambda: [_row("A")]], [broken, lambda t, b: sent.append(b)], tmp_path / "s2.json")
    assert both.notify_new() == 1 and len(sent) == 1


def test_channels_follow_the_settings(monkeypatch):
    monkeypatch.setattr(mod.sys, "platform", "darwin")
    assert channels_from_env({}) == [mod.mac_channel]
    assert channels_from_env({"GEM_NOTIFY_MAC": "0"}) == []
    assert len(channels_from_env({"GEM_SMTP_USER": "a@gmail.com", "GEM_SMTP_APP_PASSWORD": "abcd efgh"})) == 2
    assert len(channels_from_env({"GEM_SMTP_USER": "a@gmail.com"})) == 1   # no password: no email
    monkeypatch.setattr(mod.sys, "platform", "linux")
    assert channels_from_env({}) == []


def test_email_uses_gmail_ssl_with_the_app_password(monkeypatch):
    calls = []

    class FakeSMTP:
        def __init__(self, host, port, timeout): calls.append(("connect", host, port))
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, password): calls.append(("login", user, password))
        def send_message(self, m): calls.append(("to", m["To"], m["Subject"]))

    monkeypatch.setattr(mod.smtplib, "SMTP_SSL", FakeSMTP)
    mod.email_channel("me@gmail.com", "pw", "me@gmail.com")("Title", "Body")
    assert calls == [("connect", "smtp.gmail.com", 465), ("login", "me@gmail.com", "pw"),
                     ("to", "me@gmail.com", "Title")]


def test_mac_notification_passes_text_as_arguments(monkeypatch):
    run = []
    monkeypatch.setattr(mod.subprocess, "run", lambda cmd, **kw: run.append(cmd))
    mod.mac_channel('T"; do shell script "x', "body")
    assert run[0][-2:] == ['T"; do shell script "x', "body"] and "shell script" not in run[0][2]
