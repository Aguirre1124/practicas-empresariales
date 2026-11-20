from typing import Protocol

from dominio.postulacion import Postulacion


class RepositorioPostulaciones(Protocol):
    def guardar(self, postulacion: Postulacion) -> None: ...

    def buscar_por_id(self, id_postulacion: str) -> Postulacion | None: ...

    def listar_por_estudiante_y_periodo(
        self,
        documento_estudiante: str,
        periodo: str,
    ) -> list[Postulacion]: ...
