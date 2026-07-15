import { cn } from "@/lib/utils";

const CATEGORY_MAX = {
  formatting: 15,
  skills: 20,
  projects: 20,
  experience: 20,
  education: 10,
  grammar: 15,
};

const CATEGORY_LABELS = {
  formatting: "Formatting",
  skills: "Skills",
  projects: "Projects",
  experience: "Experience",
  education: "Education",
  grammar: "Grammar",
};

function scoreColor(total) {
  if (total >= 80) return "text-signal border-signal";
  if (total >= 60) return "text-ink border-ink";
  return "text-warn border-warn";
}

export default function ScoreBreakdown({ score, breakdown }) {
  return (
    <div className="flex flex-col gap-6 sm:flex-row sm:items-start">
      {/* Signature "stamp" badge -- an itemized, auditable score, not a
          generic circular progress ring. Reinforces the explainable-
          scoring philosophy the doc emphasizes for the viva. */}
      <div
        className={cn(
          "flex w-32 shrink-0 flex-col items-center justify-center gap-0.5 rounded-lg border-2 py-5",
          scoreColor(score)
        )}
      >
        <span className="font-data text-4xl font-bold leading-none">{score}</span>
        <span className="font-data text-[10px] uppercase tracking-widest text-ink-soft">
          / 100 ATS
        </span>
      </div>

      <div className="flex flex-1 flex-col gap-2.5">
        {Object.entries(CATEGORY_LABELS).map(([key, label]) => {
          const value = breakdown?.[key] ?? 0;
          const max = CATEGORY_MAX[key];
          const pct = Math.min(100, (value / max) * 100);
          return (
            <div key={key} className="flex items-center gap-3">
              <span className="w-24 shrink-0 text-xs font-medium text-ink-soft">{label}</span>
              <div className="h-2 flex-1 rounded-full bg-line/50">
                <div
                  className="h-2 rounded-full bg-signal transition-all"
                  style={{ width: `${pct}%` }}
                />
              </div>
              <span className="w-16 shrink-0 text-right font-data text-xs text-ink">
                {value}/{max}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
