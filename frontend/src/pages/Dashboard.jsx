import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  Legend,
} from "recharts";
import { TrendingUp, Target } from "lucide-react";
import { getDashboardCards, getDashboardCharts } from "@/services/dashboardService";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import StatCard from "@/components/dashboard/StatCard";
import SkillBadgeList from "@/components/analysis/SkillBadgeList";

const CHART_COLORS = { signal: "#2f6f63", warn: "#b65c3c", ink: "#12172b" };

export default function Dashboard() {
  const [cards, setCards] = useState(null);
  const [charts, setCharts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getDashboardCards(), getDashboardCharts()])
      .then(([cardsData, chartsData]) => {
        setCards(cardsData);
        setCharts(chartsData);
      })
      .catch(() => setError("Couldn't load dashboard data."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="font-data text-sm text-ink-soft">Loading dashboard…</p>;
  }

  if (error) {
    return <p className="rounded-md bg-warn-soft px-4 py-3 text-sm text-warn">{error}</p>;
  }

  const trendData = mergeTrends(charts?.ats_score_trend, charts?.match_score_trend);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-extrabold text-ink">Dashboard</h1>
        <p className="mt-1 text-sm text-ink-soft">
          A summary of every resume you've analyzed.
        </p>
      </div>

      {cards?.total_resumes === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No resumes analyzed yet</CardTitle>
            <CardDescription>
              Upload a resume to see your dashboard fill up with scores and insights.
            </CardDescription>
          </CardHeader>
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <StatCard label="Total Resumes" value={cards.total_resumes} />
            <StatCard label="Average ATS Score" value={cards.average_ats_score} suffix="/100" accent />
            <StatCard label="Average Match %" value={cards.average_match_score} suffix="%" accent />
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="size-4 text-signal" /> Top Skills
                </CardTitle>
                <CardDescription>Most common skills across analyzed resumes.</CardDescription>
              </CardHeader>
              <CardContent>
                <SkillBadgeList skills={cards.top_skills} variant="signal" emptyText="No skills detected yet." />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="size-4 text-warn" /> Top Missing Skills
                </CardTitle>
                <CardDescription>Most common gaps found when matching against job descriptions.</CardDescription>
              </CardHeader>
              <CardContent>
                <SkillBadgeList skills={cards.top_missing_skills} variant="warn" emptyText="No gaps found yet." />
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Skill Distribution</CardTitle>
              <CardDescription>How often each skill appears across your resumes.</CardDescription>
            </CardHeader>
            <CardContent>
              {charts?.skill_distribution?.length > 0 ? (
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={charts.skill_distribution}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e4e1d8" vertical={false} />
                    <XAxis dataKey="skill" tick={{ fontSize: 11, fill: "#3d4466" }} interval={0} angle={-35} textAnchor="end" height={70} />
                    <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: "#3d4466" }} />
                    <Tooltip />
                    <Bar dataKey="count" fill={CHART_COLORS.signal} radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-sm text-ink-soft">Not enough data yet.</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Score Trend</CardTitle>
              <CardDescription>Average ATS and match scores over time.</CardDescription>
            </CardHeader>
            <CardContent>
              {trendData.length > 0 ? (
                <ResponsiveContainer width="100%" height={260}>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e4e1d8" vertical={false} />
                    <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#3d4466" }} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: "#3d4466" }} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="ats" name="ATS Score" stroke={CHART_COLORS.ink} strokeWidth={2} dot={false} connectNulls />
                    <Line type="monotone" dataKey="match" name="Match %" stroke={CHART_COLORS.signal} strokeWidth={2} dot={false} connectNulls />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-sm text-ink-soft">Not enough data yet.</p>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}

function mergeTrends(atsTrend = [], matchTrend = []) {
  const byDate = {};
  for (const { date, average_score } of atsTrend) {
    byDate[date] = { ...(byDate[date] || {}), date, ats: average_score };
  }
  for (const { date, average_score } of matchTrend) {
    byDate[date] = { ...(byDate[date] || {}), date, match: average_score };
  }
  return Object.values(byDate).sort((a, b) => a.date.localeCompare(b.date));
}
