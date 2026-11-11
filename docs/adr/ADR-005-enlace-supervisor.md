# ADR-005: Dar acceso al supervisor de empresa con un enlace de un solo uso que vence en 15 días

## Estado

Aceptado — 2026-11-09

## Contexto

- RN-04 prohíbe exigir al supervisor de empresa una cuenta institucional o un registro con contraseña.
- CU-07 (evaluar al practicante) es primario por riesgo: si el supervisor no responde no hay acta (R-01, OB-02). El trámite debe tomarle pocos minutos.
- EAC-03: un enlace ya usado, con más de 15 días o alterado se rechaza en el 100% de los casos, sin mostrar datos personales, y el intento queda en la bitácora en menos de 1 minuto.
- PA-02 pide que este segundo mecanismo conviva con el inicio de sesión institucional del [ADR-004](ADR-004-autenticacion-institucional.md). CU-05 (validar horas) usa el mismo acceso.

## Alternativas consideradas

- **A) Cuenta con contraseña para el supervisor.** **Descartada por RN-04.**
- **B) Código de un solo uso enviado por correo cada vez que entra.** Seguro, pero agrega un paso en cada ingreso y pone en riesgo OB-02.
- **C) Token firmado sin estado (por ejemplo, JWT) con fecha de vencimiento.** No necesita guardar nada. Pero no se puede marcar como usado sin guardarlo, así que incumple EAC-03 (un enlace usado debe rechazarse).
- **D) Enlace con un identificador aleatorio largo, guardado en la base de datos con su vencimiento (15 días) y su estado (vigente o usado).** Al usarlo se marca como usado; cualquier enlace vencido, usado o inexistente se rechaza y se registra.

## Decisión

Se elige **D**. Es la única opción que cumple RN-04 sin pasos extra para el supervisor y que permite rechazar enlaces usados, como exige EAC-03.

## Consecuencias

**Positivas**
- El supervisor evalúa con un clic desde su correo (RN-04, R-01).
- Cada enlace se puede anular o reemitir desde el sistema.
- Cada intento rechazado queda en la bitácora con fecha, hora y dirección de origen (EAC-03).

**Negativas y costos aceptados**
- Quien tenga el correo del supervisor puede usar el enlace antes que él; el enlace prueba que se tiene el correo, no la identidad de la persona.
- Si el supervisor abre el enlace y no termina, hay que reemitirlo. Se acepta a cambio de no pedir contraseña.
- Hay que guardar y limpiar los enlaces vencidos.

**Riesgos asumidos**
- Que el área jurídica considere insuficiente esta forma de identificar al supervisor. Mitigación: validarlo junto con S-06.

**Vistas que modifica:** [lógica](../vistas/01-logica.md) (EnlaceAcceso), [desarrollo](../vistas/03-desarrollo.md) (Módulo Acceso externo) y la secuencia de [CU-07](../diagramas/secuencias/cu07-evaluar-practicante.puml).
