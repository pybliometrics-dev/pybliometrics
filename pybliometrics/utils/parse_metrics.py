"""Utility functions to parse and extract metrics data from JSON responses."""
from collections import namedtuple

from pybliometrics.utils import make_int_if_possible

# Global namedtuple for all metric data with default values
MetricData = namedtuple('MetricData', 
                       'author_id author_name metric metric_type year value percentage threshold',
                       defaults=(None, None, None, None, "all", None, None, None))


def extract_metric_data(json_data, metric_type: str, by_year: bool = False):
    """Helper function to extract metric data for a specific metric type.
    
    Parameters
    ----------
    json_data : dict
        The JSON response from the API
    metric_type : str
        The metric type to extract
    by_year : bool, optional
        Whether the data is broken down by year
        
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
        author_id, author_name = extract_author_info(result)
        metric_data = find_metric_data(result, metric_type)

        if not metric_data:
            continue

        # Process metric data using unified approach
        metric_items = process_metric(metric_data, author_id, author_name, metric_type, by_year)
        if metric_items:
            out.extend(metric_items)

    return out or None


def extract_author_info(result: dict) -> tuple:
    """Extract author ID and name from a result.
    
    Parameters
    ----------
    result : dict
        Author result from API response
        
    Returns
    -------
    tuple
        (author_id, author_name)
    """
    author_data = result.get('author', {})
    author_id = make_int_if_possible(author_data.get('id'))
    author_name = author_data.get('name')
    return author_id, author_name


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


def process_metric(metric_data: dict, author_id: int, author_name: str, metric_type: str, by_year: bool = False):
    """Unified function to process all metric types.
    
    Parameters
    ----------
    metric_data : dict
        The metric data from API response
    author_id : int
        Author ID
    author_name : str
        Author name
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
            new = MetricData(
                author_id=author_id,
                author_name=author_name,
                metric=metric_type,
                metric_type=collab_type or value_item.get('indexType') or value_item.get('impactType'),
                year=str(year),
                value=value_data.get(year),
                percentage=percentage_data.get(year),
                threshold=threshold
            )
            out.append(new)

    return out if out else None
