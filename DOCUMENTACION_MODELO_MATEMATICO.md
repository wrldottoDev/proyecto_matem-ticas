# Documentación Del Modelo Matemático De ¿Ahí es?

Este documento resume cómo explicar el funcionamiento interno del test desde la perspectiva de modelos matemáticos, lógica booleana, ponderación y teoría de grafos.

## 1. Idea General Del Sistema

`¿Ahí es?` es un test relacional que evalúa señales positivas, señales dudosas y señales de alerta dentro de un vínculo.

El sistema no usa una sola pregunta para decidir el resultado. En cambio, combina:

- Un **grafo dirigido** de preguntas.
- Una **suma acumulada de puntajes** por dimensión.
- Una **ponderación matemática** de dimensiones.
- Una **normalización** a escala `0 - 100`.
- Una **clasificación por umbrales**.
- Una **lógica booleana** para detectar finales, rutas y contradicciones.

El resultado final puede ser:

- `Green Flag`
- `Zona Gris`
- `Red Flag`

## 2. Modelo De Grafo Dirigido

El cuestionario se modela como un **grafo dirigido**.

En teoría de grafos:

- Cada pregunta es un **nodo**.
- Cada respuesta es una **arista dirigida**.
- La arista puede llevar de una pregunta actual a una siguiente pregunta.
- Algunas preguntas son terminales y cierran el recorrido.

En código, el grafo está definido principalmente en:

```text
backend/app/utils/seed_data.py
```

Cada nodo tiene una estructura como:

```python
{
    "key": "rel_inicio",
    "text": "¿Cómo describirías la comunicación cotidiana con esa persona?",
    "main_dimension": D.comunicacion.value,
    "is_start": True,
    "options": [...]
}
```

Cada opción puede apuntar a otro nodo:

```python
{
    "text": "Es constante, clara y no me deja adivinando",
    "effects": {
        D.comunicacion.value: 5,
        D.interes_real.value: 3,
    },
    "next": "honestidad_base",
}
```

Matemáticamente:

```text
G = (V, E)
```

Donde:

- `V` es el conjunto de preguntas.
- `E` es el conjunto de respuestas que conectan preguntas.

Ejemplo de ruta:

```text
rel_inicio -> honestidad_base -> coherencia_palabras_acciones -> limites_base
```

Esto permite que el test sea adaptativo: no todos los usuarios responden exactamente las mismas preguntas.

## 3. Dimensiones Del Modelo

El sistema evalúa varias dimensiones relacionales:

- Comunicación
- Respeto
- Coherencia
- Responsabilidad afectiva
- Interés real
- Honestidad
- Confianza
- Límites personales
- Manipulación
- Celos/control
- Disponibilidad emocional
- Compromiso
- Empatía
- Resolución de conflictos
- Reciprocidad

En código están en:

```text
backend/app/core/enums.py
```

Cada dimensión funciona como una variable del modelo.

Podemos representar el estado acumulado del test como un vector:

```text
S = [s1, s2, s3, ..., s15]
```

Donde cada `si` representa el puntaje acumulado de una dimensión.

Por ejemplo:

```text
S = [
  comunicacion,
  respeto,
  coherencia,
  responsabilidad_afectiva,
  interes_real,
  ...
]
```

## 4. Suma De Puntajes

Cada respuesta tiene efectos sobre una o varias dimensiones.

Ejemplo:

```python
"effects": {
    D.comunicacion.value: 5,
    D.interes_real.value: 3,
    D.disponibilidad_emocional.value: 2,
}
```

Eso significa:

```text
comunicacion += 5
interes_real += 3
disponibilidad_emocional += 2
```

La suma se hace en:

```text
backend/app/services/session_service.py
```

Función:

```python
calculate_session_result()
```

Parte clave:

```python
raw_scores = empty_dimension_scores()

for answer in answers:
    for effect in answer.option.effects:
        raw_scores[Dimension(effect.dimension)] += effect.value
```

Matemáticamente, si el usuario responde `n` preguntas:

```text
S_total = R1 + R2 + R3 + ... + Rn
```

Donde cada `Ri` es el vector de efectos de una respuesta.

## 5. Escala De Pesos Por Respuesta

Cada opción puede sumar o restar según su intensidad.

La escala usada es:

```text
Green flags fuertes:       +4 a +6
Green flags moderadas:     +2 a +3
Neutras o dudosas:          0 a -1
Red flags moderadas:       -3 a -5
Red flags fuertes:         -6 a -10
Contradicciones graves:    -5 a -10 adicionales
```

Ejemplo positivo fuerte:

```python
"effects": {
    D.respeto.value: 6,
    D.limites_personales.value: 6,
    D.responsabilidad_afectiva.value: 3,
}
```

Ejemplo negativo fuerte:

```python
"effects": {
    D.celos_control.value: -10,
    D.respeto.value: -8,
    D.confianza.value: -7,
}
```

## 6. Normalización

Los puntajes brutos pueden ser negativos o positivos. Para poder compararlos, el sistema los transforma a una escala de `0` a `100`.

La normalización está en:

```text
backend/app/core/scoring.py
```

Función:

```python
normalize_dimension()
```

Fórmula:

```text
valor_normalizado = ((valor_bruto - minimo) / (maximo - minimo)) * 100
```

Actualmente:

```text
minimo = -20
maximo = 20
```

Ejemplos:

```text
valor_bruto = -20 -> 0
valor_bruto = 0   -> 50
valor_bruto = 20  -> 100
```

Esto permite que todas las dimensiones queden en la misma escala.

## 7. Ponderación Del Resultado

No todas las dimensiones pesan igual.

