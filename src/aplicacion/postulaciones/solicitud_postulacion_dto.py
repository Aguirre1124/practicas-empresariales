from dataclasses import dataclass


@dataclass(frozen=True)
class SolicitudPostulacionDTO:
    documento_estudiante: str
    nombre_estudiante: str
    correo_estudiante: str
    nombre_programa: str
    periodo: str
    nombre_empresa: str
    nit_empresa: str
    nombre_supervisor: str
    correo_supervisor: str
    direccion_origen: str = "127.0.0.1"
