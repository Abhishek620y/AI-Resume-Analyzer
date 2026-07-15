import api from "./api";

export async function uploadJD({ title, company, description, required_skills }) {
  const { data } = await api.post("/upload-jd", {
    title,
    company,
    description,
    required_skills: required_skills || [],
  });
  return data;
}

export async function getJD(id) {
  const { data } = await api.get(`/jd/${id}`);
  return data;
}

export async function listJDs() {
  const { data } = await api.get("/jds");
  return data;
}
