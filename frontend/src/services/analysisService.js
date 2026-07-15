import api from "./api";

export async function analyzeResume(resumeId, jdId = null) {
  const { data } = await api.post("/analyze", {
    resume_id: resumeId,
    jd_id: jdId,
  });
  return data;
}

export async function getAnalysis(id) {
  const { data } = await api.get(`/analysis/${id}`);
  return data;
}
