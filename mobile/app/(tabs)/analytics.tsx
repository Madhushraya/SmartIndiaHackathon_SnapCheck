import React from "react";
import { View, Text } from "react-native";

const AnalyticsScreen: React.FC = () => {
  return (
    <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
      <Text style={{fontSize: 24, fontWeight: 'bold'}}>Analytics</Text>
      <Text style={{fontSize: 16, color: 'gray', marginTop: 10}}>Coming Soon...</Text>
    </View>
  );
};

export default AnalyticsScreen;
