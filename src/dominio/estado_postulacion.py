from enum import StrEnum


class EstadoPostulacion(StrEnum):
    PENDIENTE_VERIFICACION = "pendiente de verificación"
    CUMPLE_REQUISITOS = "cumple requisitos"
    NO_CUMPLE_REQUISITOS = "no cumple requisitos"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"

    def esta_en_tramite(self) -> bool:
        return self in (
            EstadoPostulacion.PENDIENTE_VERIFICACION,
            EstadoPostulacion.CUMPLE_REQUISITOS,
            EstadoPostulacion.APROBADA,
        )
