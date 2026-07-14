import { API_BASE_URL } from "@/lib/config";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || `Request failed with ${response.status}`);
  }

  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

export async function getConversation(userId) {
  return request(`/messages?user_id=${encodeURIComponent(userId)}`);
}

export async function queryAgent({ userId, question }) {
  return request("/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_id: userId, question }),
  });
}

export async function uploadDocument({ userId, file }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("user_id", userId);

  return request("/upload", {
    method: "POST",
    body: formData,
  });
}