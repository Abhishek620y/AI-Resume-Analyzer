import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Sparkles, CheckCircle2, XCircle } from "lucide-react";
import { getAnalysis } from "@/services/analysisService";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import ScoreBreakdown from "@/components/analysis/ScoreBreakdown";
import SkillBadgeList from "@/components/analysis/SkillBadgeList";

export default function AnalysisView() {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    getAnalysis(id)
      .then(setAnalysis)
      .catch(() => setError("Couldn't load this analysis."))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <p className="font-data text-sm text-ink-soft">Loading analysis…</p>;
  }

  if (error || !analysis) {
    return <p className="rounded-md bg-warn-soft px-4 py-3 text-sm text-warn">{error || "Analysis not found."}</p>;
  }

  const hasMatch = analysis.match_score !== null && analysis.match_score !== undefined;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link to="/history" className="flex items-center gap-1.5 text-sm text-ink-soft hover:text-ink">
          <ArrowLeft className="size-3.5" /> Back to history
        </Link>
        <h1 className="mt-2 font-display text-2xl font-extrabold text-ink">Analysis Result</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>ATS Score Breakdown</CardTitle>
          <CardDescription>
            Explainable, rule-based scoring — every point is traceable to a specific criterion.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ScoreBreakdown score={analysis.ats_score} breakdown={analysis.score_breakdown} />
        </CardContent>
      </Card>

      {hasMatch && (
        <Card>
          <CardHeader>
            <CardTitle>Job Match</CardTitle>
            <CardDescription>How well this resume fits the selected job description.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="flex items-baseline gap-2">
              <span className="font-data text-3xl font-bold text-signal">{analysis.match_score}%</span>
              <span className="text-sm text-ink-soft">match</span>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <p className="mb-1.5 flex items-center gap-1.5 text-xs font-medium uppercase tracking-wide text-signal">
                  <CheckCircle2 className="size-3.5" /> Matched Skills
                </p>
                <SkillBadgeList skills={analysis.matched_skills} variant="signal" emptyText="No matched skills." />
              </div>
              <div>
                <p className="mb-1.5 flex items-center gap-1.5 text-xs font-medium uppercase tracking-wide text-warn">
                  <XCircle className="size-3.5" /> Missing Skills
                </p>
                <SkillBadgeList skills={analysis.missing_skills} variant="warn" emptyText="No missing skills." />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="size-4 text-signal" /> AI Career Coach Feedback
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <p className="text-sm leading-relaxed text-ink">{analysis.feedback}</p>

          {analysis.recommendations?.length > 0 && (
            <div>
              <p className="mb-2 text-xs font-medium uppercase tracking-wide text-ink-soft">
                Recommendations
              </p>
              <ul className="flex flex-col gap-1.5">
                {analysis.recommendations.map((rec, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink">
                    <span className="mt-1.5 size-1 shrink-0 rounded-full bg-signal" />
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
