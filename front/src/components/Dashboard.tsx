import React, { useState } from "react";
import "react-calendar/dist/Calendar.css";
import "./Dashboard.css";
import {
  FaHome,
  FaUserGraduate,
  FaCalendarAlt,
  FaClipboardList,
  FaArrowRight,
  FaChartBar,
  FaEnvelope,
  FaCog,
  FaUserCircle,
} from "react-icons/fa";

const Dashboard: React.FC = () => {
  const [showUserMenu, setShowUserMenu] = useState(false);

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="logo">
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Logo_inacap.png"
            alt="Inacap"
          />
        </div>
        <div className="menu">
          <div className="menu-item">
            <span className="icon"><FaHome /></span>Dashboard
          </div>
          <div className="menu-item">
            <span className="icon"><FaUserGraduate /></span>Estudiantes
          </div>
          <div className="menu-item">
            <span className="icon"><FaCalendarAlt /></span>Entrevistas
          </div>
          <div className="menu-item">
            <span className="icon"><FaClipboardList /></span>Ajustes
          </div>
          <div className="menu-item">
            <span className="icon"><FaArrowRight /></span>Seguimiento
          </div>
          <div className="menu-item">
            <span className="icon"><FaChartBar /></span>Reportes
          </div>
          <div className="menu-item">
            <span className="icon"><FaEnvelope /></span>Mensajes
          </div>
        </div>
        <div className="settings">
          <span className="icon"><FaCog /></span>Configuracion
        </div>
      </aside>
      <main className="main-content">
        <header className="main-header">
          <h1>Sistema de Ajustes Razonables</h1>
          <div className="user-menu">
            <button className="user-btn" onClick={() => setShowUserMenu(!showUserMenu)}>
              <FaUserCircle size={24} /> Usuario ▼
            </button>
            {showUserMenu && (
              <div className="user-dropdown">
                <div className="dropdown-item">Perfil</div>
                <div className="dropdown-item">Configuración</div>
                <div className="dropdown-item">Cerrar sesión</div>
              </div>
            )}
          </div>
        </header>
        <div className="dashboard-stats">
          <div className="stat-box">
            <h4>Estudiantes</h4>
            <div>Total: <b>145</b></div>
            <div>Nuevos: <b>23</b></div>
            <div>Continuidad: <b>122</b></div>
          </div>
          <div className="stat-box">
            <h4>Pendientes</h4>
            <div>Entrevistas: <b>5</b></div>
            <div>Seguimiento: <b>12</b></div>
            <div>Ajustes: <b>7</b></div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;