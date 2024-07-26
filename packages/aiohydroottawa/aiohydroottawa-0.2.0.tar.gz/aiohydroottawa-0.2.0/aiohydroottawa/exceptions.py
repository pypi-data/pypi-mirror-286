"""Exceptions."""


class HydroOttawaError(Exception):
    """Generic Hydro Ottawa Exception."""


class HydroOttawaConnectionError(HydroOttawaError):
    """Error to indicate we cannot connect."""


class HydroOttawaInvalidAuth(HydroOttawaError):
    """Error to indicate there is invalid auth."""
