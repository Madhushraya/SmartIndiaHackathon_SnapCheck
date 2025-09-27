import { Tabs } from "expo-router";
import Icon from "react-native-vector-icons/MaterialIcons";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={({ route }) => ({
        tabBarIcon: ({
          focused,
          color,
          size,
        }: {
          focused: boolean;
          color: string;
          size: number;
        }) => {
          let iconName: string;

          switch (route.name) {
            case "index":
              iconName = "dashboard";
              break;
            case "attendance":
              iconName = "check-circle";
              break;
            case "analytics":
              iconName = "analytics";
              break;
            case "profile":
              iconName = "person";
              break;
            default:
              iconName = "help";
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: "#007bff",
        tabBarInactiveTintColor: "gray",
        headerStyle: {
          backgroundColor: "#007bff",
        },
        headerTintColor: "white",
        headerTitleStyle: {
          fontWeight: "bold",
        },
      })}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Dashboard",
          headerTitle: "Dashboard",
        }}
      />
      <Tabs.Screen
        name="attendance"
        options={{
          title: "Attendance",
          headerTitle: "Mark Attendance",
        }}
      />
      <Tabs.Screen
        name="analytics"
        options={{
          title: "Analytics",
          headerTitle: "Analytics",
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          headerTitle: "My Profile",
        }}
      />
    </Tabs>
  );
}
