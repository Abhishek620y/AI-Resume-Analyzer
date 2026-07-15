import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-24 text-center">
      <p className="font-data text-5xl font-bold text-ink-soft">404</p>
      <p className="text-sm text-ink-soft">This page doesn't exist.</p>
      <Button asChild variant="signal" className="mt-2">
        <Link to="/">Back to Dashboard</Link>
      </Button>
    </div>
  );
}
