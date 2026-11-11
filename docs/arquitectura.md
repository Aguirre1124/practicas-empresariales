# Documento de arquitectura: Sistema de Gestión de Prácticas Empresariales

Este documento consolida la arquitectura y enlaza a los demás archivos de `docs/` en lugar de copiar su contenido.

## 1. Introducción y objetivos

Los objetivos de negocio están en [vision.md, sección 2](vision.md#2-objetivos-de-negocio) (OB-01 a OB-06).

## 2. Restricciones

Las restricciones técnicas (RT-01 a RT-04) y de negocio (RN-01 a RN-05), con su tipo, origen e impacto arquitectónico, están en [drivers.md, sección 3](drivers.md#3-restricciones).

## 3. Contexto del sistema

El sistema como caja negra, con sus actores y sistemas externos, está en [contexto.md](contexto.md).

## 4. Estrategia de solución

*Pendiente.*

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

*Pendiente.*

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

Los escenarios de atributos de calidad (EAC-01 a EAC-03) están en [drivers.md, sección 2](drivers.md#2-escenarios-de-atributos-de-calidad).

## 9. Riesgos y deuda técnica

*Pendiente.*