El sistema usa pesos definidos en:

```text
backend/app/core/scoring.py
```

Ejemplo:

```python
DIMENSION_WEIGHTS = {
    Dimension.comunicacion: 0.07,
    Dimension.respeto: 0.08,
    Dimension.confianza: 0.08,
    Dimension.manipulacion: 0.08,
    ...
}
```

Los pesos suman `1.0`.

Fórmula del resultado final:

```text
F = (d1_normalizada * peso1)
  + (d2_normalizada * peso2)
  + ...
  + (d15_normalizada * peso15)
```

En forma compacta:

```text
F = Σ(di * wi)
```

Donde:

- `di` es la dimensión normalizada.
- `wi` es el peso de esa dimensión.
- `F` es el puntaje final.

En código:

```python
def calculate_final_score(normalized_scores):
    return round(
        sum(
            normalized_scores.get(dimension, 0.0) * weight
            for dimension, weight in DIMENSION_WEIGHTS.items()
        ),
        2,
    )
```

## 8. Clasificación Por Umbrales

Después de obtener el puntaje final `F`, el sistema clasifica el resultado.

La lógica está en:

```text
backend/app/core/scoring.py
```

Función:

```python
classify_score()
```

Reglas:

```text
F >= 70       -> Green Flag
40 <= F < 70  -> Zona Gris
F < 40        -> Red Flag
```

En código:

```python
def classify_score(score: float) -> FinalResult:
    if score >= 70:
        return FinalResult.green_flag
    if score >= 40:
        return FinalResult.zona_gris
    return FinalResult.red_flag
```

## 9. Lógica Booleana

La lógica booleana aparece en decisiones de flujo y contradicciones.

### 9.1 Decisión De Terminar O Continuar

En:

```text
backend/app/services/session_service.py
```

Código:

```python
should_finish = question.is_terminal or option.next_question_link is None
```

Esto significa:

```text
termina = pregunta_terminal OR no_existe_siguiente_pregunta
```

Tabla lógica:

| is_terminal | tiene siguiente pregunta | termina |
|---|---|---|
| True | True | True |
| True | False | True |
| False | True | False |
| False | False | True |

### 9.2 Detección De Contradicciones

Una opción puede activar una contradicción.

Ejemplo en:

```text
backend/app/utils/seed_data.py
```

```python
{
    "text": "Dice que sí, pero justifica ocultar cosas para evitar problemas",
    "activates_contradiction": True,
    "contradiction_code": "honestidad_justifica_mentir",
    "contradiction_penalty": -7,
}
```

La evaluación está en:

```text
backend/app/services/session_service.py
```

Código:

```python
if answer.option.activates_contradiction:
    contradictions.append(answer.option.contradiction_code)
    raw_scores[Dimension.confianza] += answer.option.contradiction_penalty
```

Esto significa:

```text
si contradiccion == True:
    registrar contradiccion
    aplicar penalizacion adicional
```

Ejemplos de contradicciones:

- Dice que es honesto, pero justifica mentir.
- Dice que respeta límites, pero revisaría el teléfono.
- Dice que tiene interés real, pero solo aparece cuando le conviene.
- Dice que comunica bien, pero evita hablar de problemas.
- Dice que no es celoso, pero controla salidas o amistades.
- Dice que busca algo serio, pero evita definir intenciones.
- Dice que se preocupa, pero invalida emociones.

## 10. Ejemplo Matemático Simplificado

Supongamos que una persona responde tres opciones:

```text
R1 = comunicacion +5, interes_real +3
R2 = honestidad +5, confianza +4
R3 = respeto +6, limites_personales +6
```

Suma bruta:

```text
comunicacion = 5
interes_real = 3
honestidad = 5
confianza = 4
respeto = 6
limites_personales = 6
```

Luego cada dimensión se normaliza a `0 - 100`.

Después se aplica:

```text
F = Σ(di_normalizada * peso_i)
```

Si `F >= 70`, el resultado es:

```text
Green Flag
```

## 11. Cómo Explicarlo Oralmente

Una forma clara de explicarlo:

> El test funciona como un grafo dirigido. Cada pregunta es un nodo y cada respuesta es una arista que puede llevar a otra pregunta. Cada respuesta modifica un vector de dimensiones relacionales, sumando o restando puntos. Luego esos puntajes se normalizan a una escala de 0 a 100, se ponderan según la importancia de cada dimensión y finalmente se clasifican mediante umbrales en Green Flag, Zona Gris o Red Flag. Además, el sistema usa lógica booleana para decidir cuándo termina el recorrido y para detectar contradicciones graves que penalizan la confianza.

Versión más corta:

> El modelo combina teoría de grafos, suma vectorial, ponderación y lógica booleana. El grafo decide el camino del test, la suma acumula señales por dimensión, la ponderación calcula el puntaje final y los booleanos detectan finales o contradicciones.

## 12. Archivos Clave

```text
backend/app/utils/seed_data.py
```

Define el banco de preguntas, opciones, efectos, contradicciones y conexiones del grafo.

```text
backend/app/models/option.py
```

Define `OptionNextQuestion`, que representa las aristas del grafo en base de datos.

```text
backend/app/services/seed_service.py
```

Carga el grafo en la base de datos.

```text
backend/app/services/session_service.py
```

Recorre el grafo, suma puntajes, detecta contradicciones y calcula resultados.

```text
backend/app/core/scoring.py
```

Contiene pesos, normalización, cálculo ponderado y clasificación final.

```text
backend/app/core/config.py
```

Define el rango de normalización.

```text
backend/app/core/enums.py
```

Define las dimensiones y los resultados posibles.

