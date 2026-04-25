type DimensionBarProps = {
  label: string;
  value: number;
};

function getBarColor(value: number): string {
  if (value >= 65) return "bg-emerald-400";
  if (value >= 40) return "bg-amber-400";
  return "bg-rose-400";
}

export function DimensionBar({ label, value }: DimensionBarProps) {
  const width = Math.max(0, Math.min(100, value));

  return (
    <div className="rounded-2xl border border-slate-200 bg-white/80 p-4 shadow-sm backdrop-blur transition hover:shadow-md">
      <div className="mb-3 flex items-center justify-between gap-3">
        <span className="text-sm font-medium text-slate-700">{label}</span>
        <span className="text-sm font-semibold tabular-nums text-slate-900">
          {value.toFixed(0)}
        </span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-slate-100">
        <div
          className={`h-full rounded-full transition-all duration-700 ${getBarColor(value)}`}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  );
}
