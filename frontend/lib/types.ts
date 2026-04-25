export type OptionEffect = {
  id: number;
  dimension: string;
  value: number;
};

export type QuestionOption = {
  id: number;
  text: string;
  created_at: string;
  effects: OptionEffect[];
  next_question_id: number | null;
  activates_contradiction: boolean;
  contradiction_code: string | null;
  contradiction_penalty: number;
};

export type Question = {
  id: number;
  key: string | null;
  text: string;
  main_dimension: string | null;
  is_start: boolean;
  is_terminal: boolean;
  created_at: string;
  options: QuestionOption[];
};

export type SessionCreated = {
  id: number;
  started_at: string;
};

export type DimensionScores = {
  comunicacion: number;
  respeto: number;
  coherencia: number;
  responsabilidad_afectiva: number;
  interes_real: number;
  honestidad: number;
  confianza: number;
  limites_personales: number;
  manipulacion: number;
  celos_control: number;
  disponibilidad_emocional: number;
  compromiso: number;
  empatia: number;
  resolucion_conflictos: number;
  reciprocidad: number;
};

export type SessionResult = {
  session_id: number;
  final_score: number;
  final_result: "Green Flag" | "Zona Gris" | "Red Flag";
  raw_scores: DimensionScores;
  normalized_scores: DimensionScores;
  contradiction_count: number;
  contradictions: string[];
};

export type NextQuestionPayload = {
  question: Question | null;
  session_finished: boolean;
  result: SessionResult | null;
};
