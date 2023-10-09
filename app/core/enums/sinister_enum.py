from enum import Enum

# POR DEFINIR


class SinisterStatusEnum(str, Enum):
    OPEN = 'Abierta'
    COMPLETED = 'Completado'
    CANCELLED = 'Cancelado'
    APPOINTMENT_ASSIGNED = 'Turno Asignado'
    ARCHIVED = "Archivado"
    AUDITED = "Auditado"
    RETAINED = "Retenida"
    CREATED = "Creado"
    WAITING = 'En Espera'
    CLOSED = 'Cerrado'
    APPROVED = 'Aprobado'


class SinisterTypeEnum(str, Enum):
    CATASTROPHE = "Catastrofe"
    COLITION = "Colisión"
    FIRE = "Incendio"
    ROBBERY = "Robo"
    VANDALISM = "Vandalismo"
    WINDOW_LOCK = "Vidrio/Cerradura"


class SinisterPlaceEnum(str, Enum):
    HIGHWAY = "Autopista"
    AVENUE = "Avenida"
    STREET = "Calle"
    INTERSECTION = "Intersección"
    OTHER = "Otro"
    ROUTE = "Ruta"
