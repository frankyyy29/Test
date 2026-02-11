import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://intersys-payroll.onrender.com';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const employeesAPI = {
  create: (data) => api.post('/employees/', data),
  list: () => api.get('/employees/'),
};

export const attendanceAPI = {
  create: (employeeId, data) => api.post(`/attendance/${employeeId}/records`, data),
  list: (employeeId) => api.get(`/attendance/${employeeId}/records`),
};

export const payrollAPI = {
  run: (data) => api.post('/payroll/run', data),
  getRuns: () => api.get('/payroll/runs'),
  getPayslips: (runId) => api.get(`/payroll/runs/${runId}/payslips`),
  downloadPayslip: (runId, employeeId) => 
    api.get(`/payroll/runs/${runId}/payslip/${employeeId}/pdf`, { responseType: 'blob' }),
  downloadSummary: (runId) => 
    api.get(`/payroll/runs/${runId}/export/summary.xlsx`, { responseType: 'blob' }),
};

export default api;
