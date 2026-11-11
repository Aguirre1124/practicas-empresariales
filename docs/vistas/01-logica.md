# Vista lógica: modelo de dominio

Muestra los conceptos del negocio y cómo se relacionan. No tiene tipos, métodos ni elementos técnicos: la entiende cualquier stakeholder, incluido el director de programa.

Para: usuarios finales y analistas.

## 1. Presentación principal

Diagrama UML: [../diagramas/01-logica.puml](../diagramas/01-logica.puml).

## 2. Catálogo de elementos

| Entidad | Qué representa | Atributos clave | Regla del negocio |
|---|---|---|---|
| Programa | Un programa académico de la Facultad | nombre | Cada programa tiene sus propias reglas de práctica (S-07) |
| ReglaPractica | Las reglas de un programa para un periodo | periodo de vigencia, horas mínimas, requisitos académicos, plazo de evaluación | Es un dato, no código; una versión nueva no cambia las prácticas en curso (ADR-007) |
| Estudiante | Quien se postula a la práctica | documento, nombre, correo institucional | Solo ve su propio trámite (RN-01) |
| Postulacion | La solicitud del estudiante ante la Facultad | fecha, estado | Estados: pendiente de verificación, cumple requisitos, no cumple, aprobada, rechazada |
| VerificacionRequisitos | Cada consulta al SIA para verificar requisitos | número de intento, fecha, resultado | Se reintenta hasta que el SIA responde; ninguna postulación queda sin verificar (ADR-003) |
| Practica | La práctica en curso, una vez aprobada la postulación | fecha de inicio, fecha de fin, estado | Queda ligada a la versión de reglas con la que empezó (OB-05) |
| Empresa | La organización donde se hace la práctica | nombre, NIT | Solo se consulta si el convenio está vigente (fuera de alcance gestionarlo) |
| SupervisorEmpresa | Quien supervisa al practicante en la empresa | nombre, correo | No tiene cuenta en el sistema (RN-04) |
| DocenteAsesor | El docente que acompaña la práctica | nombre, correo institucional | Solo ve las prácticas que asesora (RN-01) |
| RegistroHoras | Las horas de una semana | semana, horas, estado de validación | El estudiante las registra y el supervisor las valida (S-05) |
| Evaluacion | La evaluación del supervisor al practicante | fecha, nota, observaciones | Una por práctica; su nota alimenta el acta (S-01) |
| EnlaceAcceso | El enlace que recibe el supervisor | propósito, fecha de emisión, fecha de vencimiento, estado | Un solo uso, vence a los 15 días (ADR-005, EAC-03) |
| Acta | El acta final de la práctica | número, fecha de generación, estado | Una vez aprobada no se modifica ni se borra; si hay error se anula y se emite otra (RN-02) |
| PlantillaActa | El formato oficial del acta | versión, vigente desde | Cambiarla no requiere programar (RN-03, ADR-008) |
| AprobacionActa | La aprobación de un acta por una persona | rol del aprobador, fecha y hora, decisión | Requiere la del docente asesor y la del director de programa (S-06) |
| EventoBitacora | Un hecho relevante que queda registrado | fecha y hora, usuario o enlace, acción, dirección de origen | Solo inserción (ADR-006) |

## 3. Justificación

- **CU-01:** de aquí salen Postulacion y VerificacionRequisitos.
- **CU-07 y RN-04:** SupervisorEmpresa, Evaluacion y EnlaceAcceso. El supervisor es una entidad del dominio, no un usuario con cuenta.
- **CU-09, RN-03 y ADR-008:** Acta y PlantillaActa; cada acta sabe con qué versión de plantilla se generó.
- **CU-10, PA-03 y ADR-006:** AprobacionActa y EventoBitacora dejan rastro de quién aprobó y cuándo (OB-06).
- **CU-12, EAC-01 y ADR-007:** ReglaPractica es un dato con periodo de vigencia; un programa nuevo es un registro nuevo, no una clase nueva.
- **EAC-02 y ADR-003:** VerificacionRequisitos guarda cada intento contra el SIA; si el SIA falla, la postulación sigue existiendo en estado pendiente.
- **EAC-03 y ADR-005:** EnlaceAcceso tiene estado y vencimiento, que es lo que permite rechazar un enlace usado o vencido.
- **RN-01:** cada Practica tiene un único DocenteAsesor y un único Estudiante, que son la base de los permisos por práctica (ADR-004).
- **RN-02:** Acta y EventoBitacora no se borran.

## 4. Comportamiento

Los escenarios de [drivers.md, sección 6](../drivers.md#6-escenarios) cambian el estado de estas entidades:

- CU-01: la Postulacion pasa de pendiente de verificación a cumple o no cumple; cada consulta al SIA crea una VerificacionRequisitos.
- CU-07: el EnlaceAcceso pasa de vigente a usado y se crea la Evaluacion.
- CU-09 y CU-10: se crea el Acta y luego dos AprobacionActa.
- CU-12: se crea una versión nueva de ReglaPractica.

## 5. Vistas relacionadas

- [Desarrollo](03-desarrollo.md): estas entidades viven en la capa de dominio y los módulos de casos de uso las usan.
- [Procesos](02-procesos.md): se guardan en la Base de datos; los PDF del Acta, en el Repositorio de documentos.
