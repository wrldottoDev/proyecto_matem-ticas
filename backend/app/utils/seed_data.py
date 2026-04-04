from app.core.enums import Dimension


SEED_QUESTIONS = [
    {
        "key": "q1",
        "text": "¿Te responde con constancia y sin desaparecer por días?",
        "is_start": True,
        "options": [
            {
                "text": "Sí, mantiene el contacto de forma consistente",
                "effects": {
                    Dimension.comunicacion.value: 3,
                    Dimension.interes_real.value: 2,
                    Dimension.coherencia.value: 1,
                },
                "next": "q2",
            },
            {
                "text": "A veces sí, pero es irregular",
                "effects": {
                    Dimension.comunicacion.value: -1,
                    Dimension.coherencia.value: -1,
                },
                "next": "q3",
            },
            {
                "text": "No, aparece solo cuando le conviene",
                "effects": {
                    Dimension.comunicacion.value: -3,
                    Dimension.interes_real.value: -2,
                    Dimension.responsabilidad_afectiva.value: -2,
                },
                "next": "q4",
            },
        ],
    },
    {
        "key": "q2",
        "text": "¿Cumple lo que promete cuando quedan en algo?",
        "options": [
            {
                "text": "Sí, casi siempre cumple",
                "effects": {
                    Dimension.coherencia.value: 3,
                    Dimension.respeto.value: 2,
                },
                "next": "q5",
            },
            {
                "text": "Cumple a medias o pone excusas frecuentes",
                "effects": {
                    Dimension.coherencia.value: -1,
                    Dimension.responsabilidad_afectiva.value: -1,
                },
                "next": "q5",
            },
        ],
    },
    {
        "key": "q3",
        "text": "¿Es claro con sus intenciones contigo?",
        "options": [
            {
                "text": "Sí, habla claro y no juega con ambigüedades",
                "effects": {
                    Dimension.comunicacion.value: 2,
                    Dimension.responsabilidad_afectiva.value: 2,
                },
                "next": "q5",
            },
            {
                "text": "No mucho, evita definir lo que quiere",
                "effects": {
                    Dimension.comunicacion.value: -2,
                    Dimension.responsabilidad_afectiva.value: -2,
                    Dimension.coherencia.value: -1,
                },
                "next": "q4",
            },
        ],
    },
    {
        "key": "q4",
        "text": "¿Te busca solo cuando necesita algo de ti?",
        "options": [
            {
                "text": "Sí, casi siempre es por conveniencia",
                "effects": {
                    Dimension.interes_real.value: -3,
                    Dimension.respeto.value: -2,
                    Dimension.responsabilidad_afectiva.value: -2,
                },
                "next": "q6",
            },
            {
                "text": "No, también muestra interés genuino por tu vida",
                "effects": {
                    Dimension.interes_real.value: 2,
                    Dimension.respeto.value: 1,
                },
                "next": "q5",
            },
        ],
    },
    {
        "key": "q5",
        "text": "¿Respeta tus límites cuando dices que no o pides espacio?",
        "options": [
            {
                "text": "Sí, respeta tus límites sin presionarte",
                "effects": {
                    Dimension.respeto.value: 3,
                    Dimension.responsabilidad_afectiva.value: 2,
                },
                "next": "q7",
            },
            {
                "text": "A veces insiste o minimiza tus límites",
                "effects": {
                    Dimension.respeto.value: -2,
                    Dimension.responsabilidad_afectiva.value: -2,
                },
                "next": "q6",
            },
        ],
    },
    {
        "key": "q6",
        "text": "Cuando hay un problema, ¿cómo reacciona?",
        "options": [
            {
                "text": "Habla, escucha y busca resolverlo",
                "effects": {
                    Dimension.comunicacion.value: 2,
                    Dimension.responsabilidad_afectiva.value: 2,
                    Dimension.coherencia.value: 1,
                },
                "next": "q7",
            },
            {
                "text": "Se cierra, culpa o desaparece",
                "effects": {
                    Dimension.comunicacion.value: -3,
                    Dimension.responsabilidad_afectiva.value: -3,
                    Dimension.respeto.value: -1,
                },
            },
        ],
    },
    {
        "key": "q7",
        "text": "En general, ¿sus acciones coinciden con lo que dice?",
        "is_terminal": True,
        "options": [
            {
                "text": "Sí, hay coherencia clara entre palabras y acciones",
                "effects": {
                    Dimension.coherencia.value: 3,
                    Dimension.interes_real.value: 1,
                    Dimension.respeto.value: 1,
                },
            },
            {
                "text": "No, dice una cosa y hace otra",
                "effects": {
                    Dimension.coherencia.value: -3,
                    Dimension.respeto.value: -1,
                    Dimension.responsabilidad_afectiva.value: -2,
                },
            },
        ],
    },
]
