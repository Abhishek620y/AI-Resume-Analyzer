import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CheckCircle2 } from "lucide-react";
import { uploadResume } from "@/services/resumeService";
import { listJDs } from "@/services/jdService";
import { analyzeResume } from "@/services/analysisService";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import FileDropzone from "@/components/upload/FileDropzone";
import SkillBadgeList from "@/components/analysis/SkillBadgeList";

export default function UploadResume() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [parsedResume, setParsedResume] = useState(null);
  const [error, setError] = useState("");

  const [jds, setJds] = useState([]);
  const [selectedJdId, setSelectedJdId] = useState("");
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    listJDs()
      .then(setJds)
      .catch(() => {});
  }, []);

  async function handleUpload() {
    if (!file) return;
    setError("");
    setUploading(true);
    try {
      const resume = await uploadResume(file);
      setParsedResume(resume);
    } catch (err) {
      setError(err.response?.data?.detail || "Couldn't upload and parse this resume.");
    } finally {
      setUploading(false);
    }
  }

  async function handleAnalyze() {
    if (!parsedResume) return;
    setAnalyzing(true);
    setError("");
    try {
      const analysis = await analyzeResume(
        parsedResume.id,
        selectedJdId ? Number(selectedJdId) : null
      );
      navigate(`/analysis/${analysis.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || "Couldn't analyze this resume.");
    } finally {
      setAnalyzing(false);
    }
  }

  function reset() {
    setFile(null);
    setParsedResume(null);
    setError("");
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-extrabold text-ink">Upload Resume</h1>
        <p className="mt-1 text-sm text-ink-soft">
          Upload a PDF or DOCX resume. We'll extract the details automatically.
        </p>
      </div>

      <Card>
        <CardContent className="p-5">
          <FileDropzone file={file} onFileSelect={setFile} disabled={uploading || !!parsedResume} />

          {error && (
            <p className="mt-3 rounded-md bg-warn-soft px-3 py-2 text-sm text-warn">{error}</p>
          )}

          {!parsedResume && (
            <Button
              className="mt-4"
              variant="signal"
              disabled={!file || uploading}
              onClick={handleUpload}
            >
              {uploading ? "Parsing resume…" : "Upload & Parse"}
            </Button>
          )}
        </CardContent>
      </Card>

      {parsedResume && (
        <>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="size-4 text-signal" /> Parsed Successfully
              </CardTitle>
              <CardDescription>Here's what we extracted from the resume.</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                <Field label="Name" value={parsedResume.name} />
                <Field label="Email" value={parsedResume.email} />
                <Field label="Phone" value={parsedResume.phone} />
              </div>

              <div>
                <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-ink-soft">
                  Skills ({parsedResume.skills?.length || 0})
                </p>
                <SkillBadgeList skills={parsedResume.skills} emptyText="No skills detected." />
              </div>

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <SectionCount label="Education entries" count={parsedResume.education?.length} />
                <SectionCount label="Experience entries" count={parsedResume.experience?.length} />
                <SectionCount label="Projects" count={parsedResume.projects?.length} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Run Analysis</CardTitle>
              <CardDescription>
                Get an ATS score, and optionally match against a job description.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-ink">
                  Match against a job description (optional)
                </label>
                <select
                  value={selectedJdId}
                  onChange={(e) => setSelectedJdId(e.target.value)}
                  className="h-10 rounded-md border border-line bg-paper-raised px-3 text-sm text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal"
                >
                  <option value="">No job description — ATS score only</option>
                  {jds.map((jd) => (
                    <option key={jd.id} value={jd.id}>
                      {jd.title} {jd.company ? `— ${jd.company}` : ""}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex gap-3">
                <Button variant="signal" disabled={analyzing} onClick={handleAnalyze}>
                  {analyzing ? "Analyzing…" : "Analyze Resume"}
                </Button>
                <Button variant="outline" onClick={reset} disabled={analyzing}>
                  Upload another
                </Button>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}

function Field({ label, value }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-ink-soft">{label}</p>
      <p className="text-sm text-ink">{value || <span className="text-ink-soft">Not found</span>}</p>
    </div>
  );
}

function SectionCount({ label, count }) {
  return (
    <div className="rounded-md border border-line px-3 py-2">
      <p className="font-data text-lg font-semibold text-ink">{count || 0}</p>
      <p className="text-xs text-ink-soft">{label}</p>
    </div>
  );
}
