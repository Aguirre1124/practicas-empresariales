# ADR-008: Generar el acta final en PDF a partir de una plantilla separada del código

## Estado

Aceptado — 2026-11-09

## Contexto

- CU-09 (generar el acta final) es la razón de ser del sistema; de ella dependen OB-01 (acta en máximo 5 días hábiles) y OB-04 (menos del 1% de actas reemitidas por errores).
- RN-03: el acta debe seguir el formato y contenido del reglamento de prácticas, y ese formato lo define el Consejo de Facultad, que puede cambiarlo.
- Los datos del acta ya están en el sistema (horas validadas, evaluación del supervisor, datos del SIA), así que no hay que transcribir nada.

## Alternativas consideradas

- **A) Construir el PDF desde el código, línea por línea.** Control total. Pero cualquier cambio de formato del Consejo obliga a programar y desplegar, lo que va contra RN-03.
- **B) Plataforma comercial de generación de documentos.** Editor visual para no programadores. **Descartada por RN-05** (licencia de pago recurrente).
- **C) Plantilla HTML con marcadores, guardada aparte del código, que se llena con los datos de la práctica y se convierte a PDF con una librería libre.** La plantilla tiene versiones y cada acta guarda con qué versión se generó.

## Decisión

Se elige **C**. Cumple RN-03 porque el formato cambia editando la plantilla, sin tocar el código, y cumple RN-05 porque usa librerías libres. Los datos salen directamente del sistema, lo que ataca los errores de transcripción (OB-04).

## Consecuencias

**Positivas**
- Un cambio de formato del Consejo se aplica cambiando la plantilla (RN-03).
- El acta se arma con datos que ya están validados: no hay retranscripción (OB-04).
- Se puede saber con qué plantilla se generó cada acta.

**Negativas y costos aceptados**
- Editar la plantilla requiere saber algo de HTML; no la puede editar cualquier funcionario.
- La conversión de HTML a PDF no siempre respeta el diseño al milímetro; hay que probar el resultado con cada versión de la plantilla.
- El acta generada no tiene firma digital certificada; su validez depende de la aprobación trazable del [ADR-006](ADR-006-bitacora-auditoria.md) (S-06).

**Riesgos asumidos**
- Que se exija firma digital certificada (R-03). Mitigación: validar S-06 con el área jurídica; si se exige, se escribe un ADR nuevo.

**Vistas que modifica:** [lógica](../vistas/01-logica.md) (Acta y PlantillaActa), [desarrollo](../vistas/03-desarrollo.md) (Módulo Actas y Generador de PDF) y la secuencia de [CU-09](../diagramas/secuencias/cu09-generar-acta.puml).
