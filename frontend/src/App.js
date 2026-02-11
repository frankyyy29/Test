import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import EmployeesPage from './pages/EmployeesPage';
import AttendancePage from './pages/AttendancePage';
import PayrollPage from './pages/PayrollPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="navbar-container">
            <h1 className="navbar-title">Intersys I3 Payroll</h1>
            <ul className="nav-links">
              <li><Link to="/">Employees</Link></li>
              <li><Link to="/attendance">Attendance</Link></li>
              <li><Link to="/payroll">Payroll</Link></li>
            </ul>
          </div>
        </nav>
        <div className="container">
          <Routes>
            <Route path="/" element={<EmployeesPage />} />
            <Route path="/attendance" element={<AttendancePage />} />
            <Route path="/payroll" element={<PayrollPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
