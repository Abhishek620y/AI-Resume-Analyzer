import { Badge } from "@/components/ui/badge";

export default function SkillBadgeList({ skills, variant = "default", emptyText = "None" }) {
  if (!skills || skills.length === 0) {
    return <p className="text-sm text-ink-soft">{emptyText}</p>;
  }

  return (
    <div className="flex flex-wrap gap-1.5">
      {skills.map((skill) => (
        <Badge key={skill} variant={variant}>
          {skill}
        </Badge>
      ))}
    </div>
  );
}
