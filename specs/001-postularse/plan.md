# Plan: 001 Postularse a la práctica empresarial

## Decisiones que aplican

- **[ADR-001](../../docs/adr/ADR-001-estructura-general.md) (Monolito modular con Clean Architecture):** el código se organiza en las capas `dominio/`, `aplicacion/` e `infraestructura/`, respetando la vista de usos sin ciclos de [03-desarrollo.md](../../docs/vistas/03-desarrollo.md) (`Módulo Postulaciones` → `Módulo Reglas` → `Módulo Auditoría` → `Dominio`). Ningún archivo de `dominio/` importa de `aplicacion/` ni de `infraestructura/`, y `aplicacion/` solo importa de `dominio/` y sus propios puertos.
- **[ADR-002](../../docs/adr/ADR-002-integracion-sia.md) (Consultar el SIA solo por el adaptador detrás del puerto `ConsultaAcademica`):** el caso de uso de verificación no conoce detalles del SIA; consulta los créditos aprobados y el estado de matrícula del estudiante únicamente a través del puerto `ConsultaAcademica`.
- **[ADR-003](../../docs/adr/ADR-003-broker-mensajes.md) (Bróker de mensajes con reintentos para el SIA y el correo):** la postulación se divide en dos momentos desacoplados para cumplir `EAC-02`:
  1. Al recibir la solicitud, se valida que no haya una postulación en trámite en el mismo periodo ni datos obligatorios inválidos, se guarda la `Postulacion` en estado `pendiente de verificación`, se publica el mensaje de verificación en el puerto `PublicadorMensajes` y se devuelve confirmación inmediata al estudiante (`< 3 s`, sin llamar al SIA).
  2. El consumidor toma el mensaje y ejecuta la verificación contra el puerto `ConsultaAcademica`; si el SIA no responde en 5 s o falla, registra el intento fallido en `VerificacionRequisitos` y reencola el mensaje para reintentar con espera creciente (`0 postulaciones perdidas`).
- **[ADR-004](../../docs/adr/ADR-004-autenticacion-institucional.md) (Inicio de sesión institucional y roles en el sistema):** la solicitud llega asociada a un `Estudiante` autenticado con su cuenta institucional, quien solo puede postularse en su propio nombre (`RN-01`).
- **[ADR-006](../../docs/adr/ADR-006-bitacora-auditoria.md) (Bitácora de auditoría de solo inserción):** cada cambio de estado de la `Postulacion` (`pendiente de verificación`, `cumple requisitos` o `no cumple requisitos`) registra un `EventoBitacora` mediante el componente común de auditoría, sin métodos de modificación ni borrado.
- **[ADR-007](../../docs/adr/ADR-007-reglas-configurables.md) (Reglas de práctica como datos, por periodo):** el porcentaje mínimo de créditos aprobados (por defecto 80%) y la exigencia de matrícula activa no se escriben como constantes fijas del caso de uso, sino que se leen de la `ReglaPractica` vigente del `Programa` para el periodo académico indicado.
- **[ADR-009](../../docs/adr/ADR-009-persistencia.md) (Persistencia detrás de puertos de repositorio):** las postulaciones, reglas de práctica y eventos de bitácora se guardan detrás de puertos de repositorio; en esta etapa se implementan con adaptadores en memoria según `AGENTS.md`.

## Componentes

