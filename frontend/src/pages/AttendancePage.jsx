import React, { useState, useEffect } from 'react';
import { attendanceAPI, employeesAPI } from '../api';

function AttendancePage() {
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState('');
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    date: '',
    time_in: '',
    time_out: '',
    break_minutes: '60',
    ot_minutes: '0',
    late_minutes: '0',
    status: 'present',
  });

  useEffect(() => {
    fetchEmployees();
  }, []);

  useEffect(() => {
    if (selectedEmployee) {
      fetchAttendance(selectedEmployee);
    }
  }, [selectedEmployee]);

  const fetchEmployees = async () => {
    try {
      const response = await employeesAPI.list();
      setEmployees(response.data);
    } catch (err) {
      setError('Failed to fetch employees');
    }
  };

  const fetchAttendance = async (empId) => {
    setLoading(true);
    try {
      const response = await attendanceAPI.list(empId);
      setAttendance(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch attendance');
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
    if (!selectedEmployee) {
      setError('Please select an employee');
      return;
    }

    try {
      await attendanceAPI.create(selectedEmployee, {
        ...formData,
        break_minutes: parseInt(formData.break_minutes),
        ot_minutes: parseInt(formData.ot_minutes),
        late_minutes: parseInt(formData.late_minutes),
      });
      setSuccess('Attendance logged successfully');
      setFormData({
        date: '',
        time_in: '',
        time_out: '',
        break_minutes: '60',
        ot_minutes: '0',
        late_minutes: '0',
        status: 'present',
      });
      setShowForm(false);
      fetchAttendance(selectedEmployee);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to log attendance');
    }
  };

  return (
    <div>
      <h2 className="page-title">Attendance</h2>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="card">
        <div className="form-group">
          <label>Select Employee</label>
          <select
            value={selectedEmployee}
            onChange={(e) => setSelectedEmployee(e.target.value)}
          >
            <option value="">-- Choose Employee --</option>
            {employees.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.full_name} ({emp.employee_code})
              </option>
            ))}
          </select>
        </div>

        {selectedEmployee && (
          <>
            <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
              {showForm ? 'Cancel' : 'Log Attendance'}
            </button>

            {showForm && (
              <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
                <div className="form-group">
                  <label>Date</label>
                  <input
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Time In</label>
                  <input
                    type="time"
                    name="time_in"
                    value={formData.time_in}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Time Out</label>
                  <input
                    type="time"
                    name="time_out"
                    value={formData.time_out}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Break (minutes)</label>
                  <input
                    type="number"
                    name="break_minutes"
                    value={formData.break_minutes}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="form-group">
                  <label>Overtime (minutes)</label>
                  <input
                    type="number"
                    name="ot_minutes"
                    value={formData.ot_minutes}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="form-group">
                  <label>Late (minutes)</label>
                  <input
                    type="number"
                    name="late_minutes"
                    value={formData.late_minutes}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="form-group">
                  <label>Status</label>
                  <select
                    name="status"
                    value={formData.status}
                    onChange={handleInputChange}
                  >
                    <option value="present">Present</option>
                    <option value="absent">Absent</option>
                    <option value="leave">Leave</option>
                  </select>
                </div>
                <button type="submit" className="btn btn-success">Log Attendance</button>
              </form>
            )}
          </>
        )}
      </div>

      {selectedEmployee && (
        <div className="card">
          <h3>Attendance Records</h3>
          {loading ? (
            <div className="loading">Loading...</div>
          ) : attendance.length === 0 ? (
            <p>No attendance records found.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time In</th>
                  <th>Time Out</th>
                  <th>Status</th>
                  <th>Late (min)</th>
                  <th>OT (min)</th>
                </tr>
              </thead>
              <tbody>
                {attendance.map((rec) => (
                  <tr key={rec.id}>
                    <td>{rec.date}</td>
                    <td>{rec.time_in}</td>
                    <td>{rec.time_out}</td>
                    <td>{rec.status}</td>
                    <td>{rec.late_minutes}</td>
                    <td>{rec.ot_minutes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

export default AttendancePage;
