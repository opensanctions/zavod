import os
from typing import Optional
from normality import slugify

PathLike = os.PathLike[str]


def join_slug(
    *parts: Optional[str],
    prefix: Optional[str] = None,
    sep: str = "-",
    strict: bool = True
) -> Optional[str]:
    # SLUG_REMOVE = re.compile(r"[<>\\\'\\\"’‘]")
    sections = [slugify(p, sep=sep) for p in parts]
    if strict and None in sections:
        return None
    texts = [p for p in sections if p is not None]
    if not len(texts):
        return None
    prefix = slugify(prefix, sep=sep)
    if prefix is not None:
        texts = [prefix, *texts]
    return sep.join(texts)
