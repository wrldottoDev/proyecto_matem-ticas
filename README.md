# ¿Ahí es?

Aplicación full stack para evaluar si una persona o situación cae en `Green Flag`, `Zona Gris` o `Red Flag` mediante un cuestionario dinámico con flujo condicional y un modelo matemático ponderado.

## Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, python-dotenv
- Frontend: Next.js App Router, TypeScript, Tailwind CSS
- Infraestructura local: Docker Compose

## Estructura

```text
.
├── backend
│   ├── alembic
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   └── utils
│   ├── scripts
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── app
│   ├── components
│   ├── lib
│   ├── .env.example
│   └── Dockerfile
└── docker-compose.yml
```

## Modelo matemático

Dimensiones:

- `comunicacion`
- `respeto`
- `coherencia`
- `responsabilidad_afectiva`
- `interes_real`
- `honestidad`
- `confianza`
- `limites_personales`
- `manipulacion`
- `celos_control`
- `disponibilidad_emocional`
- `compromiso`
- `empatia`
- `resolucion_conflictos`
- `reciprocidad`

Pesos:

- `comunicacion = 0.07`
- `respeto = 0.08`
- `coherencia = 0.07`
- `responsabilidad_afectiva = 0.08`
- `interes_real = 0.06`
- `honestidad = 0.07`
- `confianza = 0.08`
- `limites_personales = 0.07`
- `manipulacion = 0.08`
- `celos_control = 0.06`
- `disponibilidad_emocional = 0.06`
- `compromiso = 0.06`
- `empatia = 0.06`
- `resolucion_conflictos = 0.05`
- `reciprocidad = 0.05`

Fórmula:

```text
F = suma(dimension_normalizada * peso_dimension)
```

Clasificación:

- `70 - 100`: Green Flag
- `40 - 69.99`: Zona Gris
- `0 - 39.99`: Red Flag

La normalización se centraliza en [backend/app/core/config.py](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/app/core/config.py) mediante `DIMENSION_MIN_SCORE` y `DIMENSION_MAX_SCORE`, para que el rango sea fácil de ajustar.

Las opciones usan efectos proporcionales:

- Green flags fuertes: `+4` a `+6`
- Green flags moderadas: `+2` a `+3`
- Neutras o dudosas: `0` a `-1`
- Red flags moderadas: `-3` a `-5`
- Red flags fuertes: `-6` a `-10`
- Contradicciones graves: penalización adicional de `-5` a `-10` aplicada a `confianza`

## Grafo del cuestionario

El test funciona como un grafo dirigido:

- Cada pregunta es un nodo con `key`, `text`, `main_dimension` e indicadores `is_start` / `is_terminal`.
- Cada opción es una arista potencial: suma/resta efectos y puede apuntar a otra pregunta mediante `next`.
- El enlace persistido en base de datos está en `option_next_questions`.
- Si la pregunta es terminal o la opción no tiene siguiente pregunta, la sesión termina.

Relaciones conceptuales implementadas:

- Honestidad -> Confianza
- Comunicación -> Resolución de conflictos
- Respeto -> Límites personales
- Manipulación -> Confianza negativa
- Celos/control -> Respeto negativo
- Ghosting -> Interés real negativo
- Responsabilidad afectiva -> Estabilidad del vínculo
- Coherencia -> Confianza
- Evasión -> Comunicación negativa
- Reciprocidad -> Interés real
- Empatía -> Resolución de conflictos

El grafo profundiza según las respuestas. Por ejemplo:

- Falta de comunicación -> ghosting -> interés real -> responsabilidad afectiva
- Honestidad dudosa -> confianza -> manipulación
- Celos/control -> privacidad/límites -> manipulación o alerta fuerte
- Respuestas positivas consistentes -> confirmación Green Flag
- Respuestas mixtas -> confirmación Zona Gris
- Alertas fuertes -> terminal Red Flag

