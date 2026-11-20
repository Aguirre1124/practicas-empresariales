from dataclasses import dataclass

from dominio.empresa import Empresa


@dataclass(frozen=True)
class SupervisorEmpresa:
    nombre: str
    correo: str
    empresa: Empresa

    def __post_init__(self) -> None:
        nombre = self.nombre.strip() if self.nombre else ""
        correo = self.correo.strip() if self.correo else ""
        if not nombre:
            raise ValueError("El nombre del supervisor de empresa es obligatorio.")
        if not correo:
            raise ValueError("El correo del supervisor de empresa es obligatorio.")
        partes = correo.split("@")
        if len(partes) != 2 or not partes[0] or "." not in partes[1]:
            raise ValueError(f"El correo del supervisor '{correo}' no tiene un formato válido.")
        object.__setattr__(self, "nombre", nombre)
        object.__setattr__(self, "correo", correo)
