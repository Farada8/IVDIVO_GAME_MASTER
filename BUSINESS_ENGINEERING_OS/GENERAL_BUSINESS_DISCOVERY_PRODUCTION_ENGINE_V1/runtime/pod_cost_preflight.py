from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Asset:
    width_px: int
    height_px: int
    content_is_retail_master: bool
    provenance_closed: bool


def effective_dpi(asset: Asset, width_in: float, height_in: float, crop: bool = True) -> float:
    target_ratio = width_in / height_in
    src_ratio = asset.width_px / asset.height_px
    if crop:
        if src_ratio > target_ratio:
            usable_w = asset.height_px * target_ratio
            usable_h = asset.height_px
        else:
            usable_w = asset.width_px
            usable_h = asset.width_px / target_ratio
    else:
        usable_w, usable_h = asset.width_px, asset.height_px
    return min(usable_w / width_in, usable_h / height_in)


def etsy_fee_eur(price_eur: float, usd_to_eur: float = 0.854922) -> float:
    listing_eur = 0.20 * usd_to_eur
    return 0.065 * price_eur + 0.04 * price_eur + 0.30 + listing_eur


def pre_cac_contribution(price_eur: float, product_eur: float, shipping_usd: float,
                         usd_to_eur: float = 0.854922, extra_shipping_usd: float = 0.0) -> float:
    shipping_eur = (shipping_usd + extra_shipping_usd) * usd_to_eur
    return price_eur - product_eur - shipping_eur - etsy_fee_eur(price_eur, usd_to_eur)


def route_asset(asset: Asset, width_in: float, height_in: float, min_dpi: float = 150.0) -> str:
    dpi = effective_dpi(asset, width_in, height_in, crop=True)
    if dpi < min_dpi:
        return "HOLD_RESOLUTION"
    if not asset.content_is_retail_master:
        return "HOLD_CREATE_CLEAN_MASTER"
    if not asset.provenance_closed:
        return "HOLD_PROVENANCE"
    return "ENGINEERING_ELIGIBLE_INTERNAL_MOCKUP"


def can_claim_profitable_sku(*, paid_orders: int, wtp_observed: bool, cac_observed: bool,
                             conversion_observed: bool, contribution_after_cac_positive: Optional[bool]) -> bool:
    return (
        paid_orders > 0
        and wtp_observed
        and cac_observed
        and conversion_observed
        and contribution_after_cac_positive is True
    )


def costs_are_fresh(as_of_iso: str) -> bool:
    # Current Printful catalog announces price changes effective 2026-08-27.
    return as_of_iso < "2026-08-27"
