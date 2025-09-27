import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  LoginRequest,
  RegisterRequest,
  AttendanceRecord,
  AttendanceStats,
  Session,
  AttendanceSubmission,
  User
} from '../types';

const API_BASE_URL = 'https://deplorable-endodermal-clarine.ngrok-free.dev/api/v1'; // For Android emulator

async function fetchWithAuth(url: string, options: RequestInit = {}) {
    const token = await AsyncStorage.getItem('userToken');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, { ...options, headers });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Something went wrong');
    }

    return response.json();
}

export const ApiService = {
  async login(credentials: LoginRequest): Promise<{ access_token: string, token_type: string, user: User }> {
    return fetchWithAuth(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },

  async register(userData: RegisterRequest): Promise<User> {
    return fetchWithAuth(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  async getCurrentSession(): Promise<Session> {
    return fetchWithAuth(`${API_BASE_URL}/sessions/current`);
  },

  async submitAttendance(attendanceData: AttendanceSubmission): Promise<AttendanceRecord> {
    return fetchWithAuth(`${API_BASE_URL}/attendance/submit`, {
      method: 'POST',
      body: JSON.stringify(attendanceData),
    });
  },

  async getRecentAttendance(): Promise<AttendanceRecord[]> {
    return fetchWithAuth(`${API_BASE_URL}/attendance/recent`);
  },

  async getAttendanceStats(): Promise<AttendanceStats> {
    return fetchWithAuth(`${API_BASE_URL}/attendance/stats`);
  },
};