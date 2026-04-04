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
};

export type Question = {
  id: number;
  text: string;
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
};

export type SessionResult = {
  session_id: number;
  final_score: number;
  final_result: "Green Flag" | "Zona Gris" | "Red Flag";
  raw_scores: DimensionScores;
  normalized_scores: DimensionScores;
};

export type NextQuestionPayload = {
  question: Question | null;
  session_finished: boolean;
  result: SessionResult | null;
};
