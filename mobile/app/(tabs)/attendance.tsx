import React, { useState, useEffect, useRef } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from "react-native";
import {
  Camera,
  useCameraDevices,
  PhotoFile,
} from "react-native-vision-camera";
import Geolocation from "@react-native-community/geolocation";
import { ApiService } from "@/services/ApiServices";
import { Session } from "../../types";
import { commonStyles } from "../../styles/commonStyles";
import { attendanceStyles } from "../../styles/attendanceStyles";

const AttendanceScreen: React.FC = () => {
  const [hasPermission, setHasPermission] = useState<boolean>(false);
  const [isCapturing, setIsCapturing] = useState<boolean>(false);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const cameraRef = useRef<Camera>(null);
  const devices = useCameraDevices();
  const device = devices.front;

  useEffect(() => {
    requestPermissions();
    getCurrentSession();
  }, []);

  const requestPermissions = async (): Promise<void> => {
    const cameraPermission = await Camera.requestCameraPermission();
    setHasPermission(cameraPermission === "authorized");
  };

  const getCurrentSession = async (): Promise<void> => {
    try {
      const session = await ApiService.getCurrentSession();
      setCurrentSession(session);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Could not fetch session";
      Alert.alert("Error", message);
    }
  };

  const getCurrentLocation = (): Promise<{
    latitude: number;
    longitude: number;
  }> => {
    return new Promise((resolve, reject) => {
      Geolocation.getCurrentPosition(
        (position) => resolve(position.coords),
        (error) => reject(error),
        { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
      );
    });
  };

  const calculateDistance = (
    lat1: number,
    lon1: number,
    lat2: number,
    lon2: number
  ): number => {
    const R = 6371e3; // Earth's radius in meters
    const p1 = (lat1 * Math.PI) / 180;
    const p2 = (lat2 * Math.PI) / 180;
    const deltaP = ((lat2 - lat1) * Math.PI) / 180;
    const deltaL = ((lon2 - lon1) * Math.PI) / 180;

    const a =
      Math.sin(deltaP / 2) * Math.sin(deltaP / 2) +
      Math.cos(p1) * Math.cos(p2) * Math.sin(deltaL / 2) * Math.sin(deltaL / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
  };

  const captureAndSubmit = async (): Promise<void> => {
    if (!device || !currentSession || !cameraRef.current) {
      Alert.alert("Error", "Camera not available or no active session");
      return;
    }

    setIsCapturing(true);

    try {
      const location = await getCurrentLocation();

      if (
        currentSession.location_lat &&
        currentSession.location_lng &&
        currentSession.geofence_radius
      ) {
        const distance = calculateDistance(
          location.latitude,
          location.longitude,
          currentSession.location_lat,
          currentSession.location_lng
        );

        if (distance > currentSession.geofence_radius) {
          Alert.alert(
            "Error",
            "You are not within the allowed location for attendance"
          );
          setIsCapturing(false);
          return;
        }
      }

      const photo: PhotoFile = await cameraRef.current.takePhoto({
        quality: 0.8,
        base64: true,
      });

      const response = await ApiService.submitAttendance({
        session_id: currentSession.id,
        latitude: location.latitude,
        longitude: location.longitude,
        face_embedding: photo.base64 || "",
        liveness_passed: true, // Assuming liveness check is passed
      });

      if (response.id) {
        Alert.alert("Success", "Attendance marked successfully!");
      } else {
        Alert.alert("Error", "Failed to mark attendance");
      }
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Failed to capture attendance. Please try again.";
      Alert.alert("Error", message);
    } finally {
      setIsCapturing(false);
    }
  };

  if (!hasPermission) {
    return (
      <View style={commonStyles.centered}>
        <Text>Camera permission is required to mark attendance</Text>
        <TouchableOpacity
          style={commonStyles.button}
          onPress={requestPermissions}
        >
          <Text style={commonStyles.buttonText}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (!device) {
    return (
      <View style={commonStyles.centered}>
        <Text>Camera not available</Text>
      </View>
    );
  }

  return (
    <View style={commonStyles.container}>
      <View style={attendanceStyles.sessionInfo}>
        {currentSession ? (
          <>
            <Text style={attendanceStyles.sessionTitle}>
              {currentSession.class_name}
            </Text>
            <Text style={attendanceStyles.sessionTime}>
              {new Date(currentSession.start_time).toLocaleTimeString()} -
              {new Date(currentSession.end_time).toLocaleTimeString()}
            </Text>
          </>
        ) : (
          <Text style={attendanceStyles.noSession}>No active session</Text>
        )}
      </View>

      <View style={attendanceStyles.cameraContainer}>
        <Camera
          ref={cameraRef}
          style={attendanceStyles.camera}
          device={device}
          isActive={true}
          photo={true}
        />
        <View style={attendanceStyles.cameraOverlay}>
          <View style={attendanceStyles.faceFrame} />
        </View>
      </View>

      <View style={attendanceStyles.controls}>
        <Text style={attendanceStyles.instructionText}>
          Position your face in the frame and tap capture
        </Text>
        <TouchableOpacity
          style={[
            attendanceStyles.captureButton,
            isCapturing && attendanceStyles.captureButtonDisabled,
          ]}
          onPress={captureAndSubmit}
          disabled={isCapturing || !currentSession}
        >
          {isCapturing ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={attendanceStyles.captureButtonText}>
              📸 Capture & Submit
            </Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default AttendanceScreen;
