# ADR-003: Procesar la verificación con el SIA y los correos por un bróker de mensajes con reintentos

## Estado

Aceptado — 2026-11-09

## Contexto

- EAC-02: si el SIA no responde en 5 segundos durante una postulación (CU-01), el sistema debe guardar la postulación como pendiente, confirmar al estudiante en menos de 3 segundos (95% de los casos), completar la verificación en máximo 30 minutos después de que el SIA se recupera y no perder ninguna postulación.
- Esas dos medidas chocan con una llamada síncrona: esperar 5 segundos al SIA ya incumple los 3 segundos de confirmación.
- PA-04 pide una sola estrategia de fallas para el SIA y para el correo institucional, que se usa en los recordatorios de evaluación (CU-07, CU-08) y en las notificaciones.
- RT-01 descarta colas gestionadas de nube pública, y RN-05 descarta productos con licencia de pago recurrente.

## Alternativas consideradas

- **A) Llamada síncrona al SIA con tiempo límite.** Simple, sin infraestructura nueva. Incumple EAC-02: el estudiante espera hasta 5 segundos y, si el SIA falla, la postulación queda sin verificar y nadie la retoma.
- **B) Tabla de pendientes en la base de datos y una tarea programada que la recorre cada pocos minutos.** No agrega infraestructura y nada se pierde. Pero cada tipo de trabajo (verificar, enviar correo) necesita su propia tabla y su propia lógica de reintento, y la verificación tarda lo que tarde la siguiente vuelta de la tarea.
- **C) Bróker de mensajes (RabbitMQ) con colas persistentes y un worker que consume y reintenta.** La API guarda la postulación como "pendiente de verificación", publica un mensaje y responde. El worker consulta el SIA y reintenta con espera creciente si falla. El mismo mecanismo sirve para los correos.
- **D) Cola gestionada de un proveedor de nube (por ejemplo, Amazon SQS).** Sin servidor que operar. **Descartada por RT-01.**

## Decisión

Se elige **C**. Es la opción que cumple EAC-02 completo (respuesta inmediata y cero pérdidas) y da una sola estrategia de reintentos para el SIA y el correo (PA-04). RabbitMQ es software libre (RN-05) y se instala en la infraestructura de la Universidad (RT-01).

## Consecuencias

**Positivas**
- El estudiante recibe la confirmación sin esperar al SIA (EAC-02).
- Ninguna postulación ni correo se pierde: los mensajes sobreviven a un reinicio.
- Una sola forma de manejar fallas de integración (PA-04).

**Negativas y costos aceptados**
- Se agregan dos contenedores (bróker y worker) que el Área de Sistemas debe operar y monitorear.
- La postulación pasa a un flujo de "enviar y esperar": el estudiante no ve el resultado de la verificación en el momento, y la interfaz debe explicarlo.
- Depurar es más difícil: un error puede estar en la API, en la cola o en el worker.

**Riesgos asumidos**
- Si el SIA cae varios días, la cola crece. Mitigación: alerta al superar 100 mensajes pendientes y aviso al director de programa.
- El equipo debe aprender a operar RabbitMQ. Mitigación: confirmar con el Área de Sistemas que lo acepta en su catálogo (RT-04); si no lo acepta, se vuelve a la alternativa B con un ADR nuevo.

**Vistas que modifica:** [procesos](../vistas/02-procesos.md) (bróker y worker), [física](../vistas/04-fisica.md) (servidor de mensajería), [lógica](../vistas/01-logica.md) (VerificacionRequisitos) y la secuencia de [CU-01](../diagramas/secuencias/cu01-postularse.puml).
