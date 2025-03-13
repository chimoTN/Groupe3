# domain/exceptions.py

class NotFoundException(Exception):
    """Exception levée lorsqu'une entité n'est pas trouvée."""
    pass

class InvalidOperationException(Exception):
    """Exception levée lorsqu'une opération n'est pas valide dans l'état actuel."""
    pass

class ValidationException(Exception):
    """Exception levée lorsqu'une validation échoue."""
    pass

class ClientNotFoundException(NotFoundException):
    """Exception levée lorsqu'un client n'est pas trouvé."""
    pass

class ClientAlreadyExistsException(Exception):
    """Exception levée lorsqu'un client existe déjà."""
    pass

class VehiculeNotFoundException(NotFoundException):
    """Exception levée lorsqu'un véhicule n'est pas trouvé."""
    pass

class VehiculeNotAvailableException(InvalidOperationException):
    """Exception levée lorsqu'un véhicule n'est pas disponible."""
    pass

class AssuranceNotFoundException(NotFoundException):
    """Exception levée lorsqu'une assurance n'est pas trouvée."""
    pass

class AssuranceAlreadyExistsException(Exception):
    """Exception levée lorsqu'une assurance existe déjà."""
    pass

class ContratNotFoundException(NotFoundException):
    """Exception levée lorsqu'un contrat n'est pas trouvé."""
    pass

class ContratNotActiveException(InvalidOperationException):
    """Exception levée lorsqu'un contrat n'est pas actif."""
    pass

class InvalidDevisPriceException(ValidationException):
    """Exception levée lorsque le prix du devis est invalide."""
    pass

class VehiculeNotEligibleForDevisException(InvalidOperationException):
    """Exception levée lorsque le véhicule n'est pas éligible pour un devis."""
    pass