Según [docs/vistas/03-desarrollo.md](../../docs/vistas/03-desarrollo.md), con una clase por archivo, sin `__init__.py` y usando los nombres del glosario de [docs/arquitectura.md](../../docs/arquitectura.md#10-glosario):

### Capa de dominio (`src/dominio/`)
- `src/dominio/estado_postulacion.py`: clase `EstadoPostulacion` con los estados válidos de la postulación (`PENDIENTE_VERIFICACION`, `CUMPLE_REQUISITOS`, `NO_CUMPLE_REQUISITOS`, `APROBADA`, `RECHAZADA`) y qué estados se consideran en trámite.
- `src/dominio/programa.py`: entidad `Programa` (`nombre`).
- `src/dominio/regla_practica.py`: entidad `ReglaPractica` (`programa`, `periodo_vigencia`, `porcentaje_creditos_minimo`, `matricula_activa_requerida`, `horas_minimas`, `plazo_evaluacion_dias`) y método de dominio para evaluar si los datos académicos cumplen los requisitos y cuáles fallaron.
- `src/dominio/estudiante.py`: entidad `Estudiante` (`documento`, `nombre`, `correo_institucional`, `programa`).
- `src/dominio/empresa.py`: entidad `Empresa` (`nombre`, `nit`) con validación del formato del NIT y datos obligatorios.
- `src/dominio/supervisor_empresa.py`: entidad `SupervisorEmpresa` (`nombre`, `correo`, `empresa`) con validación de nombre y correo obligatorios.
- `src/dominio/verificacion_requisitos.py`: entidad `VerificacionRequisitos` (`numero_intento`, `fecha`, `exitosa`, `detalle_resultado`).
- `src/dominio/postulacion.py`: entidad `Postulacion` (`id_postulacion`, `estudiante`, `regla_practica`, `empresa`, `supervisor_empresa`, `periodo`, `fecha`, `estado`, `verificaciones`) con sus reglas de transición de estado y registro de intentos de verificación.
- `src/dominio/evento_bitacora.py`: entidad inmutable `EventoBitacora` (`fecha_hora`, `usuario`, `accion`, `direccion_origen`, `detalle`).

### Capa de aplicación — Puertos (`src/aplicacion/puertos/`)
- `src/aplicacion/puertos/repositorio_postulaciones.py`: puerto `RepositorioPostulaciones` (`Protocol`) para guardar, buscar por identificador y consultar postulaciones de un estudiante en un periodo.
- `src/aplicacion/puertos/repositorio_reglas_practica.py`: puerto `RepositorioReglasPractica` (`Protocol`) para obtener la `ReglaPractica` vigente de un programa en un periodo.
- `src/aplicacion/puertos/repositorio_bitacora.py`: puerto `RepositorioBitacora` (`Protocol`) de solo inserción para registrar `EventoBitacora`.
- `src/aplicacion/puertos/consulta_academica.py`: puerto `ConsultaAcademica` (`Protocol`) que consulta en el SIA los datos académicos del estudiante (`porcentaje_creditos_aprobados`, `matricula_activa`).
- `src/aplicacion/puertos/publicador_mensajes.py`: puerto `PublicadorMensajes` (`Protocol`) para publicar y reencolar solicitudes de verificación de requisitos.
- `src/aplicacion/puertos/notificador.py`: puerto `Notificador` (`Protocol`) para enviar al correo institucional del estudiante el resultado de la verificación.

### Capa de aplicación — DTO y módulos de casos de uso (`src/aplicacion/`)
- `src/aplicacion/auditoria/registrar_evento_bitacora.py`: componente `RegistrarEventoBitacora` (*Módulo Auditoría*) que inserta un `EventoBitacora` en `RepositorioBitacora`.
- `src/aplicacion/reglas/obtener_regla_vigente.py`: componente `ObtenerReglaVigente` (*Módulo Reglas*) que obtiene la `ReglaPractica` del programa y periodo.
- `src/aplicacion/postulaciones/solicitud_postulacion_dto.py`: DTO de entrada `SolicitudPostulacionDTO` con los datos del estudiante, periodo, nombre y NIT de la empresa, y nombre y correo del supervisor.
- `src/aplicacion/postulaciones/respuesta_postulacion_dto.py`: DTO de salida `RespuestaPostulacionDTO` con el identificador de la postulación, su estado, el mensaje de confirmación o rechazo y el resultado de verificación.
- `src/aplicacion/postulaciones/datos_academicos_dto.py`: DTO `DatosAcademicosDTO` con la respuesta del SIA (`documento_estudiante`, `porcentaje_creditos_aprobados`, `matricula_activa`, `periodo`).
- `src/aplicacion/postulaciones/postularse_practica.py`: caso de uso `PostularsePractica` (*Módulo Postulaciones*, parte síncrona en la API) que valida que no exista postulación en trámite en el periodo, valida los datos de `Empresa` y `SupervisorEmpresa`, verifica que exista `ReglaPractica` vigente con `ObtenerReglaVigente`, guarda la `Postulacion` en `PENDIENTE_VERIFICACION`, registra el evento en auditoría, publica el mensaje en `PublicadorMensajes` y retorna `RespuestaPostulacionDTO` con la confirmación inmediata.
- `src/aplicacion/postulaciones/verificar_requisitos_postulacion.py`: caso de uso `VerificarRequisitosPostulacion` (*Módulo Postulaciones*, ejecutado por el worker) que consulta `ConsultaAcademica`, registra la `VerificacionRequisitos`, actualiza la `Postulacion` a `CUMPLE_REQUISITOS` o `NO_CUMPLE_REQUISITOS` (o reencola con espera creciente si el SIA falla), registra el `EventoBitacora` y notifica por `Notificador`.

### Capa de infraestructura (`src/infraestructura/`)
- `src/infraestructura/persistencia/repositorio_postulaciones_memoria.py`: clase `RepositorioPostulacionesMemoria` (*Adaptador PostgreSQL* en memoria).
- `src/infraestructura/persistencia/repositorio_reglas_practica_memoria.py`: clase `RepositorioReglasPracticaMemoria` (*Adaptador PostgreSQL* en memoria).
- `src/infraestructura/persistencia/repositorio_bitacora_memoria.py`: clase `RepositorioBitacoraMemoria` de solo inserción (*Adaptador PostgreSQL* en memoria).
- `src/infraestructura/mensajeria/publicador_mensajes_memoria.py`: clase `PublicadorMensajesMemoria` (*Publicador de mensajes* sobre cola persistente simulada en memoria con registro de reintentos y espera creciente).
- `src/infraestructura/mensajeria/consumidor_mensajes_verificacion.py`: clase `ConsumidorMensajesVerificacion` (*Consumidor de mensajes* del worker) que toma mensajes de la cola y ejecuta `VerificarRequisitosPostulacion`.
- `src/infraestructura/sia/adaptador_sia_memoria.py`: clase `AdaptadorSIAMemoria` (*Adaptador SIA*) que implementa `ConsultaAcademica` y permite simular respuestas normales y fallas/tiempos límite de 5 s del SIA (`EAC-02`).
- `src/infraestructura/notificaciones/adaptador_correo_memoria.py`: clase `AdaptadorCorreoMemoria` (*Adaptador de correo*) que implementa `Notificador`.

### Raíz de composición (`src/infraestructura/composicion/`)
- `src/infraestructura/composicion/contenedor_postulaciones.py`: clase `ContenedorPostulaciones` que instancia los adaptadores en memoria y los inyecta en `RegistrarEventoBitacora`, `ObtenerReglaVigente`, `PostularsePractica`, `VerificarRequisitosPostulacion` y `ConsumidorMensajesVerificacion` sin que el dominio ni la aplicación conozcan la infraestructura.

### Cobertura de los escenarios de `spec.md` por componentes

| Escenario de `spec.md` | Componentes que lo atienden |
|---|---|
| 1. Postulación recibida y verificada cuando el estudiante cumple requisitos académicos | `PostularsePractica`, `ObtenerReglaVigente`, `PublicadorMensajesMemoria`, `ConsumidorMensajesVerificacion`, `VerificarRequisitosPostulacion`, `AdaptadorSIAMemoria`, `RegistrarEventoBitacora`, `AdaptadorCorreoMemoria` |
| 2. Postulación verificada cuando el estudiante no cumple alguno de los requisitos académicos | `ReglaPractica`, `VerificarRequisitosPostulacion`, `VerificacionRequisitos`, `RegistrarEventoBitacora`, `AdaptadorCorreoMemoria` |
| 3. Postulación rechazada por tener otra postulación en trámite en el mismo periodo | `EstadoPostulacion`, `PostularsePractica`, `RepositorioPostulacionesMemoria` |
| 4. Nueva postulación permitida cuando la anterior quedó en no cumple requisitos o rechazada | `EstadoPostulacion`, `PostularsePractica`, `RepositorioPostulacionesMemoria` |
| 5. Postulación rechazada cuando faltan datos obligatorios de la empresa o el NIT no tiene formato válido | `Empresa`, `SupervisorEmpresa`, `PostularsePractica` |
| 6. Tolerancia a fallos cuando el SIA no responde durante la postulación (`EAC-02`) | `PostularsePractica`, `PublicadorMensajesMemoria`, `ConsumidorMensajesVerificacion`, `VerificarRequisitosPostulacion`, `AdaptadorSIAMemoria`, `VerificacionRequisitos` |

## Flujo

Sigue el diagrama de secuencia arquitectónico `ESC-01`: [docs/diagramas/secuencias/cu01-postularse.puml](../../docs/diagramas/secuencias/cu01-postularse.puml).

1. **Petición y confirmación rápida (API):** `PostularsePractica` verifica en `RepositorioPostulaciones` que el `Estudiante` no tenga otra `Postulacion` en trámite en el mismo periodo, valida los datos de `Empresa` (incluido formato de NIT) y `SupervisorEmpresa`, obtiene la `ReglaPractica` vigente mediante `ObtenerReglaVigente`, guarda la `Postulacion` en estado `PENDIENTE_VERIFICACION`, registra el evento en `RegistrarEventoBitacora`, publica el identificador de la postulación en `PublicadorMensajes` y responde de inmediato `"Recibida, estamos verificando tus requisitos"`.
2. **Verificación asíncrona y reintentos (Worker):** `ConsumidorMensajesVerificacion` toma el mensaje de la cola e invoca `VerificarRequisitosPostulacion`. Este consulta `ConsultaAcademica`:
   - Si el SIA responde, evalúa la `ReglaPractica` (mínimo de créditos aprobados y matrícula activa), agrega la `VerificacionRequisitos`, cambia el estado de la `Postulacion` a `CUMPLE_REQUISITOS` o `NO_CUMPLE_REQUISITOS`, registra el `EventoBitacora` y envía el correo por `Notificador`.
   - Si el SIA no responde en 5 s o lanza error (`EAC-02`), registra la `VerificacionRequisitos` fallida con el número de intento y reencola el mensaje en `PublicadorMensajes` con espera creciente sin perder la postulación.

## Datos

Entidades del modelo de dominio ([docs/vistas/01-logica.md](../../docs/vistas/01-logica.md)) que intervienen:

- `Programa`
- `ReglaPractica`
- `Estudiante`
- `Empresa`
- `SupervisorEmpresa`
- `Postulacion` (y `EstadoPostulacion`)
- `VerificacionRequisitos`
- `EventoBitacora`

## Fuera de alcance

- Aprobación o rechazo final de la postulación y verificación de la vigencia del convenio con la empresa por parte del director de programa (`CU-02`).
- Asignación del docente asesor de práctica (`CU-03`).
- Configuración o creación de nuevas versiones de reglas de práctica por el director de programa (`CU-12`); aquí solo se consulta la regla vigente.
- Conexión de red real a PostgreSQL, RabbitMQ, SIA o servidor SMTP (en esta etapa se usan los adaptadores en memoria según `AGENTS.md`).

## Decisiones pendientes

Ninguna. Todas las decisiones arquitectónicas requeridas por `CU-01` y `EAC-02` están cubiertas por `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-006`, `ADR-007` y `ADR-009`.
