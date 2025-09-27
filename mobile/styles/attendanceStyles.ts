import { StyleSheet } from 'react-native';

export const attendanceStyles = StyleSheet.create({
  sessionInfo: {
    backgroundColor: '#fff',
    padding: 20,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  sessionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  sessionTime: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  noSession: {
    fontSize: 16,
    color: '#999',
  },
  cameraContainer: {
    flex: 1,
    position: 'relative',
  },
  camera: {
    flex: 1,
  },
  cameraOverlay: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  faceFrame: {
    width: 250,
    height: 300,
    borderWidth: 3,
    borderColor: '#007bff',
    borderRadius: 150,
    backgroundColor: 'transparent',
  },
  controls: {
    padding: 20,
    backgroundColor: '#fff',
    alignItems: 'center',
  },
  instructionText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  captureButton: {
    backgroundColor: '#28a745',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    minWidth: 200,
    alignItems: 'center',
  },
  captureButtonDisabled: {
    backgroundColor: '#ccc',
  },
  captureButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});