from hestia_earth.schema import EmissionMethodTier

from hestia_earth.models.utils.cycle import get_excreta_N_total
from hestia_earth.models.utils.emission import _new_emission
from .noxToAirSoilFlux import _should_run, _get_value
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.excreta": "True",
        "inputs": [{
            "@type": "Input",
            "value": "",
            "term.units": ["kg", "kg N"],
            "term.termType": "excreta",
            "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
        }],
        "products": [{
            "@type": "Product",
            "value": "",
            "term.units": ["kg", "kg N"],
            "term.termType": "excreta",
            "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
        }],
        "site": {
            "@type": "Site",
            "measurements": [
                {"@type": "Measurement", "value": "", "term.@id": "totalNitrogenPerKgSoil"},
                {"@type": "Measurement", "value": "", "term.@id": "ecoClimateZone"}
            ]
        }
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 2"
    }]
}
LOOKUPS = {
    "ecoClimateZone": "STEHFEST_BOUWMAN_2006_NOX-N_FACTOR"
}
TERM_ID = 'noxToAirExcreta'
TIER = EmissionMethodTier.TIER_2.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _run(cycle: dict, ecoClimateZone: str, nitrogenContent: float, N_total: float):
    noxToAirSoilFlux = _get_value(cycle, ecoClimateZone, nitrogenContent, N_total, TERM_ID)
    N_excreta = get_excreta_N_total(cycle)
    value = N_excreta / N_total * noxToAirSoilFlux if all([
        N_excreta, N_total
    ]) else 0
    return [_emission(value)]


def run(cycle: dict):
    should_run, ecoClimateZone, nitrogenContent, N_total = _should_run(cycle, TERM_ID, TIER)
    return _run(cycle, ecoClimateZone, nitrogenContent, N_total) if should_run else []
