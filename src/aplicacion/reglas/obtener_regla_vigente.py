from aplicacion.puertos.repositorio_reglas_practica import RepositorioReglasPractica
from dominio.regla_practica import ReglaPractica


class ObtenerReglaVigente:
    def __init__(self, repositorio_reglas: RepositorioReglasPractica) -> None:
        self._repositorio_reglas = repositorio_reglas

    def ejecutar(self, nombre_programa: str, periodo: str) -> ReglaPractica:
        regla = self._repositorio_reglas.obtener_vigente(
            nombre_programa=nombre_programa,
            periodo=periodo,
        )
        if regla is None:
            raise ValueError(
                f"El programa '{nombre_programa}' no tiene reglas de práctica configuradas para el periodo '{periodo}'."
            )
        return regla
