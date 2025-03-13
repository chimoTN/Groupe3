class ContratLocationError(Exception):
    """Classe de base pour les erreurs liées aux contrats de location"""
    pass


class ClientInexistantError(ContratLocationError):
    """Erreur levée quand le client n'existe pas"""
    pass


class VehiculeInexistantError(ContratLocationError):
    """Erreur levée quand le véhicule n'existe pas"""
    pass


class AssuranceInexistanteError(ContratLocationError):
    """Erreur levée quand l'assurance n'existe pas"""
    pass


class VehiculeNonDisponibleError(ContratLocationError):
    """Erreur levée quand le véhicule n'est pas disponible"""
    pass


class DateInvalideError(ContratLocationError):
    """Erreur levée quand la date est invalide"""
    pass


class EnregistrementContratError(ContratLocationError):
    """Erreur levée lors de l'échec d'enregistrement du contrat"""
    pass