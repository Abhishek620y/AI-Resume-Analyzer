import api from "./api";

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await api.post("/upload-resume", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function getResume(id) {
  const { data } = await api.get(`/resume/${id}`);
  return data;
}

export async function listResumes() {
  const { data } = await api.get("/resumes");
  return data;
}
