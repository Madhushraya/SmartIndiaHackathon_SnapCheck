import React, { useState, useEffect } from "react";
import { View, Text, TouchableOpacity, Alert } from "react-native";
import { router } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Icon from "react-native-vector-icons/MaterialIcons";
import { commonStyles } from "../../styles/commonStyles";
import { profileStyles as styles } from "../../styles/profileStyles";

const ProfileScreen: React.FC = () => {
  const [userName, setUserName] = useState<string>("");
  const [userEmail, setUserEmail] = useState<string>("");

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async (): Promise<void> => {
    try {
      const name = await AsyncStorage.getItem("userName");
      const email = await AsyncStorage.getItem("userEmail");
      setUserName(name || "User");
      setUserEmail(email || "No email");
    } catch {
      Alert.alert("Error", "Failed to load user data.");
    }
  };

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

  return (
    <View style={commonStyles.container}>
      <View style={styles.profileHeader}>
        <View style={styles.avatarContainer}>
          <Icon name="person" size={60} color="#007bff" />
        </View>
        <Text style={styles.userName}>{userName}</Text>
        <Text style={styles.userEmail}>{userEmail}</Text>
      </View>

      <View style={styles.menuContainer}>
        <TouchableOpacity style={styles.menuItem}>
          <Icon name="edit" size={24} color="#666" />
          <Text style={styles.menuText}>Edit Profile</Text>
          <Icon name="chevron-right" size={24} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.menuItem}>
          <Icon name="notifications" size={24} color="#666" />
          <Text style={styles.menuText}>Notifications</Text>
          <Icon name="chevron-right" size={24} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.menuItem}>
          <Icon name="help" size={24} color="#666" />
          <Text style={styles.menuText}>Help & Support</Text>
          <Icon name="chevron-right" size={24} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.menuItem}>
          <Icon name="info" size={24} color="#666" />
          <Text style={styles.menuText}>About</Text>
          <Icon name="chevron-right" size={24} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.menuItem, styles.logoutItem]}
          onPress={handleLogout}
        >
          <Icon name="logout" size={24} color="#dc3545" />
          <Text style={[styles.menuText, styles.logoutText]}>Logout</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default ProfileScreen;
