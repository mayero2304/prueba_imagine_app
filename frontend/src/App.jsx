import { Activity, Headphones, Users } from "lucide-react";
import { useEffect, useState } from "react";

import { getHealth } from "./api/health";
import "./styles.css";

const modules = [
  {
    title: "Clientes",
    description: "Registro y consulta de clientes.",
    icon: Users,
  },
  {
    title: "Tickets",
    description: "Creacion y seguimiento de solicitudes.",
    icon: Headphones,
  },
];

export default function App() {
  const [apiStatus, setApiStatus] = useState("validando");

  useEffect(() => {
    getHealth()
      .then(() => setApiStatus("conectada"))
      .catch(() => setApiStatus("sin conexion"));
  }, []);

  return (
    <main className="app-shell">
      <section className="summary">
        <div>
          <p className="eyebrow">Prueba tecnica Finanz</p>
          <h1>Gestion de clientes y tickets</h1>
        </div>
        <span className={`status status-${apiStatus.replace(" ", "-")}`}>
          <Activity size={16} aria-hidden="true" />
          API {apiStatus}
        </span>
      </section>

      <section className="module-grid" aria-label="Modulos principales">
        {modules.map((module) => {
          const Icon = module.icon;

          return (
            <article className="module-card" key={module.title}>
              <Icon size={24} aria-hidden="true" />
              <div>
                <h2>{module.title}</h2>
                <p>{module.description}</p>
              </div>
            </article>
          );
        })}
      </section>
    </main>
  );
}
