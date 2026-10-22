"""Things in his profile that will cost him bids or money, said before he finds out the hard way."""

from __future__ import annotations

from datetime import date

from .india_states import normalise_states
from .models import SellerProfile
from .wording import day


def _two_years_after(d: date) -> date:
    try:
        return d.replace(year=d.year + 2)
    except ValueError:  # 29 Feb
        return d.replace(year=d.year + 2, month=3, day=1)


def profile_warnings(profile: SellerProfile, today: date) -> list[str]:
    out = []
    registered = profile.gem_registered_on
    if registered and today > _two_years_after(registered) and profile.itr_filed_on_gem is not True:
        known = ("no income tax return (ITR) is filed on GeM" if profile.itr_filed_on_gem is False
                 else "I don't know whether your income tax return (ITR) is filed on GeM")
        out.append(f"You registered on GeM on {day(registered)}, more than 24 months ago, and {known}. "
                   "Without an ITR on GeM you can't bid: file it, then tell me.")
    if profile.pfms_bank_verified is False:
        out.append("Your bank account is not PFMS-verified on GeM: payments for your orders can be held.")
    if profile.is_mse and profile.categories and not profile.own_made_products:
        out.append("You are an MSE but no product is marked as made by you. The EMD exemption applies "
                   "only to items you make yourself, so I will not assume it.")
    unknown = normalise_states(profile.states)[1]
    if unknown:
        out.append(f"I don't recognise these as Indian states: {', '.join(unknown)}. They are ignored when I "
                   "check where a bid delivers; please fix the spelling in your profile.")
    return out
