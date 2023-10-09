from enum import Enum

# POR DEFINIR


class RequestStatusEnum(str, Enum):
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


class RequestTypeEnum(str, Enum):
    PREVENTIVE = "Preventivo"
    CORRECTIVE = "Correctivo"
    VERIFICATIONS = "Verificaciones"
    TIRES = "Gomeria"


class RequestVerTypeEnum(str, Enum):
    VTV = "VTV"
    POLICE_VERIFICATION = "Verificacion Policial"
    VEHICLE_ENGRAVING = "Grabado de Autopartes"
    CRISTALS_ENGRAVING = "Grabado de Cristales"


class RequestTireReasonEnum(str, Enum):
    WEARING = "Desgaste"
    KILOMETERS = "Kilometros"
