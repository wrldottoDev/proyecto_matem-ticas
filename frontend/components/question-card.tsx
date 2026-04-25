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
    <section className="animate-fadeIn rounded-[2rem] border border-slate-200 bg-white/85 p-6 shadow-soft backdrop-blur md:p-8">
      <h2 className="max-w-2xl text-2xl font-semibold leading-tight text-slate-900 md:text-3xl">
        {question.text}
      </h2>

      <div className="mt-8 grid gap-3">
        {question.options.map((option, index) => (
          <button
            key={option.id}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(option.id)}
            className="group rounded-2xl border border-slate-200 bg-slate-50/80 px-5 py-4 text-left transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-white hover:shadow-md disabled:cursor-not-allowed disabled:opacity-60"
            style={{ animationDelay: `${index * 60}ms` }}
          >
            <div className="flex items-center gap-4">
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border border-slate-300 text-xs font-semibold text-slate-500 transition group-hover:border-slate-900 group-hover:bg-slate-900 group-hover:text-white">
                {String.fromCharCode(65 + index)}
              </span>
              <span className="text-base font-medium text-slate-800">{option.text}</span>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}
