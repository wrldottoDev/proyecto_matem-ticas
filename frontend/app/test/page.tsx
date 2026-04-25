"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { QuestionCard } from "@/components/question-card";
import { answerQuestion, createSession, getStartQuestion } from "@/lib/api";
import { Question } from "@/lib/types";

export default function TestPage() {
  const router = useRouter();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [question, setQuestion] = useState<Question | null>(null);
  const [step, setStep] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    let active = true;

    async function bootstrap() {
      try {
        const session = await createSession();
        if (!active) return;
        setSessionId(session.id);
        const firstQuestion = await getStartQuestion(session.id);
        if (!active) return;
        setQuestion(firstQuestion);
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "No se pudo iniciar el test");
      }
    }

    bootstrap();

    return () => {
      active = false;
    };
  }, []);

  const handleSelect = (optionId: number) => {
    if (!sessionId || !question) return;

    setIsSubmitting(true);
    setError(null);

    answerQuestion(sessionId, question.id, optionId)
      .then((payload) => {
        if (payload.session_finished && payload.result) {
          router.push(`/result/${payload.result.session_id}`);
          return;
        }

        if (payload.question) {
          setQuestion(payload.question);
          setStep((current) => current + 1);
        }
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "No se pudo registrar la respuesta");
      })
      .finally(() => {
        setIsSubmitting(false);
      });
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-4xl flex-col px-6 py-10 md:px-10">
      <div className="mb-8 flex items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold text-slate-950">¿Ahí es?</h1>
          <p className="mt-1 text-sm text-slate-500">
            Pregunta {step}
          </p>
        </div>
        <Link
          href="/"
          className="rounded-full border border-slate-200 bg-white/70 px-4 py-2 text-sm font-medium text-slate-500 transition hover:border-slate-300 hover:text-slate-700"
        >
          Salir
        </Link>
      </div>

      <div className="mb-6 h-2 overflow-hidden rounded-full bg-white/80">
        <div
          className="h-full rounded-full bg-gradient-to-r from-slate-800 to-slate-600 transition-all duration-500"
          style={{ width: `${Math.min(20 + step * 12, 100)}%` }}
        />
      </div>

      {error ? (
        <div className="mb-6 rounded-3xl border border-rose-200 bg-rose-50 px-5 py-4 text-sm text-rose-800">
          {error}
        </div>
      ) : null}

      {question ? (
        <QuestionCard
          question={question}
          step={step}
          onSelect={handleSelect}
          disabled={isSubmitting}
        />
      ) : (
        <section className="flex flex-col items-center rounded-[2rem] border border-slate-200 bg-white/85 p-10 shadow-soft backdrop-blur">
          <div className="mb-4 h-8 w-8 animate-spin rounded-full border-[3px] border-slate-200 border-t-slate-700" />
          <p className="text-lg font-medium text-slate-700">
            {error ? "No fue posible cargar las preguntas." : "Preparando tu evaluación..."}
          </p>
        </section>
      )}
    </main>
  );
}
