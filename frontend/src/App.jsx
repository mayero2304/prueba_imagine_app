import {
  Building2,
  CheckCircle2,
  Headphones,
  Mail,
  RefreshCw,
  Send,
  UserPlus,
  Users,
} from "lucide-react";
import { useEffect, useState } from "react";

import {
  createCustomer,
  createTicket,
  getHealth,
  listCustomers,
  listTickets,
  updateTicketStatus,
} from "./api/client";
import "./styles.css";

const initialCustomerForm = {
  name: "",
  email: "",
  company: "",
};

const initialTicketForm = {
  customer_id: "",
  title: "",
  description: "",
};

const ticketStatuses = ["Pendiente", "En progreso", "Finalizado"];
const nextTicketStatuses = {
  Pendiente: ["Pendiente", "En progreso"],
  "En progreso": ["En progreso", "Finalizado"],
  Finalizado: ["Finalizado"],
};

function formatDate(value) {
  return new Intl.DateTimeFormat("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function EmptyState({ children }) {
  return <div className="empty-state">{children}</div>;
}

export default function App() {
  const [customers, setCustomers] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [customerForm, setCustomerForm] = useState(initialCustomerForm);
  const [ticketForm, setTicketForm] = useState(initialTicketForm);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isSavingCustomer, setIsSavingCustomer] = useState(false);
  const [isSavingTicket, setIsSavingTicket] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  async function loadData({ showLoading = false } = {}) {
    if (showLoading) {
      setIsLoading(true);
    } else {
      setIsRefreshing(true);
    }
    setError("");

    try {
      const [health, customerData, ticketData] = await Promise.all([
        getHealth(),
        listCustomers(),
        listTickets(),
      ]);

      if (health.status !== "ok") {
        throw new Error("No se pudo validar el estado de la API");
      }
      setCustomers(customerData);
      setTickets(ticketData);
    } catch (refreshError) {
      setError(refreshError.message);
    } finally {
      if (showLoading) {
        setIsLoading(false);
      } else {
        setIsRefreshing(false);
      }
    }
  }

  function refreshData() {
    return loadData();
  }

  useEffect(() => {
    Promise.all([getHealth(), listCustomers(), listTickets()])
      .then(([health, customerData, ticketData]) => {
        if (health.status !== "ok") {
          throw new Error("No se pudo validar el estado de la API");
        }
        setCustomers(customerData);
        setTickets(ticketData);
      })
      .catch((refreshError) => {
        setError(refreshError.message);
      })
      .finally(() => setIsLoading(false));
  }, []);

  async function handleCreateCustomer(event) {
    event.preventDefault();
    setIsSavingCustomer(true);
    setError("");
    setNotice("");

    try {
      const customer = await createCustomer(customerForm);
      setCustomerForm(initialCustomerForm);
      setNotice("Cliente registrado");
      setCustomers((currentCustomers) => [...currentCustomers, customer]);
    } catch (createError) {
      setError(createError.message);
    } finally {
      setIsSavingCustomer(false);
    }
  }

  async function handleCreateTicket(event) {
    event.preventDefault();
    setIsSavingTicket(true);
    setError("");
    setNotice("");

    try {
      const ticket = await createTicket({
        ...ticketForm,
        customer_id: Number(ticketForm.customer_id),
      });
      setTicketForm(initialTicketForm);
      setNotice("Ticket creado");
      setTickets((currentTickets) => [...currentTickets, ticket]);
    } catch (createError) {
      setError(createError.message);
    } finally {
      setIsSavingTicket(false);
    }
  }

  async function handleStatusChange(ticketId, status) {
    setError("");
    setNotice("");

    try {
      const updatedTicket = await updateTicketStatus(ticketId, status);
      setNotice("Estado actualizado");
      setTickets((currentTickets) =>
        currentTickets.map((ticket) =>
          ticket.id === updatedTicket.id ? updatedTicket : ticket,
        ),
      );
    } catch (updateError) {
      setError(updateError.message);
    }
  }

  const customerById = new Map(
    customers.map((customer) => [customer.id, customer]),
  );

  return (
    <main className="app-shell">
      <section className="summary">
        <div>
          <p className="eyebrow">Prueba tecnica Finanz</p>
          <h1>Gestion de clientes y tickets</h1>
        </div>
      </section>

      <section className="toolbar" aria-label="Acciones generales">
        <div className="metrics">
          <span>
            <Users size={16} aria-hidden="true" />
            {customers.length} clientes
          </span>
          <span>
            <Headphones size={16} aria-hidden="true" />
            {tickets.length} tickets
          </span>
        </div>
        <button className="icon-button" type="button" onClick={refreshData}>
          <RefreshCw size={16} aria-hidden="true" />
          {isRefreshing ? "Actualizando" : "Actualizar"}
        </button>
      </section>

      {notice ? (
        <div className="feedback feedback-success">
          <CheckCircle2 size={16} aria-hidden="true" />
          {notice}
        </div>
      ) : null}

      {error ? (
        <div className="feedback feedback-error" role="alert">
          {error}
        </div>
      ) : null}

      <section className="workspace" aria-label="Gestion de soporte">
        <div className="column">
          <section className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Clientes</p>
                <h2>Registrar cliente</h2>
              </div>
              <UserPlus size={22} aria-hidden="true" />
            </div>

            <form className="form-grid" onSubmit={handleCreateCustomer}>
              <label>
                Nombre
                <input
                  required
                  minLength={1}
                  maxLength={120}
                  value={customerForm.name}
                  onChange={(event) =>
                    setCustomerForm({
                      ...customerForm,
                      name: event.target.value,
                    })
                  }
                />
              </label>
              <label>
                Correo
                <span className="input-with-icon">
                  <Mail size={16} aria-hidden="true" />
                  <input
                    required
                    type="email"
                    maxLength={180}
                    value={customerForm.email}
                    onChange={(event) =>
                      setCustomerForm({
                        ...customerForm,
                        email: event.target.value,
                      })
                    }
                  />
                </span>
              </label>
              <label>
                Empresa
                <span className="input-with-icon">
                  <Building2 size={16} aria-hidden="true" />
                  <input
                    required
                    maxLength={160}
                    value={customerForm.company}
                    onChange={(event) =>
                      setCustomerForm({
                        ...customerForm,
                        company: event.target.value,
                      })
                    }
                  />
                </span>
              </label>
              <button
                className="primary-button"
                type="submit"
                disabled={isSavingCustomer}
              >
                <Send size={16} aria-hidden="true" />
                {isSavingCustomer ? "Guardando" : "Crear cliente"}
              </button>
            </form>
          </section>

          <section className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Directorio</p>
                <h2>Clientes registrados</h2>
              </div>
            </div>

            {isLoading ? (
              <EmptyState>Cargando clientes</EmptyState>
            ) : customers.length === 0 ? (
              <EmptyState>Sin clientes registrados</EmptyState>
            ) : (
              <div className="table-shell">
                <table>
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Correo</th>
                      <th>Empresa</th>
                    </tr>
                  </thead>
                  <tbody>
                    {customers.map((customer) => (
                      <tr key={customer.id}>
                        <td>{customer.name}</td>
                        <td>{customer.email}</td>
                        <td>{customer.company}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>

        <div className="column">
          <section className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Tickets</p>
                <h2>Crear ticket</h2>
              </div>
              <Headphones size={22} aria-hidden="true" />
            </div>

            <form className="form-grid" onSubmit={handleCreateTicket}>
              <label>
                Cliente
                <select
                  required
                  value={ticketForm.customer_id}
                  onChange={(event) =>
                    setTicketForm({
                      ...ticketForm,
                      customer_id: event.target.value,
                    })
                  }
                >
                  <option value="">Seleccione un cliente</option>
                  {customers.map((customer) => (
                    <option key={customer.id} value={customer.id}>
                      {customer.name} - {customer.company}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Titulo
                <input
                  required
                  maxLength={160}
                  value={ticketForm.title}
                  onChange={(event) =>
                    setTicketForm({
                      ...ticketForm,
                      title: event.target.value,
                    })
                  }
                />
              </label>
              <label>
                Descripcion
                <textarea
                  required
                  rows="4"
                  value={ticketForm.description}
                  onChange={(event) =>
                    setTicketForm({
                      ...ticketForm,
                      description: event.target.value,
                    })
                  }
                />
              </label>
              <button
                className="primary-button"
                type="submit"
                disabled={isSavingTicket || customers.length === 0}
              >
                <Send size={16} aria-hidden="true" />
                {isSavingTicket ? "Guardando" : "Crear ticket"}
              </button>
            </form>
          </section>

          <section className="panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Seguimiento</p>
                <h2>Tickets registrados</h2>
              </div>
            </div>

            {isLoading ? (
              <EmptyState>Cargando tickets</EmptyState>
            ) : tickets.length === 0 ? (
              <EmptyState>Sin tickets registrados</EmptyState>
            ) : (
              <div className="ticket-list">
                {tickets.map((ticket) => {
                  const customer = customerById.get(ticket.customer_id);

                  return (
                    <article className="ticket-item" key={ticket.id}>
                      <div>
                        <div className="ticket-title-row">
                          <h3>{ticket.title}</h3>
                          <span className={`badge ${ticket.status}`}>
                            {ticket.status}
                          </span>
                        </div>
                        <p>{ticket.description}</p>
                        <small>
                          {customer?.name ?? "Cliente no encontrado"} ·{" "}
                          {formatDate(ticket.created_at)}
                        </small>
                      </div>
                      <label className="compact-label">
                        Estado
                        <select
                          value={ticket.status}
                          onChange={(event) =>
                            handleStatusChange(ticket.id, event.target.value)
                          }
                        >
                          {(nextTicketStatuses[ticket.status] ?? ticketStatuses).map((status) => (
                            <option key={status} value={status}>
                              {status}
                            </option>
                          ))}
                        </select>
                      </label>
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}
