import api from "./api";

export async function getDashboardCards() {
  const { data } = await api.get("/dashboard/cards");
  return data;
}

export async function getDashboardCharts() {
  const { data } = await api.get("/dashboard/charts");
  return data;
}
