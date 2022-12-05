from typing import Optional
from normality import slugify
from functools import cache, lru_cache
from addressformatting import AddressFormatter
from followthemoney.types import registry
from nomenklatura.entity import CE
from followthemoney.util import make_entity_id, join_text

from zavod.context import GenericZavod
from zavod.dataset import ZD


@cache
def get_formatter() -> AddressFormatter:
    return AddressFormatter()


@lru_cache(maxsize=200000)
def format_line(
    summary: Optional[str],
    po_box: Optional[str],
    street: Optional[str],
    postal_code: Optional[str],
    city: Optional[str],
    state: Optional[str],
    country_code: Optional[str],
) -> str:
    data = {
        "attention": summary,
        "house": po_box,
        "road": street,
        "postcode": postal_code,
        "city": city,
        "state": state,
    }
    return get_formatter().one_line(data, country=country_code)


def make_address(
    context: GenericZavod[CE, ZD],
    full: Optional[str] = None,
    remarks: Optional[str] = None,
    summary: Optional[str] = None,
    po_box: Optional[str] = None,
    street: Optional[str] = None,
    street2: Optional[str] = None,
    street3: Optional[str] = None,
    city: Optional[str] = None,
    place: Optional[str] = None,
    postal_code: Optional[str] = None,
    state: Optional[str] = None,
    region: Optional[str] = None,
    country: Optional[str] = None,
    country_code: Optional[str] = None,
    key: Optional[str] = None,
) -> CE:
    """Generate an address schema object adjacent to the main entity."""

    city = join_text(place, city, sep=", ")
    street = join_text(street, street2, street3, sep=", ")

    address = context.make("Address")
    address.add("full", full)
    address.add("remarks", remarks)
    address.add("summary", summary)
    address.add("postOfficeBox", po_box)
    address.add("street", street)
    address.add("city", city)
    address.add("postalCode", postal_code)
    address.add("region", region)
    address.add("state", state, quiet=True)
    address.add("country", country)
    address.add("country", country_code)

    country_code = address.first("country")
    if not address.has("full"):
        full = format_line(
            summary=summary,
            po_box=po_box,
            street=street,
            postal_code=postal_code,
            city=city,
            state=join_text(region, state, sep=", "),
            country_code=country_code,
        )
        address.add("full", full)

    full_country = registry.country.clean(full)
    if full_country is not None:
        address.add("country", full_country)
        # full = None

    # full = clean_address(full)
    address.set("full", full)

    if full:
        norm_full = slugify(full)
        hash_id = make_entity_id(country_code, norm_full, key)
        if hash_id is not None:
            address.id = f"addr-{hash_id}"
    return address
