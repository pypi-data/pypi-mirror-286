from typing import List
from functools import reduce
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import non_empty_list, flatten, list_sum, is_number

from .term import should_aggregate


def _formatDepth(depth: str):
    # handle float values
    return str(int(depth)) if is_number(depth) else ''


def group_blank_nodes(nodes: list):
    """
    Group a list of blank nodes using:
    - `termType`
    - the `depthUpper` and `depthLower`
    - the `startDate` and `endDate`
    - the `dates`
    - the lookup group `sumMax100Group` or `sumIs100Group` if specified

    Parameters
    ----------
    nodes : list
        List of blank nodes with their index.
    """
    def group_by(group: dict, blank_node: dict):
        term = blank_node.get('term', {})
        term_type = term.get('termType')
        lookup = download_lookup(f"{term_type}.csv")
        sum_below_100_group = get_table_value(lookup, 'termid', term.get('@id'), column_name('sumMax100Group')) \
            if lookup is not None else None
        sum_equal_100_group = get_table_value(lookup, 'termid', term.get('@id'), column_name('sumIs100Group')) \
            if lookup is not None else None
        keys = non_empty_list([
            term_type,
            _formatDepth(blank_node.get('depthUpper')),
            _formatDepth(blank_node.get('depthLower')),
            blank_node.get('startDate'),
            blank_node.get('endDate'),
            '-'.join(blank_node.get('dates', [])),
            sum_below_100_group,
            sum_equal_100_group
        ])
        key = '-'.join(keys)

        group[key] = group.get(key, []) + [{
            'node': blank_node,
            'sumMax100Group': sum_below_100_group,
            'sumIs100Group': sum_equal_100_group
        }]

        return group

    return reduce(group_by, nodes, {})


def _filter_by_array_treatment(blank_node: dict):
    term = blank_node.get('term', {})
    lookup = download_lookup(f"{term.get('termType')}.csv")
    value = get_table_value(lookup, 'termid', term.get('@id'), column_name('arrayTreatmentLargerUnitOfTime'))
    # ignore any blank node with time-split data
    return not value


def _filter_needs_depth(blank_node: dict):
    term = blank_node.get('term', {})
    lookup = download_lookup(f"{term.get('termType')}.csv")
    needs_depth = get_table_value(lookup, 'termid', term.get('@id'), column_name('recommendAddingDepth'))
    return not needs_depth or all([blank_node.get('depthUpper') is not None, blank_node.get('depthLower') is not None])


def _filter_grouped_nodes(blank_nodes: List[dict]):
    values = flatten([v.get('node').get('value', []) for v in blank_nodes])
    total_value = list_sum(values)
    blank_node = blank_nodes[0]
    sum_equal_100 = any([blank_node.get('sumMax100Group'), blank_node.get('sumIs100Group')])
    valid = not sum_equal_100 or 99.5 <= total_value <= 100.5
    return [v.get('node') for v in blank_nodes] if valid else []


def filter_blank_nodes(blank_nodes: List[dict]):
    # make sure `skipAggregation` lookup is not `True`
    nodes = [v for v in blank_nodes if all([
        should_aggregate(v.get('term', {})),
        _filter_by_array_treatment(v),
        _filter_needs_depth(v)
    ])]

    grouped_values = group_blank_nodes(nodes)
    return flatten(map(_filter_grouped_nodes, grouped_values.values()))
