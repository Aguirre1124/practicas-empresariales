from dataclasses import dataclass


@dataclass(frozen=True)
class DatosAcademicosDTO:
    documento_estudiante: str
    porcentaje_creditos_aprobados: float
    matricula_activa: bool
    periodo: str
