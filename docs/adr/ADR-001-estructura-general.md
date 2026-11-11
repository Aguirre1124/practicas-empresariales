# ADR-001: Construir el sistema como un monolito modular con Clean Architecture

## Estado

Aceptado — 2026-11-09

## Contexto

Hay que decidir en qué grandes bloques se divide el sistema y hacia dónde apuntan sus dependencias (PA-01).

- La carga es baja: entre 170 y 250 prácticas activas a la vez y decenas de usuarios concurrentes (S-03). No justifica una arquitectura distribuida, y sobredimensionar es un riesgo identificado (R-04).
- Las reglas sí cambian: cada programa tiene requisitos y horas distintos (S-07) y un cambio del reglamento debe aplicarse sin detener las prácticas en curso (OB-05). EAC-01 pide que un desarrollador nuevo incorpore un programa en máximo 16 horas tocando como máximo 2 módulos.
- El Área de Sistemas opera el sistema con su personal y solo soporta las tecnologías de su catálogo (RT-01, RT-04).
- Los casos de uso primarios (CU-01, CU-07, CU-09, CU-10 y CU-12) comparten las mismas entidades: práctica, estudiante, reglas del programa y acta.

## Alternativas consideradas

- **A) Monolito en capas tradicional (presentación, negocio, datos).** Simple y conocido. Pero las capas se organizan por tipo técnico, no por funcionalidad: un cambio de reglas toca las tres capas, y el negocio queda atado a la base de datos. Pone en riesgo EAC-01.
- **B) Microservicios (postulaciones, seguimiento, actas, reglas).** Cada servicio cambia y se despliega solo. Pero multiplica servidores, bases de datos y monitoreo para una carga que no lo necesita (S-03, R-04), y el Área de Sistemas tendría que operar varios servicios con el mismo personal (RT-01).
- **C) Monolito modular con Clean Architecture.** Un solo desplegable, dividido por dentro en módulos por funcionalidad (postulaciones, seguimiento, evaluación, actas, reglas, auditoría). Cada módulo sigue las capas dominio, aplicación e infraestructura, y las dependencias apuntan hacia el dominio.

## Decisión

Se elige **C**. Es la única opción que atiende a la vez la baja carga (S-03, R-04) y la necesidad de cambiar reglas sin afectar al resto (OB-05, EAC-01): el cambio de un programa queda dentro del módulo de reglas, y la infraestructura (base de datos, SIA, correo) queda detrás de puertos.

## Consecuencias

**Positivas**
- Un solo desplegable que el Área de Sistemas puede operar con su personal (RT-01).
- Los cambios de reglas quedan aislados en un módulo (EAC-01).
- Cambiar la base de datos o el adaptador del SIA no toca el dominio.

**Negativas y costos aceptados**
- Todo el sistema se despliega junto: un error en un módulo obliga a redesplegar todo.
- La separación entre módulos depende de la disciplina del equipo; nada en el lenguaje impide que un módulo importe a otro por dentro. Hay que revisar las importaciones en cada Pull Request.
- No se puede escalar un módulo por separado. Se acepta porque la carga no lo exige (S-03).

**Riesgos asumidos**
- Si la carga crece mucho más de lo previsto (otras facultades), habría que separar módulos en servicios. Mitigación: como los módulos ya están separados por puertos, extraer uno no obliga a reescribirlo.

**Vistas que modifica:** [procesos](../vistas/02-procesos.md) (un solo contenedor de API) y [desarrollo](../vistas/03-desarrollo.md) (módulos y capas).
