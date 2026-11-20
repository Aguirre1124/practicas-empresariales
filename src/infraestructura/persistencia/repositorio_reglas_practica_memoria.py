from dominio.regla_practica import ReglaPractica


class RepositorioReglasPracticaMemoria:
    def __init__(self) -> None:
        self._reglas: dict[tuple[str, str], ReglaPractica] = {}

    def guardar(self, regla: ReglaPractica) -> None:
        clave = (regla.programa.nombre.lower(), regla.periodo_vigencia)
        self._reglas[clave] = regla

    def obtener_vigente(
        self,
        nombre_programa: str,
        periodo: str,
    ) -> ReglaPractica | None:
        clave = (nombre_programa.strip().lower(), periodo.strip())
        return self._reglas.get(clave)
