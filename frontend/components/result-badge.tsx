import clsx from "clsx";

type ResultBadgeProps = {
  result: "Green Flag" | "Zona Gris" | "Red Flag";
};

const styles = {
  "Green Flag": "bg-emerald-100 text-emerald-800 border-emerald-300",
  "Zona Gris": "bg-amber-100 text-amber-900 border-amber-300",
  "Red Flag": "bg-rose-100 text-rose-800 border-rose-300",
};

export function ResultBadge({ result }: ResultBadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex rounded-full border px-4 py-2 text-sm font-semibold tracking-wide",
        styles[result],
      )}
    >
      {result}
    </span>
  );
}
