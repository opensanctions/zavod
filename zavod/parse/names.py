from typing import Optional
from normality import collapse_spaces
from followthemoney.util import join_text

from nomenklatura.entity import CE


def make_name(
    full: Optional[str] = None,
    name1: Optional[str] = None,
    first_name: Optional[str] = None,
    given_name: Optional[str] = None,
    name2: Optional[str] = None,
    second_name: Optional[str] = None,
    middle_name: Optional[str] = None,
    name3: Optional[str] = None,
    patronymic: Optional[str] = None,
    matronymic: Optional[str] = None,
    name4: Optional[str] = None,
    name5: Optional[str] = None,
    tail_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Optional[str]:
    """Provides a standardised way of assembling the components of a human name.
    This does a whole lot of cultural ignorance work, so YMMV."""
    full = collapse_spaces(full)
    if full is not None and len(full) > 1:
        return full
    return join_text(
        name1,
        first_name,
        given_name,
        name2,
        second_name,
        middle_name,
        name3,
        patronymic,
        matronymic,
        name4,
        name5,
        tail_name,
        last_name,
    )


def set_name_part(entity: CE, prop: str, value: Optional[str], quiet: bool) -> None:
    if value is None:
        return
    prop_ = entity.schema.get(prop)
    if prop_ is None:
        if quiet:
            return
        raise TypeError("Invalid prop: %s [value: %r]" % (prop, value))
    entity.unsafe_add(prop_, value)


def apply_name(
    entity: CE,
    full: Optional[str] = None,
    name1: Optional[str] = None,
    first_name: Optional[str] = None,
    given_name: Optional[str] = None,
    name2: Optional[str] = None,
    second_name: Optional[str] = None,
    middle_name: Optional[str] = None,
    name3: Optional[str] = None,
    patronymic: Optional[str] = None,
    matronymic: Optional[str] = None,
    name4: Optional[str] = None,
    name5: Optional[str] = None,
    tail_name: Optional[str] = None,
    last_name: Optional[str] = None,
    maiden_name: Optional[str] = None,
    alias: bool = False,
    name_prop: str = "name",
    is_weak: bool = False,
    quiet: bool = False,
) -> None:
    if not is_weak:
        set_name_part(entity, "firstName", given_name, quiet)
        set_name_part(entity, "firstName", first_name, quiet)
        set_name_part(entity, "secondName", second_name, quiet)
        set_name_part(entity, "fatherName", patronymic, quiet)
        set_name_part(entity, "motherName", matronymic, quiet)
        set_name_part(entity, "lastName", last_name, quiet)
        set_name_part(entity, "lastName", maiden_name, quiet)
        set_name_part(entity, "firstName", name1, quiet)
        set_name_part(entity, "secondName", name2, quiet)
        set_name_part(entity, "middleName", name3, quiet)
        set_name_part(entity, "middleName", name4, quiet)
        set_name_part(entity, "middleName", name5, quiet)
        set_name_part(entity, "lastName", tail_name, quiet)
    if alias:
        name_prop = "alias"
    if is_weak:
        name_prop = "weakAlias"
    full = make_name(
        full=full,
        name1=name1,
        first_name=first_name,
        given_name=given_name,
        name2=name2,
        second_name=second_name,
        middle_name=middle_name,
        name3=name3,
        patronymic=patronymic,
        matronymic=matronymic,
        name4=name4,
        name5=name5,
        tail_name=tail_name,
        last_name=last_name,
    )
    if full is not None and len(full):
        entity.add(name_prop, full, quiet=quiet)
