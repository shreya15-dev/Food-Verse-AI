const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

async function fetchWithTimeout(url, options = {}, timeoutMs = 25000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timer);
    return res;
  } catch (err) {
    clearTimeout(timer);
    if (err.name === "AbortError") {
      throw new Error(`Request timed out after ${timeoutMs / 1000} seconds. The backend may be busy or unreachable.`);
    }
    throw err;
  }
}

export async function checkHealth() {
  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/health`, { method: "GET" }, 8000);
    if (!res.ok) throw new Error(`Server returned HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn("Health check error:", err);
    return { success: false, error: err.message };
  }
}

export async function analyzeFood(file) {
  const formData = new FormData();
  formData.append("image", file);

  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/analyze/food`, {
      method: "POST",
      body: formData,
    }, 35000);
    const json = await res.json().catch(() => ({ error: `Server returned HTTP ${res.status}` }));
    if (!res.ok) {
      return { success: false, error: json.error || `HTTP ${res.status}` };
    }
    return json;
  } catch (err) {
    console.error("Food analysis error:", err);
    return { success: false, error: err.message || "Network error: could not connect to Food Verse AI backend server." };
  }
}

export async function analyzeFreshness(file) {
  const formData = new FormData();
  formData.append("image", file);

  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/analyze/freshness`, {
      method: "POST",
      body: formData,
    }, 35000);
    const json = await res.json().catch(() => ({ error: `Server returned HTTP ${res.status}` }));
    if (!res.ok) {
      return { success: false, error: json.error || `HTTP ${res.status}` };
    }
    return json;
  } catch (err) {
    console.error("Freshness analysis error:", err);
    return { success: false, error: err.message || "Network error: could not reach freshness analysis service." };
  }
}

export async function analyzeHygiene(file) {
  const formData = new FormData();
  formData.append("media", file);

  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/analyze/hygiene`, {
      method: "POST",
      body: formData,
    }, 45000);
    const json = await res.json().catch(() => ({ error: `Server returned HTTP ${res.status}` }));
    if (!res.ok) {
      return { success: false, error: json.error || `HTTP ${res.status}` };
    }
    return json;
  } catch (err) {
    console.error("Hygiene audit error:", err);
    return { success: false, error: err.message || "Network error: could not connect to kitchen hygiene inspector." };
  }
}

export async function askCookingAssistant(payload) {
  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/recipes/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }, 30000);
    const json = await res.json().catch(() => ({ error: `Server returned HTTP ${res.status}` }));
    if (!res.ok) {
      return { success: false, error: json.error || `HTTP ${res.status}` };
    }
    return json;
  } catch (err) {
    console.error("Cooking assistant error:", err);
    return { success: false, error: err.message || "Failed to communicate with cooking assistant." };
  }
}

export async function generateMealPlan(profile) {
  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/meal-plan/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile),
    }, 30000);
    const json = await res.json().catch(() => ({ error: `Server returned HTTP ${res.status}` }));
    if (!res.ok) {
      return { success: false, error: json.error || `HTTP ${res.status}` };
    }
    return json;
  } catch (err) {
    console.error("Meal plan error:", err);
    return { success: false, error: err.message || "Failed to generate personalized meal plan." };
  }
}

export async function getSavedMealPlan() {
  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/meal-plan/saved`, { method: "GET" }, 10000);
    return await res.json().catch(() => ({ success: false, error: `HTTP ${res.status}` }));
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function getHistory(limit = 50, moduleType = null) {
  try {
    let url = `${API_BASE_URL}/history?limit=${limit}`;
    if (moduleType) url += `&module_type=${encodeURIComponent(moduleType)}`;
    const res = await fetchWithTimeout(url, { method: "GET" }, 10000);
    return await res.json().catch(() => ({ success: false, error: `HTTP ${res.status}` }));
  } catch (err) {
    console.warn("Get history error:", err);
    return { success: false, error: err.message };
  }
}

export async function getHistoryDetail(recordId) {
  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/history/${recordId}`, { method: "GET" }, 10000);
    return await res.json().catch(() => ({ success: false, error: `HTTP ${res.status}` }));
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function deleteHistoryItem(recordId) {
  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/history/${recordId}`, {
      method: "DELETE",
    }, 10000);
    return await res.json().catch(() => ({ success: false, error: `HTTP ${res.status}` }));
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function clearAllHistory() {
  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}/history`, {
      method: "DELETE",
    }, 10000);
    return await res.json().catch(() => ({ success: false, error: `HTTP ${res.status}` }));
  } catch (err) {
    return { success: false, error: err.message };
  }
}
