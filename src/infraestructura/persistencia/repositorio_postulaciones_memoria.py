from dominio.postulacion import Postulacion


class RepositorioPostulacionesMemoria:
    def __init__(self) -> None:
        self._postulaciones: dict[str, Postulacion] = {}

    def guardar(self, postulacion: Postulacion) -> None:
        self._postulaciones[postulacion.id_postulacion] = postulacion

    def buscar_por_id(self, id_postulacion: str) -> Postulacion | None:
        return self._postulaciones.get(id_postulacion)

    def listar_por_estudiante_y_periodo(
        self,
        documento_estudiante: str,
        periodo: str,
    ) -> list[Postulacion]:
        return [
            postulacion
            for postulacion in self._postulaciones.values()
            if postulacion.estudiante.documento == documento_estudiante
            and postulacion.periodo == periodo
        ]
