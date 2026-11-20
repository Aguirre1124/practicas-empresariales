# language: es
# Traza: CU-01, EAC-02, RT-02, RT-03, RN-01, S-04, S-07, ADR-002, ADR-003, ADR-004, ADR-006, ADR-007
Característica: Postularse a la práctica empresarial
  Como Estudiante autenticado con cuenta institucional
  quiero presentar mi postulación a la práctica empresarial con los datos de la empresa y del supervisor
  para que se verifiquen mis requisitos académicos frente a las reglas vigentes de mi programa.

  Escenario: Postulación recibida y verificada cuando el estudiante cumple requisitos académicos
    Dado un Estudiante autenticado del Programa "Ingeniería de Sistemas" sin postulaciones en trámite en el periodo "2026-2"
    Y una Regla de práctica vigente para el Programa "Ingeniería de Sistemas" en el periodo "2026-2" que exige mínimo 80% de créditos aprobados y matrícula activa
    Y que en el SIA el Estudiante tiene 85% de créditos aprobados y matrícula activa en el periodo "2026-2"
    Cuando el Estudiante envía su Postulación para el periodo "2026-2" con la Empresa "TechCorp S.A.S.", NIT "900123456-7", Supervisor de empresa "Carlos Pérez" y correo "cperez@techcorp.com"
    Entonces la Postulación se guarda en estado "pendiente de verificación" con los datos de la Empresa y del Supervisor de empresa
    Y el Estudiante recibe la confirmación "Recibida, estamos verificando tus requisitos"
    Y al completarse la Consulta académica en el SIA se registra la Verificación de requisitos en el intento 1 con resultado exitoso
    Y la Postulación pasa al estado "cumple requisitos"
    Y se registra el Evento de bitácora del cambio de estado de la Postulación
    Y el Estudiante recibe por correo el resultado "cumple requisitos"

  Escenario: Postulación verificada cuando el estudiante no cumple alguno de los requisitos académicos
    Dado un Estudiante autenticado del Programa "Ingeniería de Sistemas" sin postulaciones en trámite en el periodo "2026-2"
    Y una Regla de práctica vigente para el Programa "Ingeniería de Sistemas" en el periodo "2026-2" que exige mínimo 80% de créditos aprobados y matrícula activa
    Y que en el SIA el Estudiante tiene 72% de créditos aprobados y matrícula activa en el periodo "2026-2"
    Cuando el Estudiante envía su Postulación para el periodo "2026-2" con la Empresa "TechCorp S.A.S.", NIT "900123456-7", Supervisor de empresa "Carlos Pérez" y correo "cperez@techcorp.com"
    Entonces la Postulación se guarda inicialmente en estado "pendiente de verificación"
    Y al completarse la Consulta académica en el SIA se registra la Verificación de requisitos en el intento 1 indicando que falló el requisito de mínimo 80% de créditos aprobados
    Y la Postulación pasa al estado "no cumple requisitos"
    Y se registra el Evento de bitácora del cambio de estado de la Postulación
    Y el Estudiante recibe por correo el resultado "no cumple requisitos" indicando el requisito que falló

  Escenario: Postulación rechazada por tener otra postulación en trámite en el mismo periodo
    Dado un Estudiante autenticado del Programa "Ingeniería de Sistemas"
    Y que el Estudiante ya tiene una Postulación en el periodo "2026-2" en estado "pendiente de verificación", "cumple requisitos" o "aprobada"
    Cuando el Estudiante intenta enviar una nueva Postulación para el periodo "2026-2" con la Empresa "Innova S.A.S.", NIT "900987654-3", Supervisor de empresa "Ana Gómez" y correo "agomez@innova.com"
    Entonces el sistema rechaza la solicitud sin guardar una nueva Postulación
    Y no realiza ni encola ninguna Consulta académica hacia el SIA
    Y muestra al Estudiante el mensaje "Ya tienes una postulación en trámite para este periodo"

  Escenario: Nueva postulación permitida cuando la anterior del mismo periodo quedó en no cumple requisitos o rechazada
    Dado un Estudiante autenticado del Programa "Ingeniería de Sistemas"
    Y que su única Postulación previa en el periodo "2026-2" está en estado "no cumple requisitos" o "rechazada"
    Y una Regla de práctica vigente para el Programa "Ingeniería de Sistemas" en el periodo "2026-2" que exige mínimo 80% de créditos aprobados y matrícula activa
    Cuando el Estudiante envía una nueva Postulación para el periodo "2026-2" con la Empresa "TechCorp S.A.S.", NIT "900123456-7", Supervisor de empresa "Carlos Pérez" y correo "cperez@techcorp.com"
    Entonces la nueva Postulación se guarda en estado "pendiente de verificación"
    Y el Estudiante recibe la confirmación "Recibida, estamos verificando tus requisitos"

  Escenario: Postulación rechazada cuando faltan datos obligatorios de la empresa o el NIT no tiene formato válido
    Dado un Estudiante autenticado del Programa "Ingeniería de Sistemas" sin postulaciones en trámite en el periodo "2026-2"
    Cuando el Estudiante intenta enviar su Postulación con el NIT "ABC-INVALIDO" o sin el correo del Supervisor de empresa
    Entonces el sistema rechaza la solicitud sin guardar la Postulación ni consultar el SIA
    Y le indica al Estudiante qué dato obligatorio falta o tiene formato inválido

  Escenario: Tolerancia a fallos cuando el SIA no responde durante la postulación (EAC-02)
    Dado el sistema en operación normal en el pico de inicio de periodo con hasta 30 usuarios concurrentes
    Y un Estudiante autenticado del Programa "Ingeniería de Sistemas" sin postulaciones en trámite en el periodo "2026-2"
    Y una Regla de práctica vigente para el Programa "Ingeniería de Sistemas" en el periodo "2026-2"
    Y que el servicio de Consulta académica del SIA no responde en 5 segundos o responde con error
    Cuando el Estudiante envía su Postulación para el periodo "2026-2" con la Empresa "TechCorp S.A.S.", NIT "900123456-7", Supervisor de empresa "Carlos Pérez" y correo "cperez@techcorp.com"
    Entonces la Postulación queda guardada en estado "pendiente de verificación" con 0 postulaciones perdidas
    Y el Estudiante recibe la confirmación "Recibida, estamos verificando tus requisitos" en menos de 3 segundos en el 95% de los casos
    Y se registra una Verificación de requisitos con el intento fallido
    Y el sistema reintenta automáticamente la Consulta académica con espera creciente hasta que el SIA responde
    Y la verificación se completa dejando la Postulación en "cumple requisitos" o "no cumple requisitos" en máximo 30 minutos después de que el SIA se recupera en el 100% de los casos
