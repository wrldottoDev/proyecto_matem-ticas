"use client";

import Link from "next/link";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col justify-center px-6 py-12 md:px-10">
      <div className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <section>
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-800">
            <span className="inline-block h-2 w-2 rounded-full bg-emerald-500" />
            Evaluación relacional
          </div>
          <h1 className="mt-6 max-w-3xl text-5xl font-semibold leading-[1.05] text-slate-950 md:text-7xl">
            ¿Ahí es?
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            Respondé algunas preguntas sobre tu situación y descubrí si estás
            ante una Green Flag, una Zona Gris o una Red Flag.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              href="/test"
              className="rounded-full bg-slate-950 px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-slate-950/20 transition hover:-translate-y-0.5 hover:bg-slate-800 hover:shadow-xl hover:shadow-slate-950/25 active:translate-y-0"
            >
              Comenzar evaluación
            </Link>
            <a
              href="#como-funciona"
              className="rounded-full border border-slate-300 bg-white/80 px-7 py-3.5 text-sm font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-white"
            >
              Cómo funciona
            </a>
          </div>
        </section>

        <section className="rounded-[2rem] border border-white/60 bg-white/75 p-8 shadow-soft backdrop-blur md:p-10">
          <div className="grid gap-5">
            <div className="rounded-3xl bg-emerald-50 p-5 transition hover:bg-emerald-100/70">
              <div className="flex items-center gap-2">
                <span className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-500" />
                <p className="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">
                  Green Flag
                </p>
              </div>
              <p className="mt-2 text-sm leading-6 text-emerald-900">
                Comunicación clara, respeto y coherencia sostenida.
              </p>
            </div>
            <div className="rounded-3xl bg-amber-50 p-5 transition hover:bg-amber-100/70">
              <div className="flex items-center gap-2">
                <span className="inline-block h-2.5 w-2.5 rounded-full bg-amber-500" />
                <p className="text-sm font-semibold uppercase tracking-[0.24em] text-amber-700">
                  Zona Gris
                </p>
              </div>
              <p className="mt-2 text-sm leading-6 text-amber-900">
                Señales mixtas: hay elementos rescatables, pero también inconsistencias.
              </p>
            </div>
            <div className="rounded-3xl bg-rose-50 p-5 transition hover:bg-rose-100/70">
              <div className="flex items-center gap-2">
                <span className="inline-block h-2.5 w-2.5 rounded-full bg-rose-500" />
                <p className="text-sm font-semibold uppercase tracking-[0.24em] text-rose-700">
                  Red Flag
                </p>
              </div>
              <p className="mt-2 text-sm leading-6 text-rose-900">
                Patrones de baja responsabilidad afectiva, poco respeto o interés dudoso.
              </p>
            </div>
          </div>
        </section>
      </div>

      <section
        id="como-funciona"
        className="mt-16 grid gap-6 rounded-[2rem] border border-slate-200 bg-white/80 p-8 shadow-soft backdrop-blur md:grid-cols-3"
      >
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
            01. Preguntas adaptativas
          </p>
          <p className="mt-3 text-base leading-7 text-slate-700">
            Cada respuesta abre un camino diferente; la evaluación se adapta a tu situación particular.
          </p>
        </div>
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
            02. Múltiples dimensiones
          </p>
          <p className="mt-3 text-base leading-7 text-slate-700">
            Se evalúan comunicación, respeto, coherencia, responsabilidad afectiva,
            interés real y más.
          </p>
        </div>
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
            03. Resultado detallado
          </p>
          <p className="mt-3 text-base leading-7 text-slate-700">
            Obtenés una clasificación final con un desglose visual de cada dimensión evaluada.
          </p>
        </div>
      </section>
    </main>
  );
}
