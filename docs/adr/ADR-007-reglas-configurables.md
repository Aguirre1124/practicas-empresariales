# ADR-007: Guardar las reglas de práctica como datos por programa, versionadas por periodo

## Estado

Aceptado — 2026-11-09

## Contexto

- Cada programa tiene requisitos académicos y horas mínimas distintos (S-07), y un cambio del reglamento debe aplicarse desde el periodo siguiente sin suspender las prácticas en curso (OB-05).
- CU-12 (configurar las reglas de un programa) es primario por mantenibilidad.
- EAC-01: un desarrollador con un mes en el proyecto incorpora un programa nuevo en máximo 16 horas, modificando como máximo 2 módulos y sin que cambien las reglas de prácticas en curso de otros programas.

## Alternativas consideradas

- **A) Reglas escritas en el código, con un `if` por programa.** Rápido al inicio. Cada programa nuevo es un cambio de código en varios lugares y un despliegue; viola la idea de EAC-01 a medida que crecen los programas.
- **B) Un motor de reglas externo (por ejemplo, Drools).** Muy flexible. Pero es una herramienta grande para reglas que son básicamente números y una lista de requisitos, y suma una tecnología que el Área de Sistemas debe aprobar (RT-04).
- **C) Reglas como datos: cada programa tiene un conjunto de reglas (horas mínimas, requisitos académicos, plazos) con un periodo de vigencia.** El director las configura desde la aplicación (CU-12). Cada práctica guarda la versión de reglas con la que empezó.
- **D) Una clase por programa que implementa una interfaz común.** Cumple el principio abierto/cerrado. Pero cada programa nuevo sigue siendo un despliegue hecho por un desarrollador.

## Decisión

Se elige **C**. Un programa nuevo con reglas del mismo tipo no requiere código: lo configura el director (CU-12). Si aparece un tipo de requisito nuevo, el cambio queda dentro del módulo de reglas y su adaptador del SIA, es decir, máximo 2 módulos (EAC-01). Como cada práctica queda ligada a su versión de reglas, cambiar las reglas no afecta las prácticas en curso (OB-05).

## Consecuencias

**Positivas**
- La mayoría de los cambios de reglas no requieren desarrollador ni despliegue.
- Las prácticas en curso conservan sus reglas (OB-05).
- Queda historial de qué reglas aplicaban en cada periodo, útil para auditoría (OB-06).

**Negativas y costos aceptados**
- Un requisito de un tipo que no existe (por ejemplo, un examen de inglés) sí requiere programar; la configuración solo cubre los tipos previstos.
- Hay que construir y probar la pantalla de configuración, que es más trabajo que escribir las reglas en código.
- Un director puede configurar una regla mal; la aplicación debe validar y mostrar un resumen antes de guardar.

**Riesgos asumidos**
- Que los programas tengan reglas muy distintas a las previstas. Mitigación: revisar los reglamentos de todos los programas antes de definir los tipos de regla (validar S-07).

**Vistas que modifica:** [lógica](../vistas/01-logica.md) (Programa y ReglaPractica), [desarrollo](../vistas/03-desarrollo.md) (Módulo Reglas) y la secuencia de [CU-12](../diagramas/secuencias/cu12-configurar-reglas.puml).
