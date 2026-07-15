import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

/**
 * Lightweight placeholder for pages whose full implementation lands in
 * Module 11 (Frontend Pages). Keeping these as real routed components
 * now lets the app shell, navigation, and protected routing all be
 * verified end-to-end ahead of that module.
 */
export default function PagePlaceholder({ title, description }) {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-extrabold text-ink">{title}</h1>
        <p className="mt-1 text-sm text-ink-soft">{description}</p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Coming in Module 11</CardTitle>
          <CardDescription>
            This page's full functionality is built in the next module. The
            navigation, layout, and routing you're seeing now are already wired up.
          </CardDescription>
        </CardHeader>
        <CardContent />
      </Card>
    </div>
  );
}
