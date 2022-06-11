from lxml import etree


def remove_namespace(el: etree._Element) -> etree._Element:
    """Remove namespace in the passed XML/HTML document in place and
    return an updated element tree.

    If the namespaces in a document define multiple tags with the same
    local tag name, this will create ambiguity and lead to errors. Most
    XML documents, however, only actively use one namespace."""
    for elem in el.iter():
        elem.tag = etree.QName(elem).localname
    etree.cleanup_namespaces(el)
    return el
