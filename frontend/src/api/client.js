const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  const contentType = response.headers.get("content-type") ?? "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    const message =
      payload?.message ?? payload?.detail ?? "No se pudo completar la solicitud";
    throw new Error(Array.isArray(message) ? message[0]?.msg : message);
  }

  return payload;
}

export function getHealth() {
  return request("/health");
}

export function listCustomers() {
  return request("/api/customers");
}

export function createCustomer(data) {
  return request("/api/customers", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function listTickets() {
  return request("/api/tickets");
}

export function createTicket(data) {
  return request("/api/tickets", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function updateTicketStatus(ticketId, status) {
  return request(`/api/tickets/${ticketId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}
