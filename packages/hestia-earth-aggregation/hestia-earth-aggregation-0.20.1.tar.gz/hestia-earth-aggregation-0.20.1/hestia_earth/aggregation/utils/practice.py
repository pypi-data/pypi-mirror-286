from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type

from .blank_node import filter_blank_nodes


_PRACTICE_AGGREGATE_COMPLETE_TERM_TYPES = [
    TermTermType.CROPRESIDUEMANAGEMENT.value,
    TermTermType.LANDCOVER.value,
    TermTermType.TILLAGE.value,
    TermTermType.WATERREGIME.value
]
_PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES = [
    TermTermType.LANDUSEMANAGEMENT.value
]


def is_complete(node: dict, term_type: str):
    practices = filter_list_term_type(node.get('practices', []), [term_type])
    return len(filter_blank_nodes(practices)) > 0 if term_type in _PRACTICE_AGGREGATE_COMPLETE_TERM_TYPES \
        else False


def filter_practices(practices: list):
    return filter_blank_nodes(filter_list_term_type(practices, _PRACTICE_AGGREGATE_COMPLETE_TERM_TYPES)) + [
        p for p in filter_list_term_type(practices, _PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES)
        if p.get('term', {}).get('units') in ['ratio', 'number', 'days']
    ]
