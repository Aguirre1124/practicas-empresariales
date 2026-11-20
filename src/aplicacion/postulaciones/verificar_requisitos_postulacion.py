from datetime import datetime, timezone

from aplicacion.auditoria.registrar_evento_bitacora import RegistrarEventoBitacora
from aplicacion.postulaciones.respuesta_postulacion_dto import RespuestaPostulacionDTO
from aplicacion.puertos.consulta_academica import ConsultaAcademica
from aplicacion.puertos.notificador import Notificador
from aplicacion.puertos.publicador_mensajes import PublicadorMensajes
from aplicacion.puertos.repositorio_postulaciones import RepositorioPostulaciones


class VerificarRequisitosPostulacion:
    def __init__(
        self,
        repositorio_postulaciones: RepositorioPostulaciones,
        consulta_academica: ConsultaAcademica,
        publicador_mensajes: PublicadorMensajes,
        notificador: Notificador,
        registrar_evento_bitacora: RegistrarEventoBitacora,
        tiempo_limite_sia_segundos: float = 5.0,
        espera_base_reintento_segundos: int = 30,
    ) -> None:
        self._repositorio_postulaciones = repositorio_postulaciones
        self._consulta_academica = consulta_academica
        self._publicador_mensajes = publicador_mensajes
        self._notificador = notificador
        self._registrar_evento_bitacora = registrar_evento_bitacora
        self._tiempo_limite_sia_segundos = tiempo_limite_sia_segundos
        self._espera_base_reintento_segundos = espera_base_reintento_segundos

    def ejecutar(
        self,
        id_postulacion: str,
        direccion_origen: str = "worker-integracion",
    ) -> RespuestaPostulacionDTO:
        postulacion = self._repositorio_postulaciones.buscar_por_id(id_postulacion)
        if postulacion is None:
            raise ValueError(f"No existe una postulación con el identificador '{id_postulacion}'.")

        ahora = datetime.now(timezone.utc)
        try:
            datos_academicos = self._consulta_academica.consultar_datos_academicos(
                documento_estudiante=postulacion.estudiante.documento,
                periodo=postulacion.periodo,
                tiempo_limite_segundos=self._tiempo_limite_sia_segundos,
            )
        except (TimeoutError, ConnectionError, RuntimeError) as error:
            verificacion = postulacion.registrar_intento_fallido(
                fecha=ahora,
                motivo=str(error) or "El servicio del SIA no respondió dentro del tiempo límite.",
            )
            self._repositorio_postulaciones.guardar(postulacion)
            espera = self._espera_base_reintento_segundos * (2 ** (verificacion.numero_intento - 1))
            self._publicador_mensajes.reencolar_verificacion(
                id_postulacion=postulacion.id_postulacion,
                espera_segundos=espera,
            )
            return RespuestaPostulacionDTO(
                aceptada=False,
                id_postulacion=postulacion.id_postulacion,
                estado=str(postulacion.estado),
                mensaje=f"SIA no disponible; verificación reencolada para reintento en {espera} s.",
                detalle_verificacion=verificacion.detalle_resultado,
            )

        verificacion = postulacion.aplicar_resultado_verificacion(
            fecha=ahora,
            porcentaje_creditos_aprobados=datos_academicos.porcentaje_creditos_aprobados,
            matricula_activa=datos_academicos.matricula_activa,
        )
        self._repositorio_postulaciones.guardar(postulacion)
        self._registrar_evento_bitacora.ejecutar(
            usuario=postulacion.estudiante.correo_institucional,
            accion="CAMBIO_ESTADO_POSTULACION",
            direccion_origen=direccion_origen,
            detalle=(
                f"Postulación {postulacion.id_postulacion} cambió a '{postulacion.estado}' "
                f"en el intento {verificacion.numero_intento}: {verificacion.detalle_resultado}"
            ),
            id_referencia=postulacion.id_postulacion,
        )
        self._notificador.enviar_correo(
            destinatario=postulacion.estudiante.correo_institucional,
            asunto=f"Resultado de verificación de postulación ({postulacion.periodo})",
            mensaje=(
                f"Tu postulación {postulacion.id_postulacion} quedó en estado "
                f"'{postulacion.estado}'. {verificacion.detalle_resultado}"
            ),
        )
        return RespuestaPostulacionDTO(
            aceptada=True,
            id_postulacion=postulacion.id_postulacion,
            estado=str(postulacion.estado),
            mensaje=f"Verificación completada: {postulacion.estado}",
            detalle_verificacion=verificacion.detalle_resultado,
        )
