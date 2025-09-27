export interface User {
  id: number;
  full_name: string;
  email: string;
  roll_number: string;
  account_id: number;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
  device_uuid: string;
  device_type: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  roll_number: string;
  face_embedding?: string;
  device_uuid: string;
  device_type: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface AttendanceRecord {
  id: number;
  user_id: number;
  session_id: number;
  device_id: number;
  timestamp: string;
  latitude?: number;
  longitude?: number;
  face_embedding?: string;
  liveness_passed: boolean;
}

export interface AttendanceStats {
  totalSessions: number;
  presentCount: number;
  attendancePercentage: number;
}

export interface Session {
  id: number;
  class_name: string;
  start_time: string;
  end_time: string;
  location_lat?: number;
  location_lng?: number;
  geofence_radius?: number;
}

export interface AttendanceSubmission {
  session_id: number;
  latitude?: number;
  longitude?: number;
  face_embedding: string;
  liveness_passed: boolean;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
}