from aplicacion.postulaciones.datos_academicos_dto import DatosAcademicosDTO


class AdaptadorSIAMemoria:
    def __init__(self) -> None:
        self._registros: dict[tuple[str, str], DatosAcademicosDTO] = {}
        self._disponible: bool = True
        self._fallas_pendientes: int = 0
        self.consultas_realizadas: int = 0

    def registrar_estudiante(self, datos: DatosAcademicosDTO) -> None:
        clave = (datos.documento_estudiante.strip(), datos.periodo.strip())
        self._registros[clave] = datos

    def configurar_disponibilidad(self, disponible: bool) -> None:
        self._disponible = disponible

    def programar_fallas(self, cantidad_fallas: int) -> None:
        self._fallas_pendientes = max(0, cantidad_fallas)

    def consultar_datos_academicos(
        self,
        documento_estudiante: str,
        periodo: str,
        tiempo_limite_segundos: float = 5.0,
    ) -> DatosAcademicosDTO:
        self.consultas_realizadas += 1
        if not self._disponible:
            raise TimeoutError(
                f"El servicio del SIA no respondió en {tiempo_limite_segundos:g} segundos."
            )
        if self._fallas_pendientes > 0:
            self._fallas_pendientes -= 1
            raise TimeoutError(
                f"El servicio del SIA no respondió en {tiempo_limite_segundos:g} segundos."
            )

        clave = (documento_estudiante.strip(), periodo.strip())
        datos = self._registros.get(clave)
        if datos is None:
            raise RuntimeError(
                f"No se encontraron datos académicos en el SIA para el documento '{documento_estudiante}' "
                f"en el periodo '{periodo}'."
            )
        return datos
