# 📘 Proyecto de Matemáticas

## 👥 Integrantes

- Dylan Piña
- Emmanuel Villegas
- Grace Hernández
- Natasha Rodríguez
- Otoniel González

---

## 📖 Introducción

“¿Ahí es?” es una herramienta interactiva desarrollada para aplicar conceptos de lógica booleana y reglas de decisión en la evaluación de comportamientos dentro de un contexto relacional. El programa utiliza un cuestionario dinámico que analiza respuestas del usuario y asigna puntajes mediante operadores lógicos, permitiendo determinar si una persona representa una Green Flag o una Red Flag. El objetivo es ofrecer una evaluación estructurada basada en criterios lógicos para apoyar la toma de decisiones.

---

## 🎯 Objetivo del Programa

Desarrollar una herramienta interactiva programada que, mediante el uso de lógica booleana y reglas de decisión, evalúe comportamientos y actitudes de una persona para determinar si representa una Green Flag o Red Flag, asignando puntajes y generando un veredicto final basado en las respuestas del usuario.

---

## ⚙️ Funcionalidades

- Cuestionario interactivo dinámico
- Evaluación de respuestas mediante lógica booleana
- Sistema de puntaje con Green Flags y Red Flags
- Detección de contradicciones entre respuestas
- Cálculo automático de porcentaje de viabilidad
- Clasificación final (Green Flag / Red Flag)
- Preguntas adaptativas según respuestas del usuario
- Almacenamiento de preguntas y respuestas en base de datos
- Evaluación lógica con operadores AND, OR y NOT
- Resultado final claro e interactivo

---

## 🧰 Tecnologías

### Backend

- Python
- FastAPI / Django (API lógica del sistema)
- PostgreSQL (Base de datos)
- SQLAlchemy / ORM

### Frontend

- Next.js
- React
- Tailwind CSS

### Base de datos

- PostgreSQL
- Sistema de preguntas por ID
- Respuestas con ponderación

### Lógica del sistema

- Lógica booleana
- Sistema de ponderación
- Evaluación condicional
- Algoritmo de puntuación

---

## 🏗️ Arquitectura

Frontend (NextJS) → API (Python) → PostgreSQL  
 ← Resultado lógico ←

---

## 🧠 Funcionamiento

El sistema presenta un cuestionario interactivo donde cada respuesta se convierte en una variable lógica.  
El backend procesa estas respuestas utilizando operadores booleanos y un sistema de ponderación, generando un puntaje final que clasifica al usuario como Green Flag o Red Flag.
