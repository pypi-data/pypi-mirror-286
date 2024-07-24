from typing import Dict, List, Union


def adapt_dashboard_with_datasources(dash: Dict, datasources: List) -> Dict:
    """Adapt dashboard with data sources."""

    def get_uid(ds_type: str) -> Union[str, None]:
        for ds in datasources:
            if ds_type == ds["datasource"]["type"]:
                return ds["datasource"]["uid"]
        return None

    panels: List = dash["dashboard"]["panels"]
    for panel in panels:
        ds_uid: str = ""
        if "datasource" in panel:
            ds_type = panel["datasource"]["type"]
            ds_uid = get_uid(ds_type=ds_type)
            panel["datasource"]["uid"] = ds_uid
        if "targets" in panel:
            for target in panel["targets"]:
                target["datasource"]["uid"] = ds_uid
    return dash


def adapt_filters_with_data_sources(filters: List, data_sources: List) -> List[Dict]:
    def get_uid(ds_type: str) -> Union[str, None]:
        for ds in data_sources:
            if ds_type == ds["datasource"]["type"]:
                return ds["datasource"]["uid"]
        return None

    for fil in filters:
        if "datasource" in fil:
            ds_type = fil["datasource"]["type"]
            ds_uid = get_uid(ds_type=ds_type)
            fil["datasource"]["uid"] = ds_uid
    return filters


def adapt_constant_variables(constants: List, adapt: Dict) -> List[Dict]:
    """
    Method that allows you to dynamize Grafana constants, where
    you search for the key query and the type of value that
    that constant contains. Currently "ORGNAME", to later assign
    the value, in particular whenever we talk about ORG we refer to SLUG.

    Parameters
    ----------
    constants: List[Dict]
        _.
    adapt: Dict
        Example:
            {"ORGNAME": 'delibreads'}
            IN
            {
                "hide": 2,
                "name": "slug",
                "query": "ORGNAME",
                "skipUrlSync": False,
                "type": "constant",
            }

    Returns
    -------
    List[Dict]
    """
    for constant in constants:
        key: str = list(adapt.keys())[0]
        if constant["query"] == key:
            constant["query"] = adapt[key]
    return constants


def adapt_dashboard_with_variables(dash: Dict, variables: List) -> Dict:
    dash["dashboard"]["templating"]["list"] = variables
    return dash
