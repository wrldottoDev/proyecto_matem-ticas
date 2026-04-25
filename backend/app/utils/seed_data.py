from app.core.enums import Dimension

D = Dimension


# Banco principal del test.
#
# Cada item es un nodo del grafo dirigido:
# - key: identificador estable del nodo.
# - main_dimension: dimension principal que explora la pregunta.
# - options[].effects: pesos por dimension. Positivo suma senales sanas; negativo resta.
# - options[].next: key del siguiente nodo. Si no existe y la pregunta es terminal, termina.
# - options[].activates_contradiction: marca una inconsistencia booleana relevante.
# - options[].contradiction_penalty: penalizacion adicional aplicada a confianza.
#
# Para agregar preguntas nuevas:
# 1. Crear un nodo con key unica.
# 2. Definir opciones con effects entre -10 y +6.
# 3. Conectar cada opcion con next si debe continuar el recorrido.
# 4. Marcar is_terminal=True solo para nodos finales.
SEED_QUESTIONS = [
    {
        "key": "rel_inicio",
        "text": "¿Cómo describirías la comunicación cotidiana con esa persona?",
        "main_dimension": D.comunicacion.value,
        "is_start": True,
        "options": [
            {
                "text": "Es constante, clara y no me deja adivinando",
                "effects": {
                    D.comunicacion.value: 5,
                    D.interes_real.value: 3,
                    D.disponibilidad_emocional.value: 2,
                },
                "next": "honestidad_base",
            },
            {
                "text": "A veces fluye, pero también desaparece o responde cuando quiere",
                "effects": {
                    D.comunicacion.value: -2,
                    D.interes_real.value: -2,
                    D.coherencia.value: -1,
                },
                "next": "ghosting_patron",
            },
            {
                "text": "Casi siempre tengo que perseguir la conversación",
                "effects": {
                    D.comunicacion.value: -6,
                    D.interes_real.value: -5,
                    D.reciprocidad.value: -4,
                },
                "next": "interes_conveniencia",
            },
        ],
    },
    {
        "key": "honestidad_base",
        "text": "Cuando habla de lo que siente o quiere, ¿se percibe honestidad?",
        "main_dimension": D.honestidad.value,
        "options": [
            {
                "text": "Sí, suele ser directo incluso cuando el tema es incómodo",
                "effects": {
                    D.honestidad.value: 5,
                    D.confianza.value: 4,
                    D.responsabilidad_afectiva.value: 2,
                },
                "next": "coherencia_palabras_acciones",
            },
            {
                "text": "Dice que sí, pero justifica ocultar cosas para evitar problemas",
                "effects": {
                    D.honestidad.value: -5,
                    D.confianza.value: -4,
                    D.coherencia.value: -3,
                },
                "activates_contradiction": True,
                "contradiction_code": "honestidad_justifica_mentir",
                "contradiction_penalty": -7,
                "next": "confianza_transparencia",
            },
            {
                "text": "Evita responder o cambia versiones con facilidad",
                "effects": {
                    D.honestidad.value: -7,
                    D.confianza.value: -6,
                    D.coherencia.value: -5,
                },
                "next": "confianza_transparencia",
            },
        ],
    },
    {
        "key": "ghosting_patron",
        "text": "Cuando desaparece, ¿qué pasa después?",
        "main_dimension": D.interes_real.value,
        "options": [
            {
                "text": "Explica, repara y procura que no sea un patrón",
                "effects": {
                    D.comunicacion.value: 2,
                    D.responsabilidad_afectiva.value: 3,
                    D.interes_real.value: 2,
                },
                "next": "conversaciones_dificiles",
            },
            {
                "text": "Vuelve como si nada y espera que yo lo normalice",
                "effects": {
                    D.comunicacion.value: -4,
                    D.responsabilidad_afectiva.value: -5,
                    D.interes_real.value: -5,
                },
                "next": "interes_conveniencia",
            },
            {
                "text": "Solo aparece cuando necesita atención, favores o validación",
                "effects": {
                    D.interes_real.value: -7,
                    D.reciprocidad.value: -6,
                    D.responsabilidad_afectiva.value: -5,
                },
                "activates_contradiction": True,
                "contradiction_code": "interes_real_aparece_por_conveniencia",
                "contradiction_penalty": -6,
                "next": "interes_conveniencia",
            },
        ],
    },
    {
        "key": "interes_conveniencia",
        "text": "¿El interés que muestra se sostiene cuando no obtiene algo inmediato de ti?",
        "main_dimension": D.reciprocidad.value,
        "options": [
            {
                "text": "Sí, pregunta, escucha y también está en días normales",
                "effects": {
                    D.interes_real.value: 5,
                    D.reciprocidad.value: 5,
                    D.empatia.value: 2,
                },
                "next": "responsabilidad_afectiva_base",
            },
            {
                "text": "Depende; a veces parece genuino y a veces utilitario",
                "effects": {
                    D.interes_real.value: -1,
                    D.reciprocidad.value: -2,
                    D.coherencia.value: -1,
                },
                "next": "reciprocidad_esfuerzo",
            },
            {
                "text": "No, el patrón es aparecer cuando le conviene",
                "effects": {
                    D.interes_real.value: -8,
                    D.reciprocidad.value: -7,
                    D.responsabilidad_afectiva.value: -4,
                },
                "next": "limites_base",
            },
        ],
    },
    {
        "key": "coherencia_palabras_acciones",
        "text": "¿Sus acciones coinciden con lo que dice que quiere contigo?",
        "main_dimension": D.coherencia.value,
        "options": [
            {
                "text": "Sí, hay consistencia entre palabras, tiempo y acciones",
                "effects": {
                    D.coherencia.value: 6,
                    D.confianza.value: 4,
                    D.compromiso.value: 3,
                },
                "next": "intenciones_claras",
            },
            {
                "text": "Tiene buenas palabras, pero sus acciones son irregulares",
                "effects": {
                    D.coherencia.value: -4,
                    D.confianza.value: -3,
                    D.compromiso.value: -2,
                },
                "next": "intenciones_claras",
            },
            {
                "text": "Dice una cosa y hace otra con frecuencia",
                "effects": {
                    D.coherencia.value: -8,
                    D.confianza.value: -6,
                    D.honestidad.value: -4,
                },
                "next": "confianza_transparencia",
            },
        ],
    },
    {
        "key": "intenciones_claras",
        "text": "¿Hay claridad sobre lo que busca: algo serio, casual o indefinido?",
        "main_dimension": D.compromiso.value,
        "options": [
            {
                "text": "Sí, lo expresa sin presionar ni prometer de más",
                "effects": {
                    D.comunicacion.value: 4,
                    D.compromiso.value: 4,
                    D.honestidad.value: 3,
                },
                "next": "limites_base",
            },
            {
                "text": "Dice que quiere algo serio, pero evita definir intenciones",
                "effects": {
                    D.compromiso.value: -5,
                    D.coherencia.value: -5,
                    D.honestidad.value: -3,
                },
                "activates_contradiction": True,
                "contradiction_code": "compromiso_evita_definir",
                "contradiction_penalty": -6,
                "next": "coherencia_presion",
            },
            {
                "text": "Prefiere mantener todo ambiguo",
                "effects": {
                    D.comunicacion.value: -3,
                    D.compromiso.value: -5,
                    D.responsabilidad_afectiva.value: -3,
                },
                "next": "conversaciones_dificiles",
            },
        ],
    },
    {
        "key": "confianza_transparencia",
        "text": "¿Puedes confiar en que te cuenta lo importante sin manipular la información?",
        "main_dimension": D.confianza.value,
        "options": [
            {
                "text": "Sí, hay transparencia y apertura razonable",
                "effects": {
                    D.confianza.value: 5,
                    D.honestidad.value: 4,
                    D.coherencia.value: 2,
                },
                "next": "limites_base",
            },
            {
                "text": "No estoy seguro; hay vacíos que luego explica a medias",
                "effects": {
                    D.confianza.value: -3,
                    D.honestidad.value: -3,
                    D.coherencia.value: -2,
                },
                "next": "conversaciones_dificiles",
            },
            {
                "text": "No, suele omitir, negar o torcer los hechos",
                "effects": {
                    D.confianza.value: -8,
                    D.honestidad.value: -8,
                    D.manipulacion.value: -5,
                },
                "next": "manipulacion_emocional",
            },
        ],
    },
    {
        "key": "limites_base",
        "text": "¿Cómo reacciona cuando dices que no o pides espacio?",
        "main_dimension": D.limites_personales.value,
        "options": [
            {
                "text": "Respeta el límite sin castigarme ni presionarme",
                "effects": {
                    D.respeto.value: 6,
                    D.limites_personales.value: 6,
                    D.responsabilidad_afectiva.value: 3,
                },
                "next": "celos_control_base",
            },
            {
                "text": "A veces insiste, negocia o minimiza el límite",
                "effects": {
                    D.respeto.value: -4,
                    D.limites_personales.value: -5,
                    D.responsabilidad_afectiva.value: -3,
                },
                "next": "telefono_privacidad",
            },
            {
                "text": "Se molesta, castiga con silencio o me hace sentir culpable",
                "effects": {
                    D.respeto.value: -7,
                    D.limites_personales.value: -8,
                    D.manipulacion.value: -6,
                },
                "next": "manipulacion_emocional",
            },
        ],
    },
    {
        "key": "telefono_privacidad",
        "text": "Si tuviera inseguridad, ¿revisaría tu teléfono o tus redes?",
        "main_dimension": D.celos_control.value,
        "options": [
            {
                "text": "No, entiende que la confianza no se construye invadiendo privacidad",
                "effects": {
                    D.confianza.value: 4,
                    D.respeto.value: 5,
                    D.limites_personales.value: 5,
                    D.celos_control.value: 4,
                },
                "next": "celos_control_base",
            },
            {
                "text": "Tal vez lo justificaría si se siente inseguro",
                "effects": {
                    D.confianza.value: -4,
                    D.respeto.value: -5,
                    D.limites_personales.value: -6,
                    D.celos_control.value: -6,
                },
                "activates_contradiction": True,
                "contradiction_code": "respeta_limites_pero_invade_privacidad",
                "contradiction_penalty": -8,
                "next": "celos_control_base",
            },
            {
                "text": "Sí, cree que revisar es prueba de amor o transparencia",
                "effects": {
                    D.confianza.value: -7,
                    D.respeto.value: -8,
                    D.limites_personales.value: -9,
                    D.celos_control.value: -9,
                },
                "activates_contradiction": True,
                "contradiction_code": "control_revisa_telefono",
                "contradiction_penalty": -9,
                "next": "manipulacion_emocional",
            },
        ],
    },
    {
        "key": "celos_control_base",
        "text": "¿Cómo maneja los celos o la inseguridad?",
        "main_dimension": D.celos_control.value,
        "options": [
            {
                "text": "Los conversa sin controlar mis amistades, ropa o salidas",
                "effects": {
                    D.celos_control.value: 5,
                    D.comunicacion.value: 3,
                    D.respeto.value: 4,
                },
                "next": "conversaciones_dificiles",
            },
            {
                "text": "Dice que no es celoso, pero opina sobre con quién puedo salir",
                "effects": {
                    D.celos_control.value: -6,
                    D.respeto.value: -5,
                    D.limites_personales.value: -4,
                },
                "activates_contradiction": True,
                "contradiction_code": "no_celoso_pero_controla_salidas",
                "contradiction_penalty": -7,
                "next": "manipulacion_emocional",
            },
            {
                "text": "Controla, acusa o pide pruebas constantes",
                "effects": {
                    D.celos_control.value: -10,
                    D.respeto.value: -8,
                    D.confianza.value: -7,
                    D.manipulacion.value: -6,
                },
                "next": "alerta_fuerte",
            },
        ],
    },
    {
        "key": "conversaciones_dificiles",
        "text": "Cuando hay un tema difícil, ¿pueden hablarlo?",
        "main_dimension": D.resolucion_conflictos.value,
        "options": [
            {
                "text": "Sí, escucha, pregunta y busca acuerdos concretos",
                "effects": {
                    D.comunicacion.value: 4,
                    D.resolucion_conflictos.value: 6,
                    D.empatia.value: 4,
                },
                "next": "responsabilidad_afectiva_base",
            },
            {
                "text": "A veces, pero suele aplazar conversaciones importantes",
                "effects": {
                    D.comunicacion.value: -2,
                    D.resolucion_conflictos.value: -3,
                    D.disponibilidad_emocional.value: -2,
                },
                "next": "evasiones_importantes",
            },
            {
                "text": "Evita, se cierra, desaparece o cambia el tema",
                "effects": {
                    D.comunicacion.value: -6,
                    D.resolucion_conflictos.value: -7,
                    D.responsabilidad_afectiva.value: -5,
                },
                "activates_contradiction": True,
                "contradiction_code": "dice_comunicar_bien_pero_evita_problemas",
                "contradiction_penalty": -6,
                "next": "evasiones_importantes",
            },
        ],
    },
    {
        "key": "evasiones_importantes",
        "text": "Si pides claridad sobre algo importante, ¿qué respuesta recibes?",
        "main_dimension": D.comunicacion.value,
        "options": [
            {
                "text": "Responde con honestidad aunque necesite tiempo para ordenar ideas",
                "effects": {
                    D.comunicacion.value: 3,
                    D.honestidad.value: 3,
                    D.disponibilidad_emocional.value: 2,
                },
                "next": "responsabilidad_afectiva_base",
            },
            {
                "text": "Da respuestas vagas y deja todo igual",
                "effects": {
                    D.comunicacion.value: -3,
                    D.honestidad.value: -2,
                    D.coherencia.value: -2,
                },
                "next": "reciprocidad_esfuerzo",
            },
            {
                "text": "Me hace sentir intenso o culpable por preguntar",
                "effects": {
                    D.manipulacion.value: -7,
                    D.empatia.value: -5,
                    D.respeto.value: -5,
                },
                "next": "manipulacion_emocional",
            },
        ],
    },
    {
        "key": "responsabilidad_afectiva_base",
        "text": "¿Se hace cargo del impacto emocional de sus acciones?",
        "main_dimension": D.responsabilidad_afectiva.value,
        "options": [
            {
                "text": "Sí, reconoce errores, repara y cambia conductas",
                "effects": {
                    D.responsabilidad_afectiva.value: 6,
                    D.empatia.value: 4,
                    D.coherencia.value: 3,
                },
                "next": "reciprocidad_esfuerzo",
            },
            {
                "text": "Pide perdón, pero repite el mismo patrón",
                "effects": {
                    D.responsabilidad_afectiva.value: -4,
                    D.coherencia.value: -4,
                    D.confianza.value: -3,
                },
                "next": "coherencia_presion",
            },
            {
                "text": "Niega el daño o dice que exagero",
                "effects": {
                    D.responsabilidad_afectiva.value: -8,
                    D.empatia.value: -7,
                    D.manipulacion.value: -6,
                },
                "activates_contradiction": True,
                "contradiction_code": "dice_preocuparse_pero_invalida_emociones",
                "contradiction_penalty": -8,
                "next": "manipulacion_emocional",
            },
        ],
    },
    {
        "key": "reciprocidad_esfuerzo",
        "text": "¿El esfuerzo por sostener el vínculo es recíproco?",
        "main_dimension": D.reciprocidad.value,
        "options": [
            {
                "text": "Sí, ambos cuidan el vínculo con acciones concretas",
                "effects": {
                    D.reciprocidad.value: 6,
                    D.interes_real.value: 4,
                    D.compromiso.value: 3,
                },
                "next": "disponibilidad_emocional",
            },
            {
                "text": "Hay intención, pero el esfuerzo todavía es desigual",
                "effects": {
                    D.reciprocidad.value: -1,
                    D.interes_real.value: -1,
                    D.compromiso.value: -1,
                },
                "next": "madurez_emocional",
            },
            {
                "text": "Yo sostengo casi todo y la otra persona recibe",
                "effects": {
                    D.reciprocidad.value: -7,
                    D.interes_real.value: -5,
                    D.responsabilidad_afectiva.value: -4,
                },
                "next": "dependencia_emocional",
            },
        ],
    },
    {
        "key": "disponibilidad_emocional",
        "text": "¿Está emocionalmente disponible para construir algo sano?",
        "main_dimension": D.disponibilidad_emocional.value,
        "options": [
            {
                "text": "Sí, puede vincularse sin huir ni absorberme",
                "effects": {
                    D.disponibilidad_emocional.value: 6,
                    D.compromiso.value: 3,
                    D.responsabilidad_afectiva.value: 3,
                },
                "next": "empatia_validacion",
            },
            {
                "text": "Quiere, pero se bloquea o se aleja cuando hay profundidad",
                "effects": {
                    D.disponibilidad_emocional.value: -3,
                    D.compromiso.value: -2,
                    D.resolucion_conflictos.value: -2,
                },
                "next": "madurez_emocional",
            },
            {
                "text": "No, evita intimidad emocional o depende de mí para regularse",
                "effects": {
                    D.disponibilidad_emocional.value: -7,
                    D.responsabilidad_afectiva.value: -5,
                    D.limites_personales.value: -4,
                },
                "next": "dependencia_emocional",
            },
        ],
    },
    {
        "key": "empatia_validacion",
        "text": "Cuando expresas una emoción, ¿la valida aunque no piense igual?",
        "main_dimension": D.empatia.value,
        "options": [
            {
                "text": "Sí, intenta comprender antes de defenderse",
                "effects": {
                    D.empatia.value: 6,
                    D.resolucion_conflictos.value: 4,
                    D.respeto.value: 3,
                },
                "next": "compromiso_acciones",
            },
            {
                "text": "A veces valida, pero se pone defensivo con facilidad",
                "effects": {
                    D.empatia.value: -2,
                    D.resolucion_conflictos.value: -2,
                    D.comunicacion.value: -1,
                },
                "next": "madurez_emocional",
            },
            {
                "text": "Invalida, ridiculiza o usa mis emociones en mi contra",
                "effects": {
                    D.empatia.value: -8,
                    D.respeto.value: -7,
                    D.manipulacion.value: -7,
                },
                "next": "alerta_fuerte",
            },
        ],
    },
    {
        "key": "compromiso_acciones",
        "text": "¿El compromiso se ve en acciones sostenidas y no solo en promesas?",
        "main_dimension": D.compromiso.value,
        "options": [
            {
                "text": "Sí, hay presencia, acuerdos y seguimiento",
                "effects": {
                    D.compromiso.value: 6,
                    D.coherencia.value: 5,
                    D.confianza.value: 4,
                },
                "next": "confirmacion_green",
            },
            {
                "text": "Hay señales buenas, pero todavía falta consistencia",
                "effects": {
                    D.compromiso.value: 1,
                    D.coherencia.value: -1,
                    D.confianza.value: 0,
                },
                "next": "confirmacion_zona_gris",
            },
            {
                "text": "Promete mucho y concreta poco",
                "effects": {
                    D.compromiso.value: -5,
                    D.coherencia.value: -6,
                    D.confianza.value: -4,
                },
                "next": "coherencia_presion",
            },
        ],
    },
    {
        "key": "madurez_emocional",
        "text": "¿Notas madurez emocional cuando algo no sale como espera?",
        "main_dimension": D.disponibilidad_emocional.value,
        "options": [
            {
                "text": "Sí, puede frustrarse sin atacar, huir ni castigar",
                "effects": {
                    D.disponibilidad_emocional.value: 4,
                    D.empatia.value: 3,
                    D.resolucion_conflictos.value: 3,
                },
                "next": "confirmacion_zona_gris",
            },
            {
                "text": "A veces reacciona bien, pero otras se cierra o explota",
                "effects": {
                    D.disponibilidad_emocional.value: -2,
                    D.resolucion_conflictos.value: -3,
                    D.responsabilidad_afectiva.value: -2,
                },
                "next": "confirmacion_zona_gris",
            },
            {
                "text": "Reacciona con berrinche, culpa, silencio o amenaza de irse",
                "effects": {
                    D.disponibilidad_emocional.value: -7,
                    D.manipulacion.value: -6,
                    D.responsabilidad_afectiva.value: -6,
                },
                "next": "alerta_fuerte",
            },
        ],
    },
    {
        "key": "dependencia_emocional",
        "text": "¿Hay señales de dependencia emocional o necesidad de control constante?",
        "main_dimension": D.limites_personales.value,
        "options": [
            {
                "text": "No, hay cercanía sin perder autonomía",
                "effects": {
                    D.limites_personales.value: 4,
                    D.disponibilidad_emocional.value: 4,
                    D.confianza.value: 3,
                },
                "next": "confirmacion_zona_gris",
            },
            {
                "text": "A veces necesita demasiada validación o presencia",
                "effects": {
                    D.limites_personales.value: -3,
                    D.disponibilidad_emocional.value: -3,
                    D.celos_control.value: -2,
                },
                "next": "madurez_emocional",
            },
            {
                "text": "Sí, se angustia, controla o me responsabiliza por su estabilidad",
                "effects": {
                    D.limites_personales.value: -7,
                    D.celos_control.value: -7,
                    D.manipulacion.value: -6,
                },
                "next": "alerta_fuerte",
            },
        ],
    },
    {
        "key": "coherencia_presion",
        "text": "Cuando se le señala una incoherencia, ¿qué hace?",
        "main_dimension": D.coherencia.value,
        "options": [
            {
                "text": "La reconoce y ajusta su conducta",
                "effects": {
                    D.coherencia.value: 4,
                    D.responsabilidad_afectiva.value: 4,
                    D.confianza.value: 2,
                },
                "next": "confirmacion_zona_gris",
            },
            {
                "text": "Promete cambiar, pero intenta pasar rápido la página",
                "effects": {
                    D.coherencia.value: -3,
                    D.responsabilidad_afectiva.value: -3,
                    D.confianza.value: -2,
                },
                "next": "madurez_emocional",
            },
            {
                "text": "Me acusa de desconfiado o convierte el problema en culpa mía",
                "effects": {
                    D.coherencia.value: -6,
                    D.manipulacion.value: -7,
                    D.confianza.value: -6,
                },
                "next": "manipulacion_emocional",
            },
        ],
    },
    {
        "key": "manipulacion_emocional",
        "text": "¿Usa culpa, silencio, victimización o gaslighting para obtener lo que quiere?",
        "main_dimension": D.manipulacion.value,
        "options": [
            {
                "text": "No, puede hablar sin manipular ni castigar",
                "effects": {
                    D.manipulacion.value: 5,
                    D.respeto.value: 4,
                    D.confianza.value: 3,
                },
                "next": "confirmacion_zona_gris",
            },
            {
                "text": "A veces usa culpa o silencio, aunque luego lo reconoce",
                "effects": {
                    D.manipulacion.value: -5,
                    D.responsabilidad_afectiva.value: -3,
                    D.confianza.value: -4,
                },
                "next": "alerta_fuerte",
            },
            {
                "text": "Sí, suele distorsionar los hechos o hacerme dudar de mí",
                "effects": {
                    D.manipulacion.value: -10,
                    D.confianza.value: -8,
                    D.respeto.value: -7,
                    D.empatia.value: -6,
                },
                "next": "alerta_fuerte",
            },
        ],
    },
    {
        "key": "alerta_fuerte",
        "text": "¿Hay una señal fuerte de alerta que se repite o escala?",
        "main_dimension": D.respeto.value,
        "options": [
            {
                "text": "No escala y hay disposición real a corregir",
                "effects": {
                    D.responsabilidad_afectiva.value: 2,
                    D.resolucion_conflictos.value: 2,
                    D.confianza.value: 1,
                },
                "next": "confirmacion_zona_gris",
            },
            {
                "text": "Sí, hay control, mentira, invasión de límites o invalidación frecuente",
                "effects": {
                    D.respeto.value: -10,
                    D.confianza.value: -9,
                    D.limites_personales.value: -9,
                    D.manipulacion.value: -8,
                },
                "next": "terminal_red",
            },
            {
                "text": "No sé, pero me siento drenado o en alerta constante",
                "effects": {
                    D.confianza.value: -5,
                    D.disponibilidad_emocional.value: -5,
                    D.responsabilidad_afectiva.value: -4,
                },
                "next": "terminal_red",
            },
        ],
    },
    {
        "key": "confirmacion_green",
        "text": "Mirando el conjunto, ¿el vínculo te da tranquilidad, claridad y libertad?",
        "main_dimension": D.confianza.value,
        "is_terminal": True,
        "options": [
            {
                "text": "Sí, se siente sano, recíproco y estable",
                "effects": {
                    D.confianza.value: 6,
                    D.respeto.value: 5,
                    D.reciprocidad.value: 5,
                    D.disponibilidad_emocional.value: 4,
                },
            },
            {
                "text": "Casi siempre, aunque hay cosas puntuales por hablar",
                "effects": {
                    D.confianza.value: 2,
                    D.comunicacion.value: 2,
                    D.resolucion_conflictos.value: 1,
                },
            },
        ],
    },
    {
        "key": "confirmacion_zona_gris",
        "text": "¿El patrón general se siente reparable con conversación y cambios concretos?",
        "main_dimension": D.resolucion_conflictos.value,
        "is_terminal": True,
        "options": [
            {
                "text": "Sí, hay temas pendientes pero también voluntad real",
                "effects": {
                    D.resolucion_conflictos.value: 3,
                    D.responsabilidad_afectiva.value: 3,
                    D.confianza.value: 2,
                },
            },
            {
                "text": "No estoy seguro; hay señales mixtas",
                "effects": {
                    D.confianza.value: -2,
                    D.coherencia.value: -2,
                    D.disponibilidad_emocional.value: -2,
                },
            },
            {
                "text": "No, siento que el costo emocional supera lo positivo",
                "effects": {
                    D.confianza.value: -5,
                    D.responsabilidad_afectiva.value: -4,
                    D.reciprocidad.value: -4,
                },
            },
        ],
    },
    {
        "key": "terminal_red",
        "text": "Con esas señales presentes, ¿la relación mantiene respeto, seguridad y autonomía?",
        "main_dimension": D.respeto.value,
        "is_terminal": True,
        "options": [
            {
                "text": "No, hay un patrón que compromete mi bienestar",
                "effects": {
                    D.respeto.value: -10,
                    D.limites_personales.value: -10,
                    D.confianza.value: -8,
                    D.manipulacion.value: -8,
                },
            },
            {
                "text": "Hay algo rescatable, pero necesito distancia y límites claros",
                "effects": {
                    D.respeto.value: -4,
                    D.limites_personales.value: -4,
                    D.confianza.value: -4,
                    D.resolucion_conflictos.value: -2,
                },
            },
        ],
    },
]
