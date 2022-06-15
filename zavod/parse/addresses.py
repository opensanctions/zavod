from normality import slugify
from functools import lru_cache
from addressformatting import AddressFormatter  # type: ignore
from followthemoney.types import registry
from followthemoney.proxy import E
from followthemoney.util import make_entity_id, join_text

from zavod.context import Zavod


@lru_cache(maxsize=None)
def get_formatter() -> AddressFormatter:
    return AddressFormatter()


def make_address(
    context: Zavod,
    full=None,
    remarks=None,
    summary=None,
    po_box=None,
    street=None,
    street2=None,
    street3=None,
    city=None,
    place=None,
    postal_code=None,
    state=None,
    region=None,
    country=None,
    country_code=None,
    key=None,
) -> E:
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
        data = {
            "attention": summary,
            "house": po_box,
            "road": street,
            "postcode": postal_code,
            "city": city,
            "state": join_text(region, state, sep=", "),
            # "country": country,
        }
        full = get_formatter().one_line(data, country=country_code)  # type: ignore
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
