import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export default function StatCard({ label, value, suffix = "", accent = false }) {
  return (
    <Card>
      <CardContent className="p-5">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-soft">{label}</p>
        <p
          className={cn(
            "mt-2 font-data text-3xl font-semibold",
            accent ? "text-signal" : "text-ink"
          )}
        >
          {value}
          {suffix && <span className="text-lg text-ink-soft">{suffix}</span>}
        </p>
      </CardContent>
    </Card>
  );
}
