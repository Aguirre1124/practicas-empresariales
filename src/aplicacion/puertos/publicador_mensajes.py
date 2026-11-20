from typing import Protocol


class PublicadorMensajes(Protocol):
    def publicar_verificacion(self, id_postulacion: str) -> None: ...

    def reencolar_verificacion(
        self,
        id_postulacion: str,
        espera_segundos: int,
    ) -> None: ...
