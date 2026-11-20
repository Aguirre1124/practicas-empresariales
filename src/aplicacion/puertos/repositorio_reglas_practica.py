from typing import Protocol

from dominio.regla_practica import ReglaPractica


class RepositorioReglasPractica(Protocol):
    def guardar(self, regla: ReglaPractica) -> None: ...

    def obtener_vigente(
        self,
        nombre_programa: str,
        periodo: str,
    ) -> ReglaPractica | None: ...
