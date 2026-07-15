import { useEffect, useState } from "react";
import { Briefcase } from "lucide-react";
import { uploadJD, listJDs } from "@/services/jdService";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import TagInput from "@/components/upload/TagInput";
import SkillBadgeList from "@/components/analysis/SkillBadgeList";

export default function UploadJD() {
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [description, setDescription] = useState("");
  const [skills, setSkills] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const [jds, setJds] = useState([]);
  const [loadingList, setLoadingList] = useState(true);

  function refreshList() {
    setLoadingList(true);
    listJDs()
      .then(setJds)
      .catch(() => {})
      .finally(() => setLoadingList(false));
  }

  useEffect(refreshList, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await uploadJD({ title, company, description, required_skills: skills });
      setTitle("");
      setCompany("");
      setDescription("");
      setSkills([]);
      refreshList();
    } catch (err) {
      setError(err.response?.data?.detail || "Couldn't save this job description.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-extrabold text-ink">Upload Job Description</h1>
        <p className="mt-1 text-sm text-ink-soft">
          Add a role to match candidate resumes against. Leave skills blank and we'll
          extract them from the description automatically.
        </p>
      </div>

      <Card>
        <CardContent className="p-5">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="title">Job Title</Label>
                <Input
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Software Engineer"
                  required
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="company">Company (optional)</Label>
                <Input
                  id="company"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  placeholder="Acme Corp"
                />
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="description">Description</Label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
                rows={6}
                placeholder="We need a strong engineer skilled in Python, FastAPI, SQL, Docker, and AWS..."
                className="rounded-md border border-line bg-paper-raised px-3 py-2 text-sm text-ink placeholder:text-ink-soft/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <Label>Required Skills (optional — auto-extracted if left blank)</Label>
              <TagInput tags={skills} onChange={setSkills} placeholder="e.g. Python, Docker, AWS" />
            </div>

            {error && (
              <p className="rounded-md bg-warn-soft px-3 py-2 text-sm text-warn">{error}</p>
            )}

            <Button type="submit" variant="signal" disabled={submitting} className="self-start">
              {submitting ? "Saving…" : "Save Job Description"}
            </Button>
          </form>
        </CardContent>
      </Card>

      <div>
        <h2 className="mb-3 font-display text-lg font-bold text-ink">Your Job Descriptions</h2>
        {loadingList ? (
          <p className="font-data text-sm text-ink-soft">Loading…</p>
        ) : jds.length === 0 ? (
          <p className="text-sm text-ink-soft">No job descriptions yet.</p>
        ) : (
          <div className="flex flex-col gap-3">
            {jds.map((jd) => (
              <Card key={jd.id}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Briefcase className="size-4 text-signal" />
                    {jd.title}
                    {jd.company && <span className="text-ink-soft font-normal">— {jd.company}</span>}
                  </CardTitle>
                  <CardDescription className="line-clamp-2">{jd.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <SkillBadgeList skills={jd.required_skills} variant="signal" emptyText="No required skills detected." />
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
