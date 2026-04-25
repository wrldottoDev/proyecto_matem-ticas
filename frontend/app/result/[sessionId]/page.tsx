"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { DimensionBar } from "@/components/dimension-bar";
import { ResultBadge } from "@/components/result-badge";
import { getResult } from "@/lib/api";
import { SessionResult } from "@/lib/types";

const dimensionLabels: Record<string, string> = {
  comunicacion: "Comunicación",
  respeto: "Respeto",
  coherencia: "Coherencia",
  responsabilidad_afectiva: "Responsabilidad afectiva",
  interes_real: "Interés real",
  honestidad: "Honestidad",
  confianza: "Confianza",
  limites_personales: "Límites personales",
  manipulacion: "Manipulación",
  celos_control: "Celos/control",
  disponibilidad_emocional: "Disponibilidad emocional",
  compromiso: "Compromiso",
  empatia: "Empatía",
  resolucion_conflictos: "Resolución de conflictos",
  reciprocidad: "Reciprocidad",
};

const descriptions: Record<SessionResult["final_result"], string> = {
  "Green Flag":
    "La combinación de respuestas apunta a señales sanas, consistentes y respetuosas.",
  "Zona Gris":
    "Hay elementos positivos, pero el patrón todavía muestra inconsistencias o dudas relevantes.",
  "Red Flag":
    "Predominan señales que sugieren poca claridad, bajo respeto o responsabilidad afectiva débil.",
};

export default function ResultPage() {
  const params = useParams<{ sessionId: string }>();
  const [result, setResult] = useState<SessionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadResult() {
      try {
        const data = await getResult(Number(params.sessionId));
        if (!active) return;
        setResult(data);
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "No se pudo cargar el resultado");
      }
    }

    loadResult();

    return () => {
      active = false;
    };
  }, [params.sessionId]);

  if (error) {
    return (
      <main className="mx-auto flex min-h-screen max-w-4xl items-center px-6 py-10 md:px-10">
        <div className="w-full rounded-[2rem] border border-rose-200 bg-rose-50 p-8 text-rose-900 shadow-soft">
          <p className="text-lg font-semibold">No fue posible cargar el resultado</p>
          <p className="mt-3 text-sm">{error}</p>
        </div>
      </main>
    );
  }

  if (!result) {
    return (
      <main className="mx-auto flex min-h-screen max-w-4xl items-center px-6 py-10 md:px-10">
        <div className="flex w-full flex-col items-center rounded-[2rem] border border-slate-200 bg-white/80 p-8 shadow-soft">
          <div className="mb-4 h-8 w-8 animate-spin rounded-full border-[3px] border-slate-200 border-t-slate-700" />
          <p className="text-lg font-medium text-slate-700">Calculando tu resultado...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-5xl flex-col px-6 py-10 md:px-10">
      <section className="rounded-[2rem] border border-slate-200 bg-white/85 p-8 shadow-soft backdrop-blur md:p-10">
        <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
          Tu resultado
        </p>
        <div className="mt-4">
          <ResultBadge result={result.final_result} />
          <h1 className="mt-4 text-4xl font-semibold text-slate-950 md:text-5xl">
            {result.final_score.toFixed(0)} <span className="text-2xl font-normal text-slate-400 md:text-3xl">/ 100</span>
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
            {descriptions[result.final_result]}
          </p>
        </div>
      </section>

      <section className="mt-8">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
          Desglose por dimensión
        </p>
        <div className="grid gap-4 md:grid-cols-2">
          {Object.entries(result.normalized_scores).map(([key, value]) => (
            <DimensionBar key={key} label={dimensionLabels[key] ?? key} value={value} />
          ))}
        </div>
      </section>

      {result.contradiction_count > 0 && (
        <section className="mt-8 rounded-[2rem] border border-amber-200 bg-amber-50/60 p-6 backdrop-blur">
          <p className="text-sm font-medium text-amber-800">
            Se detectaron {result.contradiction_count} inconsistencia(s) en tus respuestas,
            lo cual se refleja en el puntaje final.
          </p>
        </section>
      )}

      <section className="mt-8 flex flex-wrap items-center justify-center gap-4">
        <Link
          href="/test"
          className="rounded-full bg-slate-950 px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-slate-950/20 transition hover:-translate-y-0.5 hover:bg-slate-800 hover:shadow-xl active:translate-y-0"
        >
          Volver a evaluar
        </Link>
        <Link
          href="/"
          className="rounded-full border border-slate-300 bg-white/80 px-7 py-3.5 text-sm font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-white"
        >
          Ir al inicio
        </Link>
      </section>
    </main>
  );
}
