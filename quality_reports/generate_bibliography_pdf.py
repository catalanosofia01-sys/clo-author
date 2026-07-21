#!/usr/bin/env python3
"""Genera un PDF con la bibliografia anotada del TFM (referencias + justificacion)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable
)

OUT = "/home/user/clo-author/quality_reports/Bibliografia_TFM_marco_teorico.pdf"

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom", parent=styles["Title"], fontSize=18, leading=22,
    alignment=TA_CENTER, spaceAfter=6,
)
subtitle_style = ParagraphStyle(
    "SubtitleCustom", parent=styles["Normal"], fontSize=11, leading=15,
    alignment=TA_CENTER, textColor=colors.HexColor("#444444"), spaceAfter=4,
)
block_title_style = ParagraphStyle(
    "BlockTitle", parent=styles["Heading1"], fontSize=14, leading=17,
    textColor=colors.HexColor("#1f3a5f"), spaceBefore=18, spaceAfter=4,
)
block_desc_style = ParagraphStyle(
    "BlockDesc", parent=styles["Normal"], fontSize=9.5, leading=13,
    textColor=colors.HexColor("#555555"), spaceAfter=10, fontName="Helvetica-Oblique",
)
subsection_style = ParagraphStyle(
    "Subsection", parent=styles["Heading2"], fontSize=11.5, leading=14,
    textColor=colors.HexColor("#3a3a3a"), spaceBefore=10, spaceAfter=4,
)
cite_style = ParagraphStyle(
    "Cite", parent=styles["Normal"], fontSize=10.5, leading=14,
    textColor=colors.black, spaceBefore=8, spaceAfter=2, fontName="Helvetica-Bold",
)
why_style = ParagraphStyle(
    "Why", parent=styles["Normal"], fontSize=9.5, leading=13.5,
    alignment=TA_JUSTIFY, spaceAfter=6,
)
meta_style = ParagraphStyle(
    "Meta", parent=styles["Normal"], fontSize=8.5, leading=11,
    textColor=colors.HexColor("#777777"), spaceAfter=2, fontName="Helvetica-Oblique",
)

def prox_badge(n):
    colors_map = {5: "#1f6f43", 4: "#3a7d44", 3: "#a67c00", 2: "#a65200", 1: "#8c8c8c"}
    c = colors_map.get(n, "#555555")
    return f'<font color="{c}"><b>Proximidad {n}/5</b></font>'

def entry(cite, prox, why, unverified=None, note=None):
    story = []
    story.append(Paragraph(cite, cite_style))
    meta_bits = [prox_badge(prox)]
    if unverified:
        meta_bits.append('<font color="#b03030"><b>[UNVERIFICADO: %s]</b></font>' % unverified)
    story.append(Paragraph(" &nbsp;&nbsp;·&nbsp;&nbsp; ".join(meta_bits), meta_style))
    story.append(Paragraph(f"<b>Por qué leerlo:</b> {why}", why_style))
    if note:
        story.append(Paragraph(f"<b>Nota de verificación:</b> {note}", meta_style))
    return story

def block(title, desc, entries):
    story = [Paragraph(title, block_title_style)]
    if desc:
        story.append(Paragraph(desc, block_desc_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#cccccc"), spaceAfter=4))
    for e in entries:
        story.extend(entry(**e))
    return story

def subsection(title):
    return [Paragraph(title, subsection_style)]

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm, topMargin=2*cm, bottomMargin=2*cm,
    title="Bibliografía anotada — Marco teórico TFM",
    author="TFM — Didáctica de la Lengua Inglesa",
)

story = []

# --- Title page ---
story.append(Spacer(1, 3*cm))
story.append(Paragraph(
    "Bibliografía anotada del marco teórico", title_style))
story.append(Paragraph(
    "TFM: PPP -> Task-Supported Language Teaching (Ellis) + gamificación -> "
    "Aprendizaje Basado en Proyectos (entrevista periodística en roleplay)",
    subtitle_style))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(
    "4º ESO · Nivel A2 (MCER) · Currículo BOJA, Andalucía", subtitle_style))
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph(
    "34 referencias organizadas en 7 bloques temáticos, con puntuación de "
    "proximidad (1–5) y justificación de por qué cada una importa para este TFM. "
    "Las entradas marcadas [UNVERIFICADO] tienen algún dato bibliográfico "
    "(orden de autores, página o número exacto) pendiente de confirmar contra "
    "la ficha oficial antes de citarlas textualmente.",
    ParagraphStyle("Intro", parent=styles["Normal"], fontSize=10, leading=14,
                   alignment=TA_JUSTIFY, textColor=colors.HexColor("#333333"))
))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    "Generado a partir de quality_reports/lit_review_tfm_task_supported_gamification.md "
    "(búsqueda: agente librarian; revisión de calidad: librarian-critic, 92/100)",
    meta_style
))
story.append(PageBreak())

# --- Bloque 1 ---
story.extend(block(
    "Bloque 1 — Task-Based vs. Task-Supported Language Teaching (Ellis)",
    "La distinción TBLT/TSLT, el foco en la forma explícito previo a la tarea, y su "
    "aplicabilidad a niveles bajos (A1/A2) — el eje teórico central del TFM.",
    [
        dict(cite="Ellis, R. (2003). <i>Task-Based Language Learning and Teaching</i>. Oxford University Press.",
             prox=5,
             why="Obra fundacional que sienta la taxonomía de tareas y las condiciones psicolingüísticas "
                 "(foco en el significado, vacío de información, resultado comunicable) que definen una "
                 "\"tarea\" en SLA. Referencia de partida obligada para justificar por qué Who is Who, el "
                 "juego de decisiones y Black Stories cuentan como tareas y no como ejercicios."),
        dict(cite="Ellis, R. (2009). Task-based language teaching: Sorting out the misunderstandings. "
                   "<i>International Journal of Applied Linguistics</i>, 19(3), 221-246.",
             prox=5,
             why="Responde a críticas (Widdowson, Seedhouse, Sheen, Swan) aclarando que el enfoque por "
                 "tareas no es monolítico y que TSLT es una opción legítima dentro del espectro. Respuesta "
                 "directa a la pregunta del tribunal: \"¿por qué Task-Supported y no Task-Based puro?\". "
                 "Citar siempre junto a Swan (2005), Bloque 1b — son las dos caras del mismo debate."),
        dict(cite="Li, S., Ellis, R., &amp; Zhu, Y. (2016). Task-based versus task-supported language "
                   "instruction: An experimental study. <i>Annual Review of Applied Linguistics</i>, 36, 205-229.",
             prox=5,
             why="Estudio experimental con 150 estudiantes de secundaria EFL (China): TSLT con instrucción "
                 "explícita previa no es inferior a TBLT puro. Evidencia empírica directa para defender el "
                 "diseño PPP->TSLT en un contexto de secundaria comparable."),
        dict(cite="Ellis, R. (2020). Task-based language teaching for beginner-level young learners. "
                   "<i>Language Teaching for Young Learners</i>, 2(1), 4-27.",
             prox=5,
             why="Defiende el uso de tareas con apoyo estructural explícito (\"input-based tasks\") para "
                 "hacer viable el enfoque con alumnado de nivel bajo — respalda directamente la pertinencia "
                 "de TSLT en A2."),
        dict(cite="Ellis, R., Skehan, P., Li, S., Shintani, N., &amp; Lambert, C. (2020). "
                   "<i>Task-Based Language Teaching: Theory and Practice</i>. Cambridge University Press.",
             prox=4, unverified="orden exacto de autores",
             why="Manual de síntesis reciente (30 años de investigación TBLT/TSLT); fuente de autoridad "
                 "actualizada que complementa a Ellis (2003) y refuerza la actualidad bibliográfica exigida "
                 "por el tribunal."),
        dict(cite="Ellis, R., &amp; Shintani, N. (2014). <i>Exploring Language Pedagogy through Second "
                   "Language Acquisition Research</i>. Routledge.",
             prox=4,
             why="Tiende un puente entre investigación en SLA y práctica docente, con secciones sobre "
                 "secuenciación PPP y tareas — útil para justificar metodológicamente la progresión "
                 "PPP->TSLT->ABP."),
        dict(cite="Prabhu, N. S. (1987). <i>Second Language Pedagogy</i>. Oxford University Press.",
             prox=3,
             why="Fuente original de la tipología de \"vacíos\" (information-gap, reasoning-gap, "
                 "opinion-gap) que Ellis retoma después. Justifica por qué Who is Who (information-gap) y "
                 "el juego de decisiones (reasoning/opinion-gap) generan necesidad comunicativa real."),
    ]
))

# --- Bloque 1b ---
story.extend(block(
    "Bloque 1b — PPP (Presentation-Practice-Production): modelo de entrada estructurada y su crítica",
    "Cierra el hueco señalado por el librarian-critic: el PPP como modelo de entrada estructurada y su "
    "papel/crítica dentro de un enfoque comunicativo.",
    [
        dict(cite="Swan, M. (2005). Legislation by hypothesis: The case of task-based instruction. "
                   "<i>Applied Linguistics</i>, 26(3), 376-401.",
             prox=5,
             why="Crítica influyente al TBLT \"fuerte\": el noticing incidental durante la tarea no basta "
                 "para enseñar sistemáticamente lengua nueva. Es la objeción exacta que Ellis (2009) "
                 "responde; permite justificar ante el tribunal por qué la unidad arranca en PPP (entrada "
                 "explícita de pasado simple, preguntas indirectas, etc.) antes de pasar a TSLT. Citar "
                 "siempre junto a Ellis (2009), presentando el debate como una tensión resuelta "
                 "pragmáticamente por el diseño TSLT, no como un enfoque descartado.",
             note="Verificado de forma independiente contra Oxford Academic (DOI 10.1093/applin/ami013), "
                  "ERIC (EJ728163) y Semantic Scholar/ResearchGate — datos coinciden en las cuatro fuentes."),
    ]
))

# --- Bloque 2 ---
story.extend(block(
    "Bloque 2 — Aprendizaje Basado en Juegos (Game-Based Learning): efectos psicológicos",
    None, []
))
story.extend(subsection("2a. Filtro afectivo / ansiedad ante la L2"))
story.extend(entry(
    cite="Krashen, S. D. (1982). <i>Principles and Practice in Second Language Acquisition</i>. Pergamon Press.",
    prox=5,
    why="Fuente de la Affective Filter Hypothesis: ansiedad, baja motivación y falta de confianza elevan "
        "una barrera psicológica que impide la absorción de input comprensible. Base teórica indispensable "
        "para argumentar que los mini-juegos reducen el filtro afectivo y facilitan la producción oral."))
story.extend(entry(
    cite="Horwitz, E. K., Horwitz, M. B., &amp; Cope, J. (1986). Foreign Language Classroom Anxiety. "
         "<i>The Modern Language Journal</i>, 70(2), 125-132.",
    prox=5,
    why="Introduce el FLCAS (Foreign Language Classroom Anxiety Scale), instrumento de referencia para "
        "medir ansiedad comunicativa, ante exámenes y miedo a la evaluación negativa. Da rigor conceptual "
        "al argumento sobre \"reducción de ansiedad\" y podría sugerirse como instrumento de evaluación futura."))
story.extend(entry(
    cite="Ahmed, A. A. A. et al. (2022). Investigating the Effect of Using Game-Based Learning on EFL "
         "Learners' Motivation and Anxiety. <i>Education Research International</i>, 2022, Article ID 6503139.",
    prox=4, unverified="lista completa de autores",
    why="Cuasi-experimental con 58 aprendices iraníes EFL (FLCAS + AMTB): el grupo game-based learning "
        "mostró reducción significativa de ansiedad. Transferible al argumento del TFM, aunque la modalidad "
        "(juego digital de vocabulario) difiere de los juegos analógicos del TFM — de ahí la proximidad 4 "
        "y no 5."))
story.extend(entry(
    cite="Amnouychokanant, V. (2025). Reducing Anxiety among EFL Learners through Gamification: An Empirical "
         "Study of Instructional Impact. <i>International Journal of Learning, Teaching and Educational "
         "Research</i>, 24(9), 80-104.",
    prox=3, unverified="posible coautoría no confirmada",
    why="46 universitarios tailandeses, gamificación instruccional (ClassPoint): reducción significativa "
        "de ansiedad en todas las dimensiones. Muy reciente (2025), refuerza actualidad bibliográfica, pero "
        "población universitaria y modalidad de puntos/insignias se alejan del contexto del TFM "
        "(secundaria, juegos analógicos) — de ahí la proximidad 3."))
story.extend(subsection("2b. Motivación intrínseca / Teoría de la Autodeterminación (Deci &amp; Ryan)"))
story.extend(entry(
    cite="Deci, E. L., &amp; Ryan, R. M. (1985). <i>Intrinsic Motivation and Self-Determination in Human "
         "Behavior</i>. Plenum Press.",
    prox=5,
    why="Obra original de la Self-Determination Theory: autonomía, competencia y relación como necesidades "
        "psicológicas básicas. Base imprescindible para justificar por qué los juegos con reglas y roles "
        "potencian la motivación más que ejercicios PPP puramente mecánicos."))
story.extend(entry(
    cite="Ryan, R. M., &amp; Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic "
         "motivation, social development, and well-being. <i>American Psychologist</i>, 55(1), 68-78.",
    prox=5,
    why="Versión madura y más citada de la SDT; formulación estándar de autonomía-competencia-relación en "
        "estudios de motivación en L2."))
story.extend(entry(
    cite="Shen, Z., Lai, M., &amp; Wang, F. (2024). Investigating the influence of gamification on motivation "
         "and learning outcomes in online language learning. <i>Frontiers in Psychology</i>, 15, 1295709.",
    prox=4,
    why="Modelo SEM (SmartPLS) con estudiantes chinos: la gamificación mejora el logro mediado por la "
        "motivación. Evidencia cuantitativa reciente sobre el mecanismo motivación->resultado que el TFM "
        "asume teóricamente."))
story.extend(entry(
    cite="Zhou, S. (2024). Gamifying language education: The impact of digital game-based learning on "
         "Chinese EFL learners. <i>Humanities and Social Sciences Communications</i>, 11.",
    prox=4, unverified="número de artículo/páginas exactas",
    why="Estudio mixto (70 participantes): el game-based learning digital (Duolingo) aumenta el disfrute, "
        "el \"yo ideal en L2\" y la motivación intrínseca vía autonomía percibida — conecta explícitamente "
        "SDT con gamificación en EFL."))
story.extend(subsection("2c. Willingness to Communicate (MacIntyre et al.)"))
story.extend(entry(
    cite="MacIntyre, P. D., Dörnyei, Z., Clément, R., &amp; Noels, K. A. (1998). Conceptualizing "
         "Willingness to Communicate in a L2: A Situational Model of L2 Confidence and Affiliation. "
         "<i>The Modern Language Journal</i>, 82(4), 545-562.",
    prox=5, unverified="orden exacto de autores en la cabecera",
    why="Modelo piramidal seminal de la Willingness to Communicate (WTC): disposición situacional a "
        "iniciar comunicación en L2, influida por confianza y afiliación. Constructo central para "
        "argumentar que los mini-juegos actúan como puente hacia la producción oral libre."))
story.extend(entry(
    cite="Reinders, H., &amp; Wattana, S. (2015). Affect and willingness to communicate in digital "
         "game-based learning. <i>ReCALL</i>, 27(1), 38-57.",
    prox=5,
    why="Muestra cómo la interacción en videojuegos digitales reduce la ansiedad y aumenta la WTC — el "
        "entorno lúdico de bajo riesgo de \"perder la cara\" facilita la disposición a comunicarse. Muy "
        "transferible al argumento de que Black Stories/Who is Who son andamiaje afectivo hacia la "
        "interacción oral."))
story.extend(entry(
    cite="MacIntyre, P. D., &amp; Wang, L. (2021). Willingness to communicate in the L2 about meaningful "
         "photos: Application of the pyramid model of WTC. <i>Language Teaching Research</i>, 25(6), "
         "878-898.",
    prox=4,
    why="Aplicación reciente del modelo piramidal de WTC a una tarea significativa; refuerza la vigencia "
        "actual del constructo y su aplicabilidad a tareas con contenido personal/afectivo, relevante para "
        "el diseño de la entrevista final."))
story.extend(subsection("2d. Engagement / Flow (Csikszentmihalyi)"))
story.extend(entry(
    cite="Csikszentmihalyi, M. (1990). <i>Flow: The Psychology of Optimal Experience</i>. Harper &amp; Row.",
    prox=4,
    why="Obra original de la teoría del flow: absorción óptima cuando el reto percibido se ajusta a la "
        "habilidad, con metas claras y feedback inmediato — características de juegos con reglas (Black "
        "Stories, juego de decisiones). Base teórica del \"enganche\" generado por las sesiones lúdicas."))
story.extend(entry(
    cite="Liu, H., &amp; Song, X. (2021). Exploring \"flow\" in young Chinese EFL learners' online English "
         "learning activities. <i>System</i>, 96, 102425.",
    prox=4, unverified="año de imprenta vs. publicación online",
    why="Estudio mixto con 235 estudiantes de secundaria (junior high): nivel de flow moderado-alto durante "
        "una actividad lúdica, asociado positivamente con el aprendizaje percibido. Población de secundaria "
        "muy próxima al contexto del TFM (4º ESO)."))
story.extend(subsection("2e. Gamificación en EFL — revisiones sistemáticas recientes"))
story.extend(entry(
    cite="Zhang, S., &amp; Hasim, Z. (2023). Gamification in EFL/ESL instruction: A systematic review of "
         "empirical research. <i>Frontiers in Psychology</i>, 13, 1030790.",
    prox=4,
    why="Revisión sistemática que sintetiza beneficios (motivación, engagement, resultados de aprendizaje) "
        "e inconvenientes de la gamificación en EFL/ESL. Útil como estado de la cuestión general, distinto "
        "del enfoque específico del TFM (TSLT + juego con reglas, no gamificación de puntos).",
    note="Año verificado como 2023 (no ambiguo) contra PubMed (PMID 36687912) y PMC (PMC9849815); el "
         "\"2022\" del DOI refleja solo el momento de aceptación en el pipeline de Frontiers."))
story.extend(entry(
    cite="Kaya, G., &amp; Sagnak, H. C. (2022). Gamification in English as Second Language Learning in "
         "Secondary Education Aged Between 11-18: A Systematic Review Between 2013-2020. <i>International "
         "Journal of Game-Based Learning</i>, 12(1), 1-14.",
    prox=5, unverified="nombres de pila de los autores",
    why="<b>La revisión más directamente comparable al contexto del TFM</b>: población 11-18 años (incluye "
        "4º ESO), EFL, gamificación en secundaria. Diez estudios muestran mejoras en motivación, "
        "participación y aprendizaje autónomo, con ganancias en gramática y vocabulario. Referencia clave "
        "para situar el TFM en el estado de la cuestión de secundaria."))

# --- Bloque 2f ---
story.extend(block(
    "Bloque 2f — Anclaje lingüístico: Interacción, Output y Noticing",
    "Cierra el hueco señalado por el librarian-critic: por qué los juegos trabajan la lengua meta en sí, "
    "no solo la motivación — un anclaje lingüístico, no solo psicológico.",
    [
        dict(cite="Long, M. H. (1996). The role of the linguistic environment in second language "
                  "acquisition. In W. C. Ritchie &amp; T. K. Bhatia (Eds.), <i>Handbook of Second Language "
                  "Acquisition</i> (pp. 413-468). Academic Press.",
             prox=5,
             why="Formulación madura de la Interaction Hypothesis: la negociación de significado durante "
                 "la interacción (comprobaciones de comprensión, peticiones de aclaración, reformulaciones) "
                 "hace el input comprensible y dirige la atención hacia la forma. Anclaje lingüístico central "
                 "para argumentar que Who is Who y el juego de vacío de información generan negociación de "
                 "significado genuina, un mecanismo de adquisición demostrado, no solo un efecto motivacional.",
             note="Verificado contra Scientific Research Publishing y ScienceDirect/Scispace (~3.800 citas) "
                  "— páginas y editorial coinciden."),
        dict(cite="Swain, M. (1995). Three functions of output in second language learning. In G. Cook "
                  "&amp; B. Seidlhofer (Eds.), <i>Principle and Practice in Applied Linguistics: Studies in "
                  "Honour of H. G. Widdowson</i> (pp. 125-144). Oxford University Press.",
             prox=5,
             why="Formula la Output Hypothesis: producir lengua fuerza al aprendiz a notar vacíos entre lo "
                 "que quiere decir y lo que puede decir, a poner a prueba hipótesis gramaticales y a "
                 "reflexionar metalingüísticamente. Justifica por qué la entrevista final (producción oral "
                 "extendida bajo presión comunicativa real) es el punto culminante idóneo de la secuencia "
                 "PPP->TSLT->ABP: maximiza el \"pushed output\" que Swain identifica como motor de adquisición.",
             note="Verificado contra Scientific Research Publishing y Scispace (~2.200 citas) — título, "
                  "páginas y editorial coinciden."),
        dict(cite="Schmidt, R. (1990). The role of consciousness in second language learning. <i>Applied "
                  "Linguistics</i>, 11(2), 129-158.",
             prox=4,
             why="Formula la Noticing Hypothesis: el \"intake\" es lo que el aprendiz nota conscientemente "
                 "en el input, no simplemente lo que recibe. Conecta con el debate PPP vs. TBLT del Bloque "
                 "1b: Swan (2005) argumenta que el noticing incidental durante la tarea no basta para "
                 "enseñar lengua nueva de forma sistemática, mientras que el PPP proporciona noticing "
                 "dirigido y explícito antes de la tarea.",
             note="Verificado contra Oxford Academic (DOI 10.1093/applin/11.2.129) y ERIC (EJ410427) — "
                  "volumen, número y páginas coinciden."),
    ]
))

# --- Bloque 3 ---
story.extend(block(
    "Bloque 3 — Communicative Language Teaching (CLT)",
    "Fundamentos del CLT y su relación con PPP y TSLT como opciones dentro de un mismo paraguas comunicativo.",
    [
        dict(cite="Canale, M., &amp; Swain, M. (1980). Theoretical bases of communicative approaches to "
                  "second language teaching and testing. <i>Applied Linguistics</i>, 1(1), 1-47.",
             prox=4,
             why="Artículo seminal que formula el constructo de competencia comunicativa (gramatical, "
                 "sociolingüística y estratégica) sobre el que se construye todo el CLT posterior. Ancla "
                 "por qué \"comunicar\" no es solo \"hablar con fluidez\": la competencia estratégica "
                 "justifica por qué los juegos con reglas (que exigen negociar significado y parafrasear "
                 "con vocabulario A2 limitado) son actividades genuinamente comunicativas y no solo lúdicas.",
             note="Verificado contra Oxford Academic (DOI 10.1093/applin/I.1.1) y referencias cruzadas "
                  "(Sci-Hub, Scientific Research Publishing)."),
        dict(cite="Richards, J. C. (2006). <i>Communicative Language Teaching Today</i>. Cambridge "
                  "University Press / SEAMEO Regional Language Centre.",
             prox=3,
             why="Síntesis de referencia sobre los principios actuales del CLT (comunicación, tarea, "
                 "significatividad). Necesaria para situar el PPP y el TSLT como opciones dentro de un "
                 "paraguas comunicativo más amplio, evitando presentar el enfoque del TFM como opuesto al CLT."),
    ]
))

# --- Bloque 4 ---
story.extend(block(
    "Bloque 4 — Scaffolding / Zona de Desarrollo Próximo (Vygotsky, Bruner)",
    "Justifica la progresión PPP (ayuda alta) -> TSLT (ayuda decreciente) -> ABP (autonomía).",
    [
        dict(cite="Vygotsky, L. S. (1978). <i>Mind in Society: The Development of Higher Psychological "
                  "Processes</i>. Harvard University Press.",
             prox=5,
             why="Fuente original de la Zona de Desarrollo Próximo (ZPD): la distancia entre lo que el "
                 "aprendiz puede hacer solo y lo que puede hacer con ayuda experta. Base imprescindible "
                 "para justificar la progresión PPP->TSLT->ABP."),
        dict(cite="Wood, D., Bruner, J. S., &amp; Ross, G. (1976). The Role of Tutoring in Problem "
                  "Solving. <i>Journal of Child Psychology and Psychiatry</i>, 17(2), 89-100.",
             prox=5,
             why="Acuña el término \"scaffolding\" (andamiaje): el nivel de asistencia es alto cuando la "
                 "tarea es nueva y se retira progresivamente. Mecanismo operativo directamente aplicable a "
                 "la secuenciación sesión a sesión del TFM."),
    ]
))

# --- Bloque 5 ---
story.extend(block(
    "Bloque 5 — Aprendizaje Basado en Proyectos (ABP/PBL) y roleplay como género",
    "Justifica la entrevista final como ABP genuino y como género discursivo con reglas propias.",
    [
        dict(cite="Beckett, G. H., &amp; Slater, T. (2005). The Project Framework: A Tool for Language, "
                  "Content, and Skills Integration. <i>ELT Journal</i>, 59(2), 108-116.",
             prox=4,
             why="Marco explícito para integrar lengua, contenido y destrezas en proyectos de aula ESL, "
                 "con diario de proyecto y planificación explícita ante el alumnado. Responde directamente "
                 "a si la entrevista es un ABP genuino (planificación, propósito, producto), no solo una "
                 "actividad más larga."),
        dict(cite="Beckett, G. H., Beck, J., Lestari, F., Yang, J., &amp; Lim, H. J. (2025). Qualitative "
                  "research synthesis of project-based (language) learning and teaching in East and "
                  "Southeast Asia: 2002-24. <i>Language Teaching Research</i> (OnlineFirst).",
             prox=4, unverified="volumen/páginas definitivos aún no asignados",
             why="Síntesis cualitativa muy reciente (2025) de más de 20 años de investigación en PBL en "
                 "lenguas extranjeras. Muestra la vigencia de la línea PBL/ABP y aporta principios de "
                 "diseño (audiencia, producto tangible, propósito comunicativo) aplicables a la entrevista."),
        dict(cite="Kasper, G., &amp; Youn, S. J. (2018). Transforming instruction to activity: Roleplay "
                  "in language assessment. <i>Applied Linguistics Review</i>, 9(4), 589-616.",
             prox=5,
             why="Analiza cómo las instrucciones de un roleplay se transforman en actividad interaccional "
                 "real, distinguiendo roleplay de simulación y tratándolo como género discursivo con "
                 "estructura de participación propia. Clave para justificar la entrevista periodística en "
                 "roleplay como género auténtico, no como \"conversación libre disfrazada\"."),
    ]
))

# --- Bloque 6 ---
story.extend(block(
    "Bloque 6 — Nivel A2 / MCER (CEFR)",
    "Ancla las expectativas de producción oral del alumnado en descriptores oficiales verificables.",
    [
        dict(cite="Council of Europe. (2020). <i>Common European Framework of Reference for Languages: "
                  "Learning, Teaching, Assessment — Companion Volume</i>. Council of Europe Publishing.",
             prox=5,
             why="Descriptores actualizados (2018/2020) de producción e interacción oral por nivel, "
                 "incluido A2. Imprescindible para justificar por qué la progresión PPP->TSLT->ABP es "
                 "coherente con lo exigible a un hablante A2 en interacción, frente a producción sostenida "
                 "(más propia de B1+)."),
    ]
))

# --- Bloque 7 ---
story.extend(block(
    "Bloque 7 — Marco curricular español: LOMLOE y BOJA (Andalucía, 4º ESO)",
    "Fuentes normativas (no artículos académicos) necesarias para el encaje curricular de la unidad.",
    [
        dict(cite="Ley Orgánica 3/2020, de 29 de diciembre (LOMLOE). BOE núm. 340, 30 de diciembre de 2020.",
             prox=3,
             why="Introduce el aprendizaje competencial y las \"situaciones de aprendizaje\" como unidad "
                 "de programación — encaje directo para justificar la unidad didáctica como una situación "
                 "de aprendizaje con tarea final auténtica."),
        dict(cite="Real Decreto 217/2022, de 29 de marzo, por el que se establece la ordenación y las "
                  "enseñanzas mínimas de la Educación Secundaria Obligatoria. BOE núm. 76, 30 de marzo de "
                  "2022 (BOE-A-2022-4975).",
             prox=3,
             why="Desarrolla a nivel estatal las enseñanzas mínimas de la ESO derivadas de la LOMLOE, "
                 "incluido el \"Perfil de salida\" competencial — fuente necesaria antes de citar el "
                 "decreto autonómico que la desarrolla."),
        dict(cite="Decreto 102/2023, de 9 de mayo, por el que se establece la ordenación y el currículo "
                  "de la etapa de ESO en Andalucía. BOJA núm. 90, 15 de mayo de 2023.",
             prox=4,
             why="Decreto autonómico vigente que debe citarse explícitamente al justificar el encaje "
                 "curricular de la unidad didáctica para 4º ESO en Andalucía."),
        dict(cite="Orden de 30 de mayo de 2023, por la que se desarrolla el currículo de la ESO en "
                  "Andalucía. BOJA núm. 104, 2 de junio de 2023.",
             prox=4,
             why="Desarrolla el Decreto 102/2023 con los saberes básicos y criterios de evaluación por "
                 "materia — fuente donde localizar los criterios específicos de Primera Lengua Extranjera "
                 "(Inglés) para 4º ESO."),
    ]
))

doc.build(story)
print(f"PDF generado: {OUT}")
