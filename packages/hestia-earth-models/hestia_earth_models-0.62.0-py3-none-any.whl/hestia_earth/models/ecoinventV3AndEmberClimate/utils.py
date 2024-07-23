from typing import Dict, Any, Union, List

from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data
from hestia_earth.utils.tools import safe_parse_float, non_empty_list

from hestia_earth.models.log import debugMissingLookup
from hestia_earth.models.data.ecoinventV3 import ecoinventV3_emissions


EMBER_ECOINVENT_LOOKUP_NAME = "ember-ecoinvent-mapping.csv"


def _lookup_data(term_id: str, grouping: str, country_id: str, year: str, lookup_name: str, **log_args):
    lookup = download_lookup(lookup_name)
    column = column_name(grouping)
    data = get_table_value(lookup, 'termid', country_id, column)
    percentage = extract_grouped_data(data, year)
    debugMissingLookup(lookup_name, 'termid', country_id, column, percentage, year=year, term=term_id, **log_args)
    return safe_parse_float(percentage, None)


def _convert_name(name: str) -> str: return name.replace(";", ",")


def _zero_from_non_numeric(value: Any) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def _extract_emission_value(value_iter: Any) -> Union[float, None]:
    value_list = list(value_iter)
    try:
        if len(list(value_list)) > 0 and len(list(value_list)[0]) > 1:
            return safe_parse_float(list(value_list)[0][1])
    except ValueError:
        return None


def _get_emission_rate_per_source(ember_ecoinvent_mapping: Dict, emission_term_id: str) -> Dict:
    """
    Returns the emissions rate in kg/kWh as a mapping indexed by ember energy source name.
    eg: {"bioenergy": 0.8947372128046288, "coal": 0.000124581084822, ... }
    """

    return {
        ember_source: _extract_emission_value(filter(
            lambda x: x[0] == emission_term_id,
            ecoinventV3_emissions(ecoinvent_lookup["ecoinventname"])
        ))
        for ember_source, ecoinvent_lookup in ember_ecoinvent_mapping.items()
    }


def get_emission(term_id: str, country: str, year: int, energy: float, model: str) -> float:
    """
    Get the <term_id> emissions in kg for the energy consumed.
        a: ecoInventId of each source        - from "ember-ecoinvent-mapping.csv"
        b: Ember sources list                - from b
        c: Percentages per source            - from region-ember-energySources.csv (country, ember-source, year:value)
        d: Energy per source (kWh)           - from energy * each of c
        e: Emissions/kWh per source          - from ecoinvent (using id from b)
        f: Emissions per source (kg)         - from e * d for each source
        g: Total emissions                   - from sum(f)
    """
    # a: ecoInventId of each source
    ember_ecoinvent_lookup = download_lookup(EMBER_ECOINVENT_LOOKUP_NAME)
    ember_ecoinvent_mapping = {
        row["ember"].lower(): {"ecoinventid": row["ecoinventid"], "ecoinventname": _convert_name(row["ecoinventname"])}
        for row in ember_ecoinvent_lookup
    }

    # b: Ember sources
    ember_sources = list(ember_ecoinvent_mapping.keys())

    # c: Percentages per source
    percentages_per_source = {
        source: _lookup_data(
            term_id=source,
            grouping=source,
            country_id=country,
            year=str(year),
            lookup_name="region-ember-energySources.csv",
            model=model
        )
        for source in ember_sources
    }

    # d: Energy per source (kWh)
    energy_per_source = {
        source: energy * _zero_from_non_numeric(percentage) / 100
        for source, percentage in percentages_per_source.items()
    }

    # e: Emissions/kWh per source
    emission_rate_per_source = _get_emission_rate_per_source(
        ember_ecoinvent_mapping=ember_ecoinvent_mapping,
        emission_term_id=term_id
    )

    # f: Emissions per source (kg)
    emissions_per_source = {
        source: energy_per_source[source] * emission_rate_per_source[source]
        for source in ember_sources
        if energy_per_source[source] is not None and emission_rate_per_source[source] is not None
    }

    # g: Total emissions (kg of <term_id>)
    return sum(emissions_per_source.values())


def get_all_emission_terms() -> List[str]:
    ember_ecoinvent_lookup = download_lookup(EMBER_ECOINVENT_LOOKUP_NAME)
    eco_invent_name = _convert_name(ember_ecoinvent_lookup[0]["ecoinventname"])
    return [e[0] for e in non_empty_list(ecoinventV3_emissions(eco_invent_name))]
