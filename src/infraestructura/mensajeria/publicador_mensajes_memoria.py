from collections import deque


class PublicadorMensajesMemoria:
    def __init__(self) -> None:
        self._cola: deque[tuple[str, int]] = deque()
        self.historial_reintentos: list[tuple[str, int]] = []

    def publicar_verificacion(self, id_postulacion: str) -> None:
        self._cola.append((id_postulacion, 0))

    def reencolar_verificacion(
        self,
        id_postulacion: str,
        espera_segundos: int,
    ) -> None:
        self._cola.append((id_postulacion, espera_segundos))
        self.historial_reintentos.append((id_postulacion, espera_segundos))

    def tomar_siguiente(self) -> tuple[str, int] | None:
        if not self._cola:
            return None
        return self._cola.popleft()

    def cantidad_pendientes(self) -> int:
        return len(self._cola)

    def supera_umbral_alerta(self, umbral: int = 100) -> bool:
        return len(self._cola) > umbral
