from typing import Protocol

from aplicacion.postulaciones.datos_academicos_dto import DatosAcademicosDTO


class ConsultaAcademica(Protocol):
    def consultar_datos_academicos(
        self,
        documento_estudiante: str,
        periodo: str,
        tiempo_limite_segundos: float = 5.0,
    ) -> DatosAcademicosDTO: ...
