import * as React from "react";
import { cva } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded border px-2 py-0.5 font-data text-xs font-medium",
  {
    variants: {
      variant: {
        default: "border-line bg-line/30 text-ink",
        signal: "border-signal/30 bg-signal-soft text-signal",
        warn: "border-warn/30 bg-warn-soft text-warn",
        outline: "border-line bg-transparent text-ink-soft",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

function Badge({ className, variant, ...props }) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };
