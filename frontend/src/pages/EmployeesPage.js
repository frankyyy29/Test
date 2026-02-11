import React, { useState, useEffect } from 'react';
import { employeesAPI } from '../api';

function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    employee_code: '',
    full_name: '',
    employee_type: 'attendance',
    position: '',
    basic_salary: '',
    bank_bpi_account: '',
  });

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    setLoading(true);
    try {
      const response = await employeesAPI.list();
      setEmployees(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch employees');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await employeesAPI.create({
        ...formData,
        basic_salary: parseFloat(formData.basic_salary),
      });
      setSuccess('Employee created successfully');
      setFormData({
        employee_code: '',
        full_name: '',
        employee_type: 'attendance',
        position: '',
        basic_salary: '',
        bank_bpi_account: '',
      });
      setShowForm(false);
      fetchEmployees();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create employee');
    }
  };

  return (
    <div>
      <h2 className="page-title">Employees</h2>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="card">
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add New Employee'}
        </button>

        {showForm && (
          <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
            <div className="form-group">
              <label>Employee Code</label>
              <input
                type="text"
                name="employee_code"
                value={formData.employee_code}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Employee Type</label>
              <select
                name="employee_type"
                value={formData.employee_type}
                onChange={handleInputChange}
              >
                <option value="attendance">Attendance</option>
                <option value="non-attendance">Non-Attendance</option>
              </select>
            </div>
            <div className="form-group">
              <label>Position</label>
              <input
                type="text"
                name="position"
                value={formData.position}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label>Basic Salary</label>
              <input
                type="number"
                name="basic_salary"
                value={formData.basic_salary}
                onChange={handleInputChange}
                step="0.01"
                required
              />
            </div>
            <div className="form-group">
              <label>Bank Account (BPI)</label>
              <input
                type="text"
                name="bank_bpi_account"
                value={formData.bank_bpi_account}
                onChange={handleInputChange}
              />
            </div>
            <button type="submit" className="btn btn-success">Create Employee</button>
          </form>
        )}
      </div>

      <div className="card">
        <h3>Employee List</h3>
        {loading ? (
          <div className="loading">Loading...</div>
        ) : employees.length === 0 ? (
          <p>No employees found.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Code</th>
                <th>Name</th>
                <th>Type</th>
                <th>Position</th>
                <th>Basic Salary</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.id}>
                  <td>{emp.id}</td>
                  <td>{emp.employee_code}</td>
                  <td>{emp.full_name}</td>
                  <td>{emp.employee_type}</td>
                  <td>{emp.position}</td>
                  <td>₱{emp.basic_salary.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default EmployeesPage;
