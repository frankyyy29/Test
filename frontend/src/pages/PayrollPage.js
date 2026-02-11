import React, { useState, useEffect } from 'react';
import { payrollAPI } from '../api';

function PayrollPage() {
  const [payslips, setPayslips] = useState([]);
  const [selectedRun, setSelectedRun] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showRunForm, setShowRunForm] = useState(false);
  const [formData, setFormData] = useState({
    cutoff_start_date: '',
    cutoff_end_date: '',
  });

  useEffect(() => {
    // Could fetch runs here if API provides a list endpoint
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleRunPayroll = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await payrollAPI.run(formData);
      setSuccess(`Payroll run created with ID: ${response.data.id}`);
      setFormData({
        cutoff_start_date: '',
        cutoff_end_date: '',
      });
      setShowRunForm(false);
      setSelectedRun(response.data.id);
      fetchPayslips(response.data.id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to run payroll');
    } finally {
      setLoading(false);
    }
  };

  const fetchPayslips = async (runId) => {
    setLoading(true);
    try {
      const response = await payrollAPI.getPayslips(runId);
      setPayslips(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch payslips');
    } finally {
      setLoading(false);
    }
  };

  const downloadPayslip = async (runId, employeeId) => {
    try {
      const blob = await payrollAPI.downloadPayslip(runId, employeeId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `payslip_${employeeId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError('Failed to download payslip');
    }
  };

  const downloadSummary = async (runId) => {
    try {
      const blob = await payrollAPI.downloadSummary(runId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `payroll_summary_${runId}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError('Failed to download summary');
    }
  };

  return (
    <div>
      <h2 className="page-title">Payroll</h2>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="card">
        <button className="btn btn-primary" onClick={() => setShowRunForm(!showRunForm)}>
          {showRunForm ? 'Cancel' : 'Run Payroll'}
        </button>

        {showRunForm && (
          <form onSubmit={handleRunPayroll} style={{ marginTop: '20px' }}>
            <div className="form-group">
              <label>Cutoff Start Date</label>
              <input
                type="date"
                name="cutoff_start_date"
                value={formData.cutoff_start_date}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Cutoff End Date</label>
              <input
                type="date"
                name="cutoff_end_date"
                value={formData.cutoff_end_date}
                onChange={handleInputChange}
                required
              />
            </div>
            <button type="submit" className="btn btn-success" disabled={loading}>
              {loading ? 'Processing...' : 'Run Payroll'}
            </button>
          </form>
        )}
      </div>

      {selectedRun && (
        <div className="card">
          <div style={{ marginBottom: '20px' }}>
            <h3>Payroll Run #{selectedRun}</h3>
            <button className="btn btn-primary btn-small" onClick={() => downloadSummary(selectedRun)}>
              Download Summary Excel
            </button>
          </div>

          <h3>Payslips</h3>
          {loading ? (
            <div className="loading">Loading...</div>
          ) : payslips.length === 0 ? (
            <p>No payslips found.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Employee ID</th>
                  <th>Employee Code</th>
                  <th>Employee Name</th>
                  <th>Gross</th>
                  <th>Deductions</th>
                  <th>Net Pay</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {payslips.map((slip) => (
                  <tr key={slip.id}>
                    <td>{slip.employee_id}</td>
                    <td>{slip.employee_code || 'N/A'}</td>
                    <td>{slip.employee_name || 'N/A'}</td>
                    <td>₱{slip.gross?.toFixed(2) || '0.00'}</td>
                    <td>₱{slip.deductions?.toFixed(2) || '0.00'}</td>
                    <td><strong>₱{slip.net_pay?.toFixed(2) || '0.00'}</strong></td>
                    <td>
                      <button
                        className="btn btn-primary btn-small"
                        onClick={() => downloadPayslip(selectedRun, slip.employee_id)}
                      >
                        PDF
                      </button>
                    </td>
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

export default PayrollPage;
