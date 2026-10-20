"""Step 1.5: RejectionService for managing rejection reasons, challenge drafts, and past rejections."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Sequence

from ..domain.rejection import (
    DisqualificationAnalysis,
    analyze_rejection,
    check_rejection_warnings,
)
from ..infrastructure.sqlite_repositories import (
    SqliteProfileRepository,
    SqliteRejectionRepository,
)


class RejectionService:
    def __init__(
        self,
        rejection_repo: SqliteRejectionRepository,
        profile_repo: SqliteProfileRepository,
    ):
        self._rejection_repo = rejection_repo
        self._profile_repo = profile_repo

    def analyze(
        self,
        text: str,
        bid_number: str | None = None,
        eval_date: date | None = None,
        now: datetime | None = None,
    ) -> DisqualificationAnalysis:
        profile = self._profile_repo.get()
        return analyze_rejection(
            text=text,
            bid_number=bid_number,
            eval_date=eval_date,
            profile=profile,
            now=now,
        )

    def save_rejection(
        self,
        bid_number: str | None,
        reason_text: str,
        missing_doc: str | None,
        category: str | None = None,
        now: datetime | None = None,
    ) -> int:
        return self._rejection_repo.save_rejection(
            bid_number=bid_number,
            reason_text=reason_text,
            missing_doc=missing_doc,
            category=category,
            now=now,
        )

    def list_history(self) -> list[dict]:
        return self._rejection_repo.list_rejections()

    def get_warnings_for_docs(self, docs: Sequence[str]) -> list[dict]:
        return self._rejection_repo.find_warnings_for_docs(docs)

    def delete_history_item(self, rejection_id: int) -> bool:
        return self._rejection_repo.delete_rejection(rejection_id)
