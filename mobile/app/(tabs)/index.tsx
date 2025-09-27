import React, { useState, useEffect, useCallback } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Alert,
} from "react-native";
import { router } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Icon from "react-native-vector-icons/MaterialIcons";
import { ApiService } from "@/services/ApiServices";
import { AttendanceRecord, AttendanceStats } from "../../types";
import { commonStyles } from "../../styles/commonStyles";
import { dashboardStyles as styles } from "../../styles/dashboardStyles";

interface QuickAction {
  title: string;
  icon: string;
  route: string;
  color: string;
}

const DashboardScreen: React.FC = () => {
  const [userName, setUserName] = useState<string>("Student");
  const [recentAttendance, setRecentAttendance] = useState<AttendanceRecord[]>(
    []
  );
  const [stats, setStats] = useState<AttendanceStats>({
    totalSessions: 0,
    presentCount: 0,
    attendancePercentage: 0,
  });
  const [refreshing, setRefreshing] = useState<boolean>(false);

  const loadDashboardData = useCallback(async (): Promise<void> => {
    try {
      const name = await AsyncStorage.getItem("userName");
      setUserName(name || "Student");

      const [attendanceData, statsData] = await Promise.all([
        ApiService.getRecentAttendance(),
        ApiService.getAttendanceStats(),
      ]);

      setRecentAttendance(attendanceData.slice(0, 5));
      setStats(statsData);
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Could not load dashboard data";
      Alert.alert("Error", message);
    }
  }, []);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const onRefresh = useCallback(async (): Promise<void> => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  }, [loadDashboardData]);

  const handleLogout = (): void => {
    Alert.alert("Logout", "Are you sure you want to logout?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Logout",
        onPress: async () => {
          await AsyncStorage.clear();
          router.replace("/login");
        },
      },
    ]);
  };

  const getAttendanceColor = (percentage: number): string => {
    if (percentage >= 80) return "#28a745";
    if (percentage >= 60) return "#ffc107";
    return "#dc3545";
  };

  const quickActions: QuickAction[] = [
    {
      title: "Mark Attendance",
      icon: "check-circle",
      route: "/attendance",
      color: "#28a745",
    },
    {
      title: "View Analytics",
      icon: "analytics",
      route: "/analytics",
      color: "#17a2b8",
    },
    {
      title: "My Profile",
      icon: "person",
      route: "/profile",
      color: "#6f42c1",
    },
  ];

  return (
    <ScrollView
      style={commonStyles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={commonStyles.header}>
        <View style={styles.welcomeSection}>
          <Text style={styles.welcomeText}>Welcome back,</Text>
          <Text style={styles.nameText}>{userName} 👋</Text>
          <Text style={styles.tagline}>
            Ready to learn something new today?
          </Text>
        </View>
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Icon name="logout" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{stats.totalSessions}</Text>
          <Text style={styles.statLabel}>Total Sessions</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{stats.presentCount}</Text>
          <Text style={styles.statLabel}>Present</Text>
        </View>
        <View style={styles.statCard}>
          <Text
            style={[
              styles.statNumber,
              { color: getAttendanceColor(stats.attendancePercentage) },
            ]}
          >
            {stats.attendancePercentage}%
          </Text>
          <Text style={styles.statLabel}>Attendance</Text>
        </View>
      </View>

      <View style={styles.quickActionsContainer}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <View style={styles.actionsGrid}>
          {quickActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.actionCard, { borderLeftColor: action.color }]}
              onPress={() => router.push(action.route as any)}
            >
              <Icon name={action.icon} size={32} color={action.color} />
              <Text style={styles.actionTitle}>{action.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.recentAttendanceContainer}>
        <Text style={styles.sectionTitle}>Recent Attendance</Text>
        {recentAttendance.map((record, index) => (
          <View key={index} style={styles.attendanceCard}>
            <View style={styles.attendanceDate}>
              <Text style={styles.dateText}>
                {new Date(record.timestamp).toLocaleDateString()}
              </Text>
              <Text style={styles.timeText}>
                {new Date(record.timestamp).toLocaleTimeString()}
              </Text>
            </View>
            <View style={styles.attendanceStatus}>
              <View
                style={[
                  styles.statusDot,
                  {
                    backgroundColor: record.liveness_passed
                      ? "#28a745"
                      : "#dc3545",
                  },
                ]}
              />
              <Text style={styles.statusText}>
                {record.liveness_passed ? "Present" : "Absent"}
              </Text>
            </View>
          </View>
        ))}
      </View>
    </ScrollView>
  );
};

export default DashboardScreen;