La detección de contradicciones vive en los metadatos de opción: `activates_contradiction`, `contradiction_code` y `contradiction_penalty`. El cálculo está en [backend/app/services/session_service.py](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/app/services/session_service.py).

## Backend

### Funcionalidades implementadas

- CRUD básico de preguntas y opciones
- Asignación de efectos por dimensión a cada opción
- Asignación de siguiente pregunta por opción
- Detección de contradicciones declaradas por opción
- Inicio de sesiones de test
- Respuesta de preguntas con flujo condicional
- Finalización automática cuando una pregunta es terminal o la opción no tiene siguiente pregunta
- Cálculo de puntajes brutos, normalizados, score final y clasificación
- Seeds iniciales con preguntas reales de ejemplo

### Endpoints principales

- `GET /api/v1/health`
- `POST /api/v1/admin/questions`
- `GET /api/v1/admin/questions`
- `GET /api/v1/admin/questions/{question_id}`
- `POST /api/v1/admin/questions/{question_id}/options`
- `POST /api/v1/admin/options/{option_id}/effects`
- `POST /api/v1/admin/options/{option_id}/next-question`
- `POST /api/v1/test/sessions`
- `GET /api/v1/test/sessions/{session_id}/start`
- `POST /api/v1/test/sessions/{session_id}/answers`
- `GET /api/v1/test/sessions/{session_id}/result`

### Variables de entorno backend

Copiar [backend/.env.example](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/.env.example) a `backend/.env`.

```env
APP_NAME=API de ¿Ahí es?
API_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg2://ahi_es:ahi_es@localhost:5432/ahi_es
CORS_ORIGINS_RAW=http://localhost:3000
DIMENSION_MIN_SCORE=-20
DIMENSION_MAX_SCORE=20
```

### Ejecución local del backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

## Frontend

### Pantallas implementadas

- Home con explicación del sistema
- Vista de test que muestra una pregunta a la vez
- Vista de resultado con score final, clasificación y barras por dimensión

### Variables de entorno frontend

Copiar [frontend/.env.example](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/frontend/.env.example) a `frontend/.env.local`.

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Ejecución local del frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Base de datos y migraciones

La migración inicial ya está incluida en [backend/alembic/versions/20260404_0001_initial_schema.py](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/alembic/versions/20260404_0001_initial_schema.py).

Comandos útiles:

```bash
cd backend
alembic upgrade head
python scripts/seed.py
```

## Docker Compose

Para levantar PostgreSQL, backend y frontend juntos:

```bash
docker compose up --build
```

Servicios:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Documentación Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

El contenedor del backend ejecuta migraciones y seeds al iniciar.

## Banco de preguntas

Se carga un banco amplio de preguntas sobre:

- Comunicación constante y ghosting
- Honestidad, confianza y coherencia
- Respeto de límites y privacidad
- Responsabilidad afectiva
- Claridad de intenciones y compromiso
- Interés real y reciprocidad
- Manipulación emocional
- Celos/control
- Empatía y resolución de conflictos
- Dependencia e inmadurez emocional
- Señales sanas, zona gris y alertas fuertes

La definición está en [backend/app/utils/seed_data.py](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/app/utils/seed_data.py).

El seeder [backend/app/services/seed_service.py](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/app/services/seed_service.py) crea primero todos los nodos y después resuelve las aristas `next`, para permitir que una opción apunte a preguntas definidas más adelante.

## Pruebas

```bash
cd backend
pytest
```

Las pruebas básicas validan carga del grafo, una ruta Green Flag y una ruta con contradicción.

## Notas de diseño

- La lógica pesada está en servicios, no en los endpoints.
- Los pesos están centralizados y validados en [backend/app/core/scoring.py](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/app/core/scoring.py).
- Las validaciones clave del flujo viven en [backend/app/services/session_service.py](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/backend/app/services/session_service.py).
- El frontend consume la API real con `fetch` desde [frontend/lib/api.ts](/Users/ottogonzalez/Documents/mate1/proyecto/ahi_es/frontend/lib/api.ts).
