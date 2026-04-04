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
        <div className="w-full rounded-[2rem] border border-slate-200 bg-white/80 p-8 text-center shadow-soft">
          <p className="text-lg font-medium text-slate-700">Calculando resultado...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-5xl flex-col px-6 py-10 md:px-10">
      <section className="rounded-[2rem] border border-slate-200 bg-white/85 p-8 shadow-soft backdrop-blur md:p-10">
        <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
          Resultado final
        </p>
        <div className="mt-4 flex flex-wrap items-center justify-between gap-6">
          <div>
            <ResultBadge result={result.final_result} />
            <h1 className="mt-4 text-4xl font-semibold text-slate-950 md:text-5xl">
              {result.final_score.toFixed(2)} / 100
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
              {descriptions[result.final_result]}
            </p>
          </div>
          <div className="rounded-[1.75rem] bg-slate-950 px-6 py-5 text-white">
            <p className="text-xs uppercase tracking-[0.24em] text-slate-300">Sesión</p>
            <p className="mt-2 text-2xl font-semibold">#{result.session_id}</p>
          </div>
        </div>
      </section>

      <section className="mt-8 grid gap-4 md:grid-cols-2">
        {Object.entries(result.normalized_scores).map(([key, value]) => (
          <DimensionBar key={key} label={dimensionLabels[key]} value={value} />
        ))}
      </section>

      <section className="mt-8 rounded-[2rem] border border-slate-200 bg-white/75 p-8 shadow-soft backdrop-blur">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
              Puntajes brutos
            </p>
            <p className="mt-3 text-sm leading-7 text-slate-600">
              Estos valores acumulan el impacto directo de tus respuestas antes de normalizar a
              la escala de 0 a 100.
            </p>
          </div>
          <Link
            href="/test"
            className="rounded-full bg-slate-950 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Repetir test
          </Link>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {Object.entries(result.raw_scores).map(([key, value]) => (
            <div key={key} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-500">{dimensionLabels[key]}</p>
              <p className="mt-2 text-2xl font-semibold text-slate-900">{value.toFixed(2)}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
