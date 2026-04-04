import { Question } from "@/lib/types";

type QuestionCardProps = {
  question: Question;
  step: number;
  onSelect: (optionId: number) => void;
  disabled?: boolean;
};

export function QuestionCard({
  question,
  step,
  onSelect,
  disabled = false,
}: QuestionCardProps) {
  return (
    <section className="rounded-[2rem] border border-slate-200 bg-white/85 p-6 shadow-soft backdrop-blur md:p-8">
      <div className="mb-6 flex items-center justify-between gap-4">
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-600">
          Paso {step}
        </span>
        <span className="text-xs font-medium uppercase tracking-[0.24em] text-slate-400">
          Cuestionario dinámico
        </span>
      </div>

      <h2 className="max-w-2xl text-2xl font-semibold leading-tight text-slate-900 md:text-3xl">
        {question.text}
      </h2>

      <div className="mt-8 grid gap-4">
        {question.options.map((option) => (
          <button
            key={option.id}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(option.id)}
            className="group rounded-3xl border border-slate-200 bg-slate-50 px-5 py-4 text-left transition hover:-translate-y-0.5 hover:border-slate-300 hover:bg-white disabled:cursor-not-allowed disabled:opacity-60"
          >
            <div className="flex items-center justify-between gap-4">
              <span className="text-base font-medium text-slate-800">{option.text}</span>
              <span className="text-sm text-slate-400 transition group-hover:text-slate-600">
                Elegir
              </span>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}
