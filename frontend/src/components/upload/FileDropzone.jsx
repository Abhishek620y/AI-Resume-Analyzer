import { useCallback, useState } from "react";
import { UploadCloud, FileText, X } from "lucide-react";
import { cn } from "@/lib/utils";

const ACCEPTED_EXTENSIONS = [".pdf", ".docx"];

export default function FileDropzone({ file, onFileSelect, disabled }) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState("");

  const validateAndSet = useCallback(
    (selected) => {
      setError("");
      if (!selected) return;
      const ext = "." + selected.name.split(".").pop().toLowerCase();
      if (!ACCEPTED_EXTENSIONS.includes(ext)) {
        setError("Only PDF and DOCX files are supported.");
        return;
      }
      onFileSelect(selected);
    },
    [onFileSelect]
  );

  function handleDrop(e) {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    validateAndSet(e.dataTransfer.files?.[0]);
  }

  if (file) {
    return (
      <div className="flex items-center justify-between rounded-lg border border-line bg-paper-raised px-4 py-3">
        <div className="flex items-center gap-3">
          <FileText className="size-5 text-signal" />
          <div>
            <p className="text-sm font-medium text-ink">{file.name}</p>
            <p className="text-xs text-ink-soft">{(file.size / 1024).toFixed(0)} KB</p>
          </div>
        </div>
        {!disabled && (
          <button
            onClick={() => onFileSelect(null)}
            className="rounded-full p-1 text-ink-soft hover:bg-line/40 hover:text-ink"
          >
            <X className="size-4" />
          </button>
        )}
      </div>
    );
  }

  return (
    <div>
      <label
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed px-6 py-10 text-center transition-colors",
          isDragging ? "border-signal bg-signal-soft" : "border-line bg-paper-raised hover:bg-line/20"
        )}
      >
        <UploadCloud className="size-8 text-ink-soft" strokeWidth={1.5} />
        <p className="text-sm font-medium text-ink">
          Drag and drop your resume, or <span className="text-signal">browse</span>
        </p>
        <p className="text-xs text-ink-soft">PDF or DOCX, up to 10MB</p>
        <input
          type="file"
          className="hidden"
          accept=".pdf,.docx"
          disabled={disabled}
          onChange={(e) => validateAndSet(e.target.files?.[0])}
        />
      </label>
      {error && <p className="mt-2 text-sm text-warn">{error}</p>}
    </div>
  );
}
