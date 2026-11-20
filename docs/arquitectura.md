# Documento de arquitectura: Sistema de Gestión de Prácticas Empresariales

> Versión 0.3 | Estado: en construcción

Este documento consolida la arquitectura del sistema y enlaza a los demás archivos de `docs/` en lugar de copiar su contenido. Es el mapa de entrada para el equipo y para el agente en cada sesión de SDD.

## 1. Introducción y objetivos

El sistema reemplaza la gestión manual en hojas de Excel y correo electrónico de las 500 prácticas empresariales anuales de la Facultad de Ingenierías (acompañadas por 50 docentes asesores), cubriendo desde la postulación del estudiante hasta la generación y aprobación electrónica del acta final.

El problema, los seis objetivos de negocio medibles (`OB-01` a `OB-06`), el alcance y los diez stakeholders (seis de negocio y cuatro técnicos) están en [vision.md](vision.md).

## 2. Restricciones

Las restricciones técnicas (`RT-01` a `RT-04`) y de negocio (`RN-01` a `RN-05`), con su tipo, origen e impacto arquitectónico, están en [drivers.md, sección 3](drivers.md#3-restricciones).

## 3. Contexto del sistema

El sistema como caja negra, sus cinco actores (estudiante, docente asesor, director de programa y administrador con cuenta institucional; supervisor de empresa mediante enlace sin cuenta) y los tres sistemas externos con los que interactúa (SIA, proveedor de identidad institucional y servicio de correo) están en [contexto.md](contexto.md) y su diagrama en [diagramas/contexto.puml](diagramas/contexto.puml).

## 4. Estrategia de solución

Resumen de las decisiones de alto nivel que estructuran el sistema frente a sus drivers principales:

| Driver | Enfoque | ADR |
|---|---|---|
| **PA-01** Estructura general (`S-03`, `R-04`) | Un solo desplegable construido como monolito modular con Clean Architecture; la carga (170 a 250 prácticas activas) no justifica distribuir y las dependencias apuntan siempre hacia el dominio. | [ADR-001](adr/ADR-001-estructura-general.md) |
| **EAC-01** Mantenibilidad (`OB-05`, `S-07`, `CU-12`) | Las reglas de práctica se guardan como datos por programa y periodo de vigencia, no como código. Cada práctica conserva la versión con la que inició, y un tipo nuevo de requisito solo toca el módulo de reglas y el adaptador del SIA (máximo 2 módulos). | [ADR-007](adr/ADR-007-reglas-configurables.md), [ADR-001](adr/ADR-001-estructura-general.md), [ADR-002](adr/ADR-002-integracion-sia.md) |
| **EAC-02** Fiabilidad ante fallas del SIA (`OB-01`, `RT-03`, `CU-01`) | La API registra la postulación como pendiente, publica un mensaje en una cola persistente de RabbitMQ y responde al estudiante en menos de 3 s sin esperar al SIA. Un worker independiente consulta los servicios del SIA a través de un puerto y reintenta con espera creciente si falla. | [ADR-003](adr/ADR-003-broker-mensajes.md), [ADR-002](adr/ADR-002-integracion-sia.md) |
| **EAC-03** Seguridad en acceso externo (`RN-04`, `RN-01`, `CU-07`) | El supervisor de empresa ingresa con un enlace de un solo uso guardado en base de datos con vigencia de 15 días. Cualquier intento con un enlace usado, vencido o alterado se rechaza sin exponer datos personales y queda registrado en menos de 1 minuto en la bitácora. | [ADR-005](adr/ADR-005-enlace-supervisor.md), [ADR-006](adr/ADR-006-bitacora-auditoria.md) |
| **RN-02, RN-03** Validez y conservación del acta (`OB-04`, `CU-09`, `CU-10`) | El acta se genera en PDF llenando una plantilla HTML versionada fuera del código (sin retranscribir datos), se aprueba con identidad institucional trazable en la bitácora y se guarda en el almacenamiento institucional con política de no borrado. | [ADR-008](adr/ADR-008-plantilla-acta.md), [ADR-009](adr/ADR-009-persistencia.md), [ADR-004](adr/ADR-004-autenticacion-institucional.md) |

## 5. Vistas

Las cuatro vistas del modelo 4+1, cada una con su diagrama en [diagramas/](diagramas/):

| Vista | Documento | Diagrama | Notación |
|---|---|---|---|
| Lógica | [vistas/01-logica.md](vistas/01-logica.md) | [01-logica.puml](diagramas/01-logica.puml) | UML, modelo de dominio |
| Procesos | [vistas/02-procesos.md](vistas/02-procesos.md) | [02-procesos.puml](diagramas/02-procesos.puml) | C4, contenedores (nivel 2) |
| Desarrollo | [vistas/03-desarrollo.md](vistas/03-desarrollo.md) | [03-desarrollo.puml](diagramas/03-desarrollo.puml) | C4, componentes (nivel 3) |
| Física | [vistas/04-fisica.md](vistas/04-fisica.md) | [04-fisica.puml](diagramas/04-fisica.puml) | C4, despliegue |

Los escenarios (+1) que recorren las vistas están en [drivers.md, sección 6](drivers.md#6-escenarios) y sus diagramas en [diagramas/secuencias/](diagramas/secuencias/).

### Matriz de cobertura: drivers y ADR por vista

Ninguna fila queda vacía: todo driver y todo ADR se ven en al menos una vista.

| Driver o ADR | Contexto | Lógica | Procesos | Desarrollo | Física |
|---|:-:|:-:|:-:|:-:|:-:|
| CU-01 Postularse | ✓ | ✓ | ✓ | ✓ | |
| CU-07 Evaluar al practicante | ✓ | ✓ | | ✓ | |
| CU-09 Generar el acta | | ✓ | ✓ | ✓ | |
| CU-10 Aprobar el acta | ✓ | ✓ | | ✓ | |
| CU-12 Configurar reglas | ✓ | ✓ | | ✓ | |
| EAC-01 Mantenibilidad (máximo 2 módulos) | | ✓ | | ✓ | |
| EAC-02 Fiabilidad (SIA no responde) | | ✓ | ✓ | | ✓ |
| EAC-03 Seguridad (enlace inválido) | | ✓ | | ✓ | |
| RT-01 Infraestructura institucional | | | | | ✓ |
| RT-02 Inicio de sesión institucional | ✓ | | ✓ | ✓ | ✓ |
| RT-03 Solo servicios del SIA | ✓ | | ✓ | ✓ | |
| RT-04 Catálogo institucional | | | ✓ | | ✓ |
| RN-01 Datos personales (Ley 1581) | | ✓ | ✓ | ✓ | ✓ |
| RN-02 Retención documental | | ✓ | ✓ | | ✓ |
| RN-03 Formato del acta | | ✓ | | ✓ | |
| RN-04 Supervisor sin cuenta | ✓ | ✓ | | ✓ | |
| RN-05 Sin licencias de pago | | | ✓ | | ✓ |
| PA-01 Estructura general | | | ✓ | ✓ | |
| PA-02 Autenticación y autorización | ✓ | | ✓ | ✓ | |
| PA-03 Registro y trazabilidad | | ✓ | | ✓ | |
| PA-04 Fallas de integración | | | ✓ | ✓ | ✓ |
| PA-05 Migración inicial (riesgo, ver sección 7) | | | | ✓ | |
| ADR-001 Monolito modular | | | ✓ | ✓ | |
| ADR-002 Adaptador del SIA | ✓ | | ✓ | ✓ | |
| ADR-003 Bróker de mensajes | | ✓ | ✓ | | ✓ |
| ADR-004 Inicio de sesión y roles | ✓ | | ✓ | ✓ | |
| ADR-005 Enlace del supervisor | | ✓ | | ✓ | |
| ADR-006 Bitácora de auditoría | | ✓ | | ✓ | |
| ADR-007 Reglas como datos | | ✓ | | ✓ | |
| ADR-008 Plantilla del acta | | ✓ | | ✓ | |
| ADR-009 Persistencia | | | ✓ | | ✓ |

## 6. Conceptos transversales

Cómo se resuelven las preocupaciones arquitectónicas ([drivers.md, sección 4](drivers.md#4-preocupaciones-arquitectónicas)) de forma uniforme en todo el sistema:

| Concepto | Cómo se resuelve | Dónde se ve |
|---|---|---|
| **PA-01** Estructura general | Un solo desplegable dividido en módulos por funcionalidad (`postulaciones`, `seguimiento`, `evaluacion`, `actas`, `reglas`, `acceso_externo`, `auditoria`) con las capas `dominio`, `aplicacion` e `infraestructura`. La vista de usos se organiza en cinco niveles sin ciclos ([ADR-001](adr/ADR-001-estructura-general.md)). | [Procesos](vistas/02-procesos.md), [Desarrollo](vistas/03-desarrollo.md) |
| **PA-02** Autenticación y autorización | Conviven dos entradas: inicio de sesión único institucional (OpenID Connect) con roles y permisos filtrados por práctica o programa dentro del sistema ([ADR-004](adr/ADR-004-autenticacion-institucional.md)), y enlace de un solo uso con vigencia de 15 días para el supervisor de empresa ([ADR-005](adr/ADR-005-enlace-supervisor.md)). | [Contexto](contexto.md), [Desarrollo](vistas/03-desarrollo.md), [ESC-02](diagramas/secuencias/cu07-evaluar-practicante.puml), [ESC-04](diagramas/secuencias/cu10-aprobar-acta.puml) |
| **PA-03** Registro y trazabilidad | Un módulo común de auditoría escribe en una tabla de bitácora de solo inserción (quién, qué, cuándo, dirección de origen y práctica) cada aprobación o rechazo de acta, cambio de estado o de reglas, acceso a datos personales e intento de acceso rechazado ([ADR-006](adr/ADR-006-bitacora-auditoria.md)). | [Lógica](vistas/01-logica.md), [Desarrollo](vistas/03-desarrollo.md), [ESC-02](diagramas/secuencias/cu07-evaluar-practicante.puml), [ESC-04](diagramas/secuencias/cu10-aprobar-acta.puml) |
| **PA-04** Manejo de errores y fallas de integración | Ningún caso de uso llama en síncrono al SIA ni al servidor de correo: la API guarda el estado pendiente y publica un mensaje en RabbitMQ; el worker consume de la cola persistente y reintenta con espera creciente si el servicio externo falla ([ADR-002](adr/ADR-002-integracion-sia.md), [ADR-003](adr/ADR-003-broker-mensajes.md)). | [Procesos](vistas/02-procesos.md), [Desarrollo](vistas/03-desarrollo.md), [Física](vistas/04-fisica.md), [ESC-01](diagramas/secuencias/cu01-postularse.puml) |
| **PA-05** Migración inicial de datos | Declarada como riesgo sin ADR aún (ver sección 7): cuando se recolecten y unifiquen las hojas de Excel de los docentes asesores en una plantilla común, se ejecutará un script de carga inicial que invoque los casos de uso del sistema sin escribir directo en la base de datos. | [Desarrollo](vistas/03-desarrollo.md) (componente `Carga inicial`) |

## 7. Decisiones de diseño

### Índice de ADR

| ADR | Decisión | Estado | Drivers que atiende |
|---|---|---|---|
| [ADR-001](adr/ADR-001-estructura-general.md) | Monolito modular con Clean Architecture | Aceptado | PA-01, EAC-01, CU-12, RT-01, RT-04 |
| [ADR-002](adr/ADR-002-integracion-sia.md) | Consultar el SIA solo por un adaptador | Aceptado | RT-03, CU-01 |
| [ADR-003](adr/ADR-003-broker-mensajes.md) | Bróker de mensajes con reintentos para el SIA y el correo | Aceptado | EAC-02, PA-04, CU-01, RT-01, RN-05 |
| [ADR-004](adr/ADR-004-autenticacion-institucional.md) | Inicio de sesión institucional y roles en el sistema | Aceptado | RT-02, PA-02, RN-01, CU-10 |
| [ADR-005](adr/ADR-005-enlace-supervisor.md) | Enlace de un solo uso para el supervisor | Aceptado | RN-04, EAC-03, CU-07, PA-02 |
| [ADR-006](adr/ADR-006-bitacora-auditoria.md) | Bitácora de auditoría de solo inserción | Aceptado | CU-10, PA-03, EAC-03, RN-01 |
| [ADR-007](adr/ADR-007-reglas-configurables.md) | Reglas de práctica como datos, por periodo | Aceptado | CU-12, EAC-01 |
| [ADR-008](adr/ADR-008-plantilla-acta.md) | Acta en PDF desde una plantilla separada del código | Aceptado | CU-09, RN-03, RN-05 |
| [ADR-009](adr/ADR-009-persistencia.md) | PostgreSQL y almacenamiento institucional sin borrado | Aceptado | RT-04, RT-01, RN-02, RN-05, RN-01 |

### Cobertura de los drivers

| Driver | Cubierto por |
|---|---|
| CU-01 | ADR-002, ADR-003 |
| CU-07 | ADR-005 |
| CU-09 | ADR-008 |
| CU-10 | ADR-004, ADR-006 |
| CU-12 | ADR-007, ADR-001 |
| EAC-01 | ADR-007, ADR-001 |
| EAC-02 | ADR-003 |
| EAC-03 | ADR-005, ADR-006 |
| RT-01 | ADR-001, ADR-003, ADR-009 |
| RT-02 | ADR-004 |
| RT-03 | ADR-002 |
| RT-04 | ADR-009, ADR-001 |
| RN-01 | ADR-004, ADR-006, ADR-009 |
| RN-02 | ADR-009 |
| RN-03 | ADR-008 |
| RN-04 | ADR-005 |
| RN-05 | ADR-003, ADR-008, ADR-009 |
| PA-01 | ADR-001 |
| PA-02 | ADR-004, ADR-005 |
| PA-03 | ADR-006 |
| PA-04 | ADR-003 |
| PA-05 | **Sin ADR: se declara como riesgo** |

**Riesgo declarado: PA-05 (migración inicial desde Excel).** Está en el cuadrante "cuestionar" de la matriz de priorización: se ejecuta una sola vez y depende de archivos con formatos distintos por docente asesor que todavía no se conocen. Decidir ahora la herramienta de migración sería decidir sin información. Se mantiene pendiente con esta mitigación: recolectar una muestra de los archivos de cada docente asesor antes de la primera iteración; si los formatos se pueden unificar en una plantilla, la carga se hace con un script de un solo uso que escribe a través de los mismos casos de uso del sistema (sin escribir directo en la base de datos), y esa decisión se registra en un ADR nuevo.

## 8. Requisitos de calidad

El detalle de los escenarios de atributos de calidad con sus seis partes está en [drivers.md, sección 2](drivers.md#2-escenarios-de-atributos-de-calidad) y su priorización en [drivers.md, sección 5](drivers.md#5-matriz-de-priorización). La columna **Se verifica en** conecta cada escenario con la especificación de SDD que comprueba su medida:

| EAC | Atributo (ISO/IEC 25010:2023) | Prioridad | ADR que lo atiende | Se verifica en |
|---|---|---|---|---|
| **EAC-01** | Mantenibilidad (modificabilidad: máximo 16 h, máximo 2 módulos, 0 prácticas en curso afectadas) | Atender primero | [ADR-007](adr/ADR-007-reglas-configurables.md), [ADR-001](adr/ADR-001-estructura-general.md) | `specs/012-configurar-reglas/spec.md` (por especificar) |
| **EAC-02** | Fiabilidad (tolerancia a fallos del SIA: 0 pérdidas, confirmación en menos de 3 s al 95%, verificación en máximo 30 min tras recuperarse) | Atender primero | [ADR-003](adr/ADR-003-broker-mensajes.md), [ADR-002](adr/ADR-002-integracion-sia.md) | `specs/001-postularse/spec.md` |
| **EAC-03** | Seguridad (confidencialidad y responsabilidad: 100% de enlaces inválidos rechazados, 0 datos personales mostrados, registro en bitácora en menos de 1 min) | Hacer ya | [ADR-005](adr/ADR-005-enlace-supervisor.md), [ADR-006](adr/ADR-006-bitacora-auditoria.md) | `specs/007-evaluar-practicante/spec.md` (por especificar) |

## 9. Riesgos y deuda técnica

Consolida los riesgos iniciales de [vision.md, sección 6](vision.md#6-supuestos-y-riesgos-iniciales), los riesgos asumidos en los ADR y la deuda técnica (`DT`) aceptada conscientemente a cambio de simplicidad operativa:

| ID | Riesgo o deuda | Origen | Impacto | Respuesta |
|---|---|---|---|---|
| **R-01** | Los supervisores de empresa no responden la evaluación dentro del plazo reglamentario. | [vision.md](vision.md#6-supuestos-y-riesgos-iniciales) (`OB-02`, `OB-01`) | Sin evaluación del supervisor no se puede generar el acta final (`CU-09`) y se retrasa el cierre de la práctica. | Acceso con un clic por enlace sin cuenta ([ADR-005](adr/ADR-005-enlace-supervisor.md)), formulario corto y recordatorios automáticos con copia al docente asesor (`CU-08`). |
| **R-02** | El SIA no ofrece los servicios de consulta esperados o cae durante varios días en inicio de semestre. | [vision.md](vision.md#6-supuestos-y-riesgos-iniciales) (`S-02`, `S-09`), [ADR-002](adr/ADR-002-integracion-sia.md), [ADR-003](adr/ADR-003-broker-mensajes.md) | La cola de verificaciones pendientes en RabbitMQ crece y los estudiantes tardan en conocer si cumplen requisitos. | Confirmar contrato con el administrador del SIA en la primera semana; alerta al superar 100 mensajes en cola y plan B mediante adaptador que lea una exportación periódica sin tocar los casos de uso. |
| **R-03** | El área jurídica exige firma digital certificada para el acta o objeta el enlace del supervisor como prueba de identidad. | [vision.md](vision.md#6-supuestos-y-riesgos-iniciales) (`S-06`), [ADR-005](adr/ADR-005-enlace-supervisor.md), [ADR-008](adr/ADR-008-plantilla-acta.md) | Habría que integrar un proveedor externo de firma certificada antes de emitir actas oficiales. | Validar `S-06` con el área jurídica antes de construir el módulo de actas; si se exige, registrar un ADR nuevo para el adaptador de firma. |
| **R-04** | Los archivos Excel de las prácticas en curso tienen estructuras incompatibles entre los 50 docentes asesores. | [drivers.md](drivers.md#4-preocupaciones-arquitectónicas) (`PA-05`, sin ADR) | Retraso o errores de datos al migrar las prácticas activas en el lanzamiento (`CU-15`). | Recolectar muestra de archivos, unificarlos en una plantilla común y ejecutar un script de un solo uso que cargue a través de los casos de uso del sistema. |
| **DT-01** | La separación entre módulos y capas en Python depende de la disciplina en los `import`; el intérprete no impide que un módulo importe detalles internos de otro. | [ADR-001](adr/ADR-001-estructura-general.md) (costo aceptado) | Si se rompe la regla de dependencia o se introduce un ciclo entre módulos, se degrada la mantenibilidad (`EAC-01`). | Se acepta en esta etapa para conservar un único desplegable simple; se verifica la regla de dependencia en cada Pull Request y en el archivo `validacion.md` de cada funcionalidad. |
| **DT-02** | El enlace del supervisor prueba acceso a su buzón de correo, no su identidad personal, y si se invalida o vence sin enviar hay que reemitirlo. | [ADR-005](adr/ADR-005-enlace-supervisor.md) (costo aceptado) | Reemisión manual ocasional por parte del docente asesor o del director de programa. | Se acepta para no exigir registro ni contraseña al supervisor (`RN-04`); el enlace solo pasa a estado `usado` en la misma transacción en que se guarda la evaluación ([ESC-02](diagramas/secuencias/cu07-evaluar-practicante.puml)). |
| **DT-03** | Los datos estructurados viven en PostgreSQL y los PDF de las actas en el almacenamiento institucional, sin transacción distribuida entre ambos. | [ADR-009](adr/ADR-009-persistencia.md) (costo aceptado) | Si ocurre una falla entre guardar el PDF y registrar el acta en base de datos, o si se restauran respaldos desfasados, puede quedar un archivo sin registro o viceversa. | Se acepta para cumplir la retención sin borrado (`RN-02`) sin inflar PostgreSQL con binarios; la API escribe primero el PDF en el repositorio de documentos antes de confirmar el registro del acta en la base de datos ([ESC-03](diagramas/secuencias/cu09-generar-acta.puml)). |

## 10. Glosario

Lenguaje ubicuo del dominio: cada concepto tiene un único término en la documentación, en los escenarios Gherkin (`spec.md`) y en el código fuente (`src/`). Reúne las entidades de la [vista lógica](vistas/01-logica.md), los roles de [vision.md](vision.md#4-stakeholders) y [contexto.md](contexto.md), los estados del proceso y los puertos de la [vista de desarrollo](vistas/03-desarrollo.md).

| Término | Definición | Nombre en el código |
|---|---|---|
| **Programa** | Programa académico de la Facultad de Ingenierías que tiene reglas propias de práctica (`S-07`). | `Programa` |
| **Regla de práctica** | Conjunto de requisitos académicos, horas mínimas y plazos de evaluación vigentes para un programa en un periodo (`ADR-007`). | `ReglaPractica` |
| **Estudiante** | Estudiante de la Facultad que se postula a la práctica, registra sus horas semanales y consulta su trámite. Solo ve su propia información (`RN-01`). | `Estudiante` |
| **Postulación** | Solicitud que presenta el estudiante ante la Facultad para iniciar su práctica empresarial (`CU-01`, `CU-02`). | `Postulacion` |
| **Estado de la postulación** | Situación de la postulación: `PENDIENTE_VERIFICACION`, `CUMPLE_REQUISITOS`, `NO_CUMPLE`, `APROBADA` o `RECHAZADA`. | `EstadoPostulacion` |
| **Verificación de requisitos** | Cada intento de consulta al SIA para comprobar si el estudiante cumple las reglas de práctica de su programa (`ADR-002`, `ADR-003`). | `VerificacionRequisitos` |
| **Práctica** | Práctica empresarial en curso, originada por una postulación aprobada y ligada a la versión de reglas con la que empezó (`OB-05`). | `Practica` |
| **Estado de la práctica** | Situación de la práctica empresarial: `EN_CURSO`, `HORAS_CUMPLIDAS`, `EVALUADA` o `CERRADA`. | `EstadoPractica` |
| **Empresa** | Organización externa con convenio vigente donde el estudiante realiza su práctica. | `Empresa` |
| **Supervisor de empresa** | Persona externa en la empresa que valida las horas semanales y evalúa el desempeño del practicante sin tener cuenta en el sistema (`RN-04`). | `SupervisorEmpresa` |
| **Docente asesor** | Docente de la Facultad asignado para acompañar la práctica, revisar el avance de horas y aprobar el acta final. Solo ve las prácticas que asesora (`RN-01`). | `DocenteAsesor` |
| **Director de programa** | Coordinador de prácticas del programa académico: aprueba o rechaza postulaciones, asigna docente asesor, configura reglas y aprueba el acta final. | `DirectorPrograma` |
| **Administrador del sistema** | Rol interno encargado de asignar roles institucionales y ejecutar la migración inicial de prácticas en curso (`CU-15`). | `AdministradorSistema` |
| **Registro de horas** | Reporte de las horas trabajadas por el estudiante en una semana, pendiente de validación por el supervisor (`CU-04`, `CU-05`). | `RegistroHoras` |
| **Evaluación** | Calificación y observaciones que el supervisor de empresa registra sobre el desempeño del practicante y que alimentan el acta final (`CU-07`, `S-01`). | `Evaluacion` |
| **Enlace de acceso** | Enlace de un solo uso con vigencia de 15 días enviado por correo al supervisor para validar horas o evaluar al practicante (`ADR-005`, `EAC-03`). | `EnlaceAcceso` |
| **Estado del enlace** | Situación del enlace de acceso del supervisor: `VIGENTE`, `USADO` o `VENCIDO`. | `EstadoEnlace` |
| **Acta** | Documento académico oficial que cierra la práctica empresarial; una vez aprobada no se modifica ni se borra (`CU-09`, `RN-02`). | `Acta` |
| **Estado del acta** | Situación del acta final: `PENDIENTE_APROBACION`, `EN_CORRECCION`, `APROBADA` o `ANULADA`. | `EstadoActa` |
| **Plantilla de acta** | Formato oficial versionado, separado del código, con el que se genera el PDF del acta (`ADR-008`, `RN-03`). | `PlantillaActa` |
| **Aprobación de acta** | Decisión trazable (aprobación o rechazo con observaciones) registrada por el docente asesor o el director de programa sobre un acta (`CU-10`, `S-06`). | `AprobacionActa` |
| **Evento de bitácora** | Registro inmutable de solo inserción con fecha, hora, usuario o enlace, acción, dirección de origen y práctica asociada (`ADR-006`). | `EventoBitacora` |
| **Consulta académica** | Puerto de salida mediante el cual la aplicación consulta en el SIA los datos académicos del estudiante sin acoplarse a su servicio (`ADR-002`). | `ConsultaAcademica` |
| **Publicador de mensajes** | Puerto de salida para encolar en el bróker las verificaciones pendientes con el SIA y los correos por enviar (`ADR-003`). | `PublicadorMensajes` |
| **Notificador** | Puerto de salida para el envío de notificaciones, recordatorios y enlaces de acceso por el servicio de correo institucional. | `Notificador` |
| **Generador de acta** | Puerto de salida que toma los datos de la práctica y la plantilla vigente para producir el archivo PDF del acta (`ADR-008`). | `GeneradorActa` |
| **Repositorio de documentos** | Puerto de salida para almacenar y leer los PDF de las actas en el almacenamiento institucional sin borrado (`ADR-009`). | `RepositorioDocumentos` |
