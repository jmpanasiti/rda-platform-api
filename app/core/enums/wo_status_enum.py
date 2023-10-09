from enum import Enum


class StatusEnum(str, Enum):
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
    # WAITING_CLIENT_RESPONSE = 'Waiting Client Response'
    # WAITING_PROVIDER_RESPONSE = "Waiting Provider Response"
    # WAITING_RDA_RESPONSE = "Waiting RDA Response"
    # WAITING_USER_RESPONSE = "Waiting User Response"
    # WAITING_INSURANCE_RESPONSE = "Waiting Insurance Response"
    # WAITING_MANAGER = "Waiting Manager"
    # WAITIGN_RESOLVE = "Waiting Resolve"
    # WAITING_REPLACEMENT = "Waiting Replacement"
    # WAITING_DOCUMENTATION = "Waiting Documentation"
    # PROCESSING_PAYMENT = "Processing Payment"
    # FIXED_STATE = "Fixed State"
    # OP_CONTROL_NOT_STARTED = "Operations Control Not Started"
    # OP_CONTROL_IN_PROGRESS = "Operations Control In Progress"
    # REVISION_AGENT = "Revision Agent"
    # REVISION_FINAL = "Revision Final"
    # REVISION_FINAL_UR = "Revision Final UR"
    # CONFIRMING_INFO = "Confirming Information"
    # OT_OBSERVED = "OT Observed"
    # RESCHEDULE_ASSIGMENT = "Reschedule Assigment"
    # PROVISIONAL_DELIVERED = "Provisional Delivered"
