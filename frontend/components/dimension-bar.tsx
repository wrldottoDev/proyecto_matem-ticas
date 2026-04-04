type DimensionBarProps = {
  label: string;
  value: number;
};

export function DimensionBar({ label, value }: DimensionBarProps) {
  const width = Math.max(0, Math.min(100, value));

  return (
    <div className="rounded-3xl border border-slate-200 bg-white/80 p-4 shadow-sm backdrop-blur">
      <div className="mb-3 flex items-center justify-between gap-3">
        <span className="text-sm font-medium text-slate-600">{label}</span>
        <span className="text-sm font-semibold text-slate-900">{value.toFixed(2)}</span>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-gradient-to-r from-emerald-400 via-amber-400 to-rose-400"
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  );
}
