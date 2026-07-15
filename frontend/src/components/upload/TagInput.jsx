import { useState } from "react";
import { X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

export default function TagInput({ tags, onChange, placeholder }) {
  const [draft, setDraft] = useState("");

  function commitDraft() {
    const value = draft.trim();
    if (value && !tags.includes(value)) {
      onChange([...tags, value]);
    }
    setDraft("");
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      commitDraft();
    } else if (e.key === "Backspace" && !draft && tags.length > 0) {
      onChange(tags.slice(0, -1));
    }
  }

  function removeTag(tag) {
    onChange(tags.filter((t) => t !== tag));
  }

  return (
    <div>
      <div className="flex flex-wrap items-center gap-1.5 rounded-md border border-line bg-paper-raised p-2">
        {tags.map((tag) => (
          <Badge key={tag} variant="signal" className="gap-1">
            {tag}
            <button type="button" onClick={() => removeTag(tag)}>
              <X className="size-3" />
            </button>
          </Badge>
        ))}
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={commitDraft}
          placeholder={tags.length === 0 ? placeholder : ""}
          className="min-w-[120px] flex-1 border-none bg-transparent px-1 py-1 text-sm text-ink outline-none placeholder:text-ink-soft/60"
        />
      </div>
      <p className="mt-1 text-xs text-ink-soft">Press Enter to add a skill.</p>
    </div>
  );
}
