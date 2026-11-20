from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EventoBitacora:
    fecha_hora: datetime
    usuario: str
    accion: str
    direccion_origen: str
    detalle: str
    id_referencia: str = ""

    def __post_init__(self) -> None:
        usuario = self.usuario.strip() if self.usuario else ""
        accion = self.accion.strip() if self.accion else ""
        origen = self.direccion_origen.strip() if self.direccion_origen else ""
        detalle = self.detalle.strip() if self.detalle else ""
        if not usuario:
            raise ValueError("El usuario o actor del evento de bitácora es obligatorio.")
        if not accion:
            raise ValueError("La acción del evento de bitácora es obligatoria.")
        if not origen:
            raise ValueError("La dirección de origen del evento de bitácora es obligatoria.")
        if not detalle:
            raise ValueError("El detalle del evento de bitácora es obligatorio.")
        object.__setattr__(self, "usuario", usuario)
        object.__setattr__(self, "accion", accion)
        object.__setattr__(self, "direccion_origen", origen)
        object.__setattr__(self, "detalle", detalle)
        object.__setattr__(self, "id_referencia", (self.id_referencia or "").strip())
