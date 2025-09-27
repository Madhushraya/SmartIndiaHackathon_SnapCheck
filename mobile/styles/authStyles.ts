import { StyleSheet } from 'react-native';

export const authStyles = StyleSheet.create({
  formContainer: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  tabContainer: {
    flexDirection: 'row',
    marginBottom: 30,
    backgroundColor: '#e9ecef',
    borderRadius: 25,
    padding: 5,
  },
  tab: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
    borderRadius: 20,
  },
  activeTab: {
    backgroundColor: '#007bff',
  },
  tabText: {
    color: '#666',
    fontWeight: '500',
  },
  activeTabText: {
    color: '#fff',
  },
  linkButton: {
    marginTop: 20,
    alignItems: 'center',
  },
  linkText: {
    color: '#007bff',
    fontSize: 16,
  },
});