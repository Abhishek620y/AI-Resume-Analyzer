import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, FileText, ScanLine } from "lucide-react";
import { listResumes } from "@/services/resumeService";
import { listJDs } from "@/services/jdService";
import { analyzeResume } from "@/services/analysisService";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import SkillBadgeList from "@/components/analysis/SkillBadgeList";

export default function History() {
  const navigate = useNavigate();
  const [resumes, setResumes] = useState([]);
  const [jds, setJds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [analyzingId, setAnalyzingId] = useState(null);

  useEffect(() => {
    Promise.all([listResumes(), listJDs()])
      .then(([resumeData, jdData]) => {
        setResumes(resumeData);
        setJds(jdData);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return resumes;
    return resumes.filter((r) => {
      const haystack = [r.name, r.email, ...(r.skills || [])].join(" ").toLowerCase();
      return haystack.includes(q);
    });
  }, [resumes, search]);

  async function handleQuickAnalyze(resumeId) {
    setAnalyzingId(resumeId);
    try {
      const jdId = jds.length > 0 ? jds[0].id : null;
      const analysis = await analyzeResume(resumeId, jdId);
      navigate(`/analysis/${analysis.id}`);
    } catch {
      setAnalyzingId(null);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-extrabold text-ink">History</h1>
        <p className="mt-1 text-sm text-ink-soft">Every resume you've uploaded, searchable by name, email, or skill.</p>
      </div>

      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-ink-soft" />
        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by name, email, or skill…"
          className="pl-9"
        />
      </div>

      {loading ? (
        <p className="font-data text-sm text-ink-soft">Loading…</p>
      ) : filtered.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-sm text-ink-soft">
            {resumes.length === 0 ? "No resumes uploaded yet." : "No resumes match your search."}
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((resume) => (
            <Card key={resume.id}>
              <CardContent className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-start gap-3">
                  <FileText className="mt-0.5 size-5 shrink-0 text-signal" />
                  <div>
                    <p className="font-medium text-ink">{resume.name || "Unnamed candidate"}</p>
                    <p className="text-xs text-ink-soft">{resume.email || "No email found"}</p>
                    <div className="mt-2">
                      <SkillBadgeList skills={resume.skills?.slice(0, 6)} emptyText="No skills detected." />
                    </div>
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={analyzingId === resume.id}
                  onClick={() => handleQuickAnalyze(resume.id)}
                  className="shrink-0"
                >
                  <ScanLine className="size-3.5" />
                  {analyzingId === resume.id ? "Analyzing…" : "Analyze"}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
