from enum import Enum


class VehicleTypeEnum(str, Enum):
    AUTOELEVATOR = 'Autoelevador'
    AUTOMOTOR = 'Automotor'
    TRUCK = 'Camion'
    BOGIE = 'Carreton'
    VAN = 'Furgon'
    UTILITY_VAN = 'Furgon utilitario'
    BIKE = 'Moto'
    PICK_UP = 'Pick up'
    SUV = 'SUV'
    ALL_TERRAIN = 'Todo terreno'
    TRACTOR = 'Tractor'
    PASSENGER_TRANSPORT = 'Transporte de pasajeros'
    UTILITY = 'Utilitario'


class FuelTypeEnum(str, Enum):
    PETROL = 'Nafta'
    DIESEL = 'Diesel'
    ELECTRIC = 'Electrico'
    HYBRID = 'Hibrido'


class OwnershipEnum(str, Enum):
    RDA = 'RDA'
    CLIENT = 'Cliente'
    BANK = 'Banco'


class CoverageTypeEnum(str, Enum):
    CIVIL = 'Responsabilidad civil'
    ALL_RISK = 'Todo Riesgo'
    THIRDS = 'Terceros completo'
    AUTO = 'Autoaseguro'
    O_COVERAGE = 'Cobertura O'


class PurchaseTypeEnum(str, Enum):
    FACTORY = 'Fabrica'
    IMPROTER = 'Importador'
    CONCESSIONAIRE = 'Concesionario'


class VehicleStatusEnum(str, Enum):
    ACTIVE = 'Activo'
    INACTIVE = 'Inactivo'
    ON_PROCESS_REGISTER = 'En proceso de alta'
    ON_PROCESS_UNREGISTER = 'En proceso de baja'
    VERIFY = 'Verificar'
    MODERATE = 'Moderar'
    SUSPENDED = 'Suspendido'
    SUPERCARS = 'SuperAutos'
    PATENTING = 'Patentamiento'
    ASSUREMENT = 'Aseguramiento'
    EQUIPMENT = 'Equipamiento'
    TELEMETRY_COMPLETED = 'Telemetria completado'
    REQUEST_COMPLETED = 'Pedido Completo'
    PURCHASE_COMPLETED = 'Compras Completo'
    MANAGEMENT_COMPLETED = 'Gestoria Completo'
    ASSURANCE_COMPLETED = 'Seguro Completo'
    LOGISTICS_COMPLETED = 'Logistica Completo'
    MANAGEMENT_DOMAIN_UPDATED = 'Gestoria - Dominio Actualizado'
    TOTAL_DESTRUCTION = 'Destrucción Total'
