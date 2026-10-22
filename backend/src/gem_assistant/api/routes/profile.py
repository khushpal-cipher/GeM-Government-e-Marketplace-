from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Request

from ...domain.models import SellerProfile
from ...domain.profile_warnings import profile_warnings

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=SellerProfile | None)
def get_profile(request: Request) -> SellerProfile | None:
    return request.app.state.container.profiles.get()


@router.put("", response_model=SellerProfile)
def save_profile(profile: SellerProfile, request: Request) -> SellerProfile:
    return request.app.state.container.profiles.save(profile)


@router.get("/spec-names", response_model=list[str])
def get_spec_names(request: Request) -> list[str]:
    return request.app.state.container.bid_query.spec_names()


@router.get("/warnings", response_model=list[str])
def get_warnings(request: Request) -> list[str]:
    profile = request.app.state.container.profiles.get()
    return profile_warnings(profile, date.today()) if profile else []
