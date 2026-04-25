import clsx from "clsx";

type ResultBadgeProps = {
  result: "Green Flag" | "Zona Gris" | "Red Flag";
};

const styles = {
  "Green Flag": "bg-emerald-100 text-emerald-800 border-emerald-300",
  "Zona Gris": "bg-amber-100 text-amber-900 border-amber-300",
  "Red Flag": "bg-rose-100 text-rose-800 border-rose-300",
};

const dots = {
  "Green Flag": "bg-emerald-500",
  "Zona Gris": "bg-amber-500",
  "Red Flag": "bg-rose-500",
};

export function ResultBadge({ result }: ResultBadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold tracking-wide",
        styles[result],
      )}
    >
      <span className={clsx("inline-block h-2.5 w-2.5 rounded-full", dots[result])} />
      {result}
    </span>
  );
}
