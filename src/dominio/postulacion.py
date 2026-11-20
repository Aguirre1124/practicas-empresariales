from dataclasses import dataclass, field
from datetime import datetime

from dominio.empresa import Empresa
from dominio.estado_postulacion import EstadoPostulacion
from dominio.estudiante import Estudiante
from dominio.regla_practica import ReglaPractica
from dominio.supervisor_empresa import SupervisorEmpresa
from dominio.verificacion_requisitos import VerificacionRequisitos


@dataclass
class Postulacion:
    id_postulacion: str
    estudiante: Estudiante
    regla_practica: ReglaPractica
    empresa: Empresa
    supervisor_empresa: SupervisorEmpresa
    periodo: str
    fecha: datetime
    estado: EstadoPostulacion = EstadoPostulacion.PENDIENTE_VERIFICACION
    verificaciones: list[VerificacionRequisitos] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id_postulacion or not self.id_postulacion.strip():
            raise ValueError("El identificador de la postulación es obligatorio.")
        if not self.periodo or not self.periodo.strip():
            raise ValueError("El periodo académico de la postulación es obligatorio.")
        self.id_postulacion = self.id_postulacion.strip()
        self.periodo = self.periodo.strip()

    def esta_en_tramite(self) -> bool:
        return self.estado.esta_en_tramite()

    def siguiente_numero_intento(self) -> int:
        return len(self.verificaciones) + 1

    def registrar_intento_fallido(self, fecha: datetime, motivo: str) -> VerificacionRequisitos:
        verificacion = VerificacionRequisitos(
            numero_intento=self.siguiente_numero_intento(),
            fecha=fecha,
            exitosa=False,
            detalle_resultado=motivo,
        )
        self.verificaciones.append(verificacion)
        return verificacion

    def aplicar_resultado_verificacion(
        self,
        fecha: datetime,
        porcentaje_creditos_aprobados: float,
        matricula_activa: bool,
    ) -> VerificacionRequisitos:
        if self.estado != EstadoPostulacion.PENDIENTE_VERIFICACION:
            raise ValueError(
                f"Solo se puede verificar una postulación pendiente; estado actual: '{self.estado}'."
            )
        incumplimientos = self.regla_practica.evaluar_requisitos(
            porcentaje_creditos_aprobados=porcentaje_creditos_aprobados,
            matricula_activa=matricula_activa,
        )
        if not incumplimientos:
            self.estado = EstadoPostulacion.CUMPLE_REQUISITOS
            verificacion = VerificacionRequisitos(
                numero_intento=self.siguiente_numero_intento(),
                fecha=fecha,
                exitosa=True,
                detalle_resultado="Cumple todos los requisitos académicos vigentes.",
            )
        else:
            self.estado = EstadoPostulacion.NO_CUMPLE_REQUISITOS
            verificacion = VerificacionRequisitos(
                numero_intento=self.siguiente_numero_intento(),
                fecha=fecha,
                exitosa=False,
                detalle_resultado=" ".join(incumplimientos),
            )
        self.verificaciones.append(verificacion)
        return verificacion
