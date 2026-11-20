from datetime import datetime, timezone
from uuid import uuid4

from aplicacion.auditoria.registrar_evento_bitacora import RegistrarEventoBitacora
from aplicacion.postulaciones.respuesta_postulacion_dto import RespuestaPostulacionDTO
from aplicacion.postulaciones.solicitud_postulacion_dto import SolicitudPostulacionDTO
from aplicacion.puertos.publicador_mensajes import PublicadorMensajes
from aplicacion.puertos.repositorio_postulaciones import RepositorioPostulaciones
from aplicacion.reglas.obtener_regla_vigente import ObtenerReglaVigente
from dominio.empresa import Empresa
from dominio.estado_postulacion import EstadoPostulacion
from dominio.estudiante import Estudiante
from dominio.postulacion import Postulacion
from dominio.programa import Programa
from dominio.supervisor_empresa import SupervisorEmpresa


class PostularsePractica:
    def __init__(
        self,
        repositorio_postulaciones: RepositorioPostulaciones,
        obtener_regla_vigente: ObtenerReglaVigente,
        publicador_mensajes: PublicadorMensajes,
        registrar_evento_bitacora: RegistrarEventoBitacora,
    ) -> None:
        self._repositorio_postulaciones = repositorio_postulaciones
        self._obtener_regla_vigente = obtener_regla_vigente
        self._publicador_mensajes = publicador_mensajes
        self._registrar_evento_bitacora = registrar_evento_bitacora

    def ejecutar(self, solicitud: SolicitudPostulacionDTO) -> RespuestaPostulacionDTO:
        existentes = self._repositorio_postulaciones.listar_por_estudiante_y_periodo(
            documento_estudiante=solicitud.documento_estudiante.strip(),
            periodo=solicitud.periodo.strip(),
        )
        if any(postulacion.esta_en_tramite() for postulacion in existentes):
            return RespuestaPostulacionDTO(
                aceptada=False,
                id_postulacion=None,
                estado=None,
                mensaje="Ya tienes una postulación en trámite para este periodo",
            )

        try:
            programa = Programa(nombre=solicitud.nombre_programa)
            estudiante = Estudiante(
                documento=solicitud.documento_estudiante,
                nombre=solicitud.nombre_estudiante,
                correo_institucional=solicitud.correo_estudiante,
                programa=programa,
            )
            empresa = Empresa(nombre=solicitud.nombre_empresa, nit=solicitud.nit_empresa)
            supervisor = SupervisorEmpresa(
                nombre=solicitud.nombre_supervisor,
                correo=solicitud.correo_supervisor,
                empresa=empresa,
            )
            regla = self._obtener_regla_vigente.ejecutar(
                nombre_programa=programa.nombre,
                periodo=solicitud.periodo.strip(),
            )
        except ValueError as error:
            return RespuestaPostulacionDTO(
                aceptada=False,
                id_postulacion=None,
                estado=None,
                mensaje=str(error),
            )

        postulacion = Postulacion(
            id_postulacion=f"POST-{uuid4().hex[:8].upper()}",
            estudiante=estudiante,
            regla_practica=regla,
            empresa=empresa,
            supervisor_empresa=supervisor,
            periodo=solicitud.periodo.strip(),
            fecha=datetime.now(timezone.utc),
            estado=EstadoPostulacion.PENDIENTE_VERIFICACION,
        )
        self._repositorio_postulaciones.guardar(postulacion)
        self._registrar_evento_bitacora.ejecutar(
            usuario=estudiante.correo_institucional,
            accion="POSTULACION_RECIBIDA",
            direccion_origen=solicitud.direccion_origen,
            detalle=(
                f"Postulación {postulacion.id_postulacion} registrada en estado "
                f"'{postulacion.estado}' para el periodo {postulacion.periodo}."
            ),
            id_referencia=postulacion.id_postulacion,
        )
        self._publicador_mensajes.publicar_verificacion(postulacion.id_postulacion)

        return RespuestaPostulacionDTO(
            aceptada=True,
            id_postulacion=postulacion.id_postulacion,
            estado=str(postulacion.estado),
            mensaje="Recibida, estamos verificando tus requisitos",
        )
