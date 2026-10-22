"""Tells him about alerts outside the app (step 5.2): a Mac notification, and an email if set up.

Outbound only: nothing here reads a reply or takes a command. Each alert is announced once
(remembered in a small file in the data folder); one message per round, not one per alert.
"""

from __future__ import annotations

import json
import smtplib
import subprocess
import sys
import threading
from email.message import EmailMessage
from pathlib import Path
from typing import Callable, Sequence

Channel = Callable[[str, str], None]  # (title, body) -> raises on failure


def mac_channel(title: str, body: str) -> None:
    # Text goes in as arguments, never spliced into the script, so an odd bid text cannot become code.
    script = "on run argv\ndisplay notification (item 2 of argv) with title (item 1 of argv)\nend run"
    subprocess.run(["osascript", "-e", script, title, body[:240]], check=True, capture_output=True, timeout=15)


def email_channel(user: str, password: str, to: str, host: str = "smtp.gmail.com", port: int = 465) -> Channel:
    def send(title: str, body: str) -> None:
        message = EmailMessage()
        message["Subject"], message["From"], message["To"] = title, user, to
        message.set_content(body)
        with smtplib.SMTP_SSL(host, port, timeout=30) as smtp:
            smtp.login(user, password)
            smtp.send_message(message)
    return send


def channels_from_env(env: dict[str, str]) -> list[Channel]:
    """Mac notification on a Mac unless GEM_NOTIFY_MAC=0; email only when the Gmail app password is set."""
    found: list[Channel] = []
    if sys.platform == "darwin" and env.get("GEM_NOTIFY_MAC", "1") != "0":
        found.append(mac_channel)
    user, password = env.get("GEM_SMTP_USER", "").strip(), env.get("GEM_SMTP_APP_PASSWORD", "").replace(" ", "")
    if user and password:
        found.append(email_channel(user, password, env.get("GEM_NOTIFY_TO", "").strip() or user))
    return found


class AlertNotifier:
    def __init__(self, alert_sources: Sequence[Callable[[], list[dict]]], channels: Sequence[Channel], seen_file: Path):
        self._sources, self._channels, self._seen_file = alert_sources, channels, seen_file

    def _seen(self) -> set[str]:
        try:
            return set(json.loads(self._seen_file.read_text()))
        except (OSError, ValueError):
            return set()

    def notify_new(self) -> int:
        """Announce alerts not announced before. Returns how many were announced."""
        rows = [row for source in self._sources for row in source()]
        key = lambda r: f"{r['kind']}|{r['ref']}|{r['due']}"  # noqa: E731
        seen = self._seen()
        new = [r for r in rows if key(r) not in seen]
        if not new or not self._channels:
            return 0
        title = f"GeM Assistant: {len(new)} new alert{'s' if len(new) != 1 else ''}"
        body = "\n".join(f"{r['label']}: {r['ref']} ({r['due_text']})" for r in new)
        delivered = False
        for channel in self._channels:
            try:
                channel(title, body)
                delivered = True
            except Exception as error:  # one broken channel must not hide the others
                print(f"alert notification failed: {type(error).__name__}", file=sys.stderr)
        if not delivered:
            return 0  # try again next round
        # Remember only what is still open, so the file stays small and a returning alert is announced again.
        self._seen_file.write_text(json.dumps(sorted({key(r) for r in rows})))
        self._seen_file.chmod(0o600)
        return len(new)

    def start(self, every_seconds: int = 600) -> None:
        stop = threading.Event()

        def loop() -> None:
            while True:
                try:
                    self.notify_new()
                except Exception as error:
                    print(f"alert round failed: {type(error).__name__}", file=sys.stderr)
                if stop.wait(every_seconds):
                    return
        threading.Thread(target=loop, daemon=True, name="gem-alert-notifier").start()
