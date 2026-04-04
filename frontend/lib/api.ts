import {
  NextQuestionPayload,
  Question,
  SessionCreated,
  SessionResult,
} from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Ocurrió un error al conectar con la API");
  }

  return response.json() as Promise<T>;
}

export function createSession(): Promise<SessionCreated> {
  return apiFetch<SessionCreated>("/test/sessions", { method: "POST" });
}

export function getStartQuestion(sessionId: number): Promise<Question> {
  return apiFetch<Question>(`/test/sessions/${sessionId}/start`);
}

export function answerQuestion(
  sessionId: number,
  questionId: number,
  optionId: number,
): Promise<NextQuestionPayload> {
  return apiFetch<NextQuestionPayload>(`/test/sessions/${sessionId}/answers`, {
    method: "POST",
    body: JSON.stringify({ question_id: questionId, option_id: optionId }),
  });
}

export function getResult(sessionId: number): Promise<SessionResult> {
  return apiFetch<SessionResult>(`/test/sessions/${sessionId}/result`);
}
