from dataclasses import dataclass

from dominio.programa import Programa


@dataclass(frozen=True)
class Estudiante:
    documento: str
    nombre: str
    correo_institucional: str
    programa: Programa

    def __post_init__(self) -> None:
        documento = self.documento.strip() if self.documento else ""
        nombre = self.nombre.strip() if self.nombre else ""
        correo = self.correo_institucional.strip() if self.correo_institucional else ""
        if not documento:
            raise ValueError("El documento del estudiante es obligatorio.")
        if not nombre:
            raise ValueError("El nombre del estudiante es obligatorio.")
        if not correo or "@" not in correo:
            raise ValueError("El correo institucional del estudiante no es válido.")
        object.__setattr__(self, "documento", documento)
        object.__setattr__(self, "nombre", nombre)
        object.__setattr__(self, "correo_institucional", correo)
