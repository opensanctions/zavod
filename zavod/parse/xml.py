from lxml import etree


def remove_namespace(el: etree._Element) -> etree._Element:
    """Remove all namespace details from the given XML document."""
    for elem in el.iter():
        elem.tag = etree.QName(elem).localname
    etree.cleanup_namespaces(el)
    return el
