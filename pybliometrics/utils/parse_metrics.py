"""Utility functions to parse and extract metrics data from JSON responses."""
from typing import NamedTuple

from pybliometrics.utils import make_int_if_possible

class MetricData(NamedTuple):
    """Global namedtuple for all metric data with default values."""
    entity_id: int | None
    entity_name: str | None
    metric: str | None
    year: str | None = "all"
    value: int | float | None = None
    percentage: float | None = None
    threshold: int | None = None


def extract_metric_data(json_data, metric_type: str, by_year: bool, entity_type: str):
    """Helper function to extract metric data for a specific metric type.
    
    Parameters
    ----------
    json_data : dict
        The JSON response from the API
    metric_type : str
        The metric type to extract
    by_year : bool, optional
        Whether the data is broken down by year
    entity_type : str, optional
        The type of entity ("author", "institution", or "topic")
        
    Returns
    -------
    list or None
        List of MetricData namedtuples or None if no data found
    """
    out = []

    # Get results from JSON data
    if isinstance(json_data, dict):
        results = json_data.get('results', [])
    else:
        results = []

    for result in results:
        entity_id, entity_name = extract_entity_info(result, entity_type)
        metric_data = find_metric_data(result, metric_type)

        if not metric_data:
            continue

        # Process metric data using unified approach
        metric_items = process_metric(metric_data, entity_id, entity_name, metric_type, by_year)
        if metric_items:
            out.extend(metric_items)

    return out or None

def extract_metric_lists(json_data, metric_type: str, entity_type: str) -> list:
    out = []

    # Get results from JSON data
    if isinstance(json_data, dict):
        results = json_data.get('results', [])
    else:
        results = []

    for result in results:
        entity_id, entity_name = extract_entity_info(result, entity_type)
        metric_data = find_metric_data(result, metric_type)

        if not metric_data:
            continue

        metric_values = metric_data.get('values', [])
        out.append({
            "entity_id": entity_id,
            "entity_name": entity_name,
            "values": metric_values
        })
    return out


def extract_entity_info(result: dict, entity_type: str) -> tuple:
    """Extract entity ID and name from a result.
    
    Parameters
    ----------
    result : dict
        Entity result from API response
    entity_type : str
        The type of entity ("author", "institution", or "topic")
        
    Returns
    -------
    tuple
        (entity_id, entity_name)
    """
    entity_data = result.get(entity_type, {})
    entity_id = make_int_if_possible(entity_data.get('id'))
    entity_name = entity_data.get('name')
    return entity_id, entity_name


def find_metric_data(result: dict, metric_type: str):
    """Find specific metric data in the metrics list.
    
    Parameters
    ----------
    result : dict
        Author result from API response
    metric_type : str
        The metric type to find
        
    Returns
    -------
    dict or None
        The metric data or None if not found
    """
    metrics = result.get('metrics', [])
    for metric in metrics:
        if metric.get('metricType') == metric_type:
            return metric
    return None


def process_metric(metric_data: dict, entity_id: int, entity_name: str, metric_type: str, by_year: bool = False):
    """Unified function to process all metric types.
    
    Parameters
    ----------
    metric_data : dict
        The metric data from API response
    entity_id : int
        Entity ID (author or institution)
    entity_name : str
        Entity name (author or institution)
    metric_type : str
        The metric type
    by_year : bool, optional
        Whether the data is broken down by year
        
    Returns
    -------
    list or None
        List of MetricData namedtuples or None if no data
    """
    out = []

    # Normalize all metrics to have a 'values' structure
    if 'values' in metric_data:
        # Already has multiple values (collaboration/threshold metrics)
        values_list = metric_data['values']
    else:
        # Simple metric - wrap in a list to make it uniform
        values_list = [metric_data]

    # Process all value items uniformly
    for value_item in values_list:
        # Extract type-specific information - just try to get them, default to None
        collab_type = value_item.get('collabType')
        threshold = value_item.get('threshold')

        # Normalize data structure: convert single values to year-keyed dictionaries
        if by_year:
            value_data = value_item.get('valueByYear', {})
            percentage_data = value_item.get('percentageByYear', {})
        else:
            value_data = {"all": value_item.get('value')}
            percentage_data = {"all": value_item.get('percentage')}

        # Process all years uniformly
        for year in value_data.keys():
            # For nested metrics (like Collaboration), metric is the specific type (collabType)
            # For simple metrics (like CitationCount), metric is the metric_type itself
            metric_name = collab_type or value_item.get('indexType') or value_item.get('impactType') or metric_type

            new = MetricData(
                entity_id=entity_id,
                entity_name=entity_name,
                metric=metric_name,
                year=str(year),
                value=value_data.get(year),
                percentage=percentage_data.get(year),
                threshold=threshold
            )
            out.append(new)

    return out if out else None
