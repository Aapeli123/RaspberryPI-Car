import { StatusBar } from 'expo-status-bar';
import React, {useState, useRef} from 'react';
import { Button, StyleSheet, Text, TextInput, View } from 'react-native';

export default function App() {
  const [connected, setConnected ] = useState(false);
  const [carState, setCarState] = useState("");
  const [ip, setIp] = useState("");
  const [sid, setSid] = useState("");
  const ipRef = useRef(ipRef)
  let websocket;

  function parseMessage(message) {
    if(message === "Car is already being controlled") {
      setConnected(false);
    }
    setCarState(message);
  }

  async function connectToIp(ip) {
    let res = await fetch(`http://${ip}:4242/start`)
    let sid = await res.text();
    if (sid != "Car is already being controlled") {
      setSid(sid);
    }
  }

  async function sendCommand(command) {
    let res = await fetch(`http://${ip}:4242/${command}/${sid}`)
    let status = await res.text();
    setCarState(status);
  }

  async function disconnect() {
    await fetch(`http://${ip}:4242/quit/${sid}`)
    setConnected(false);
  }

  async function connect() {
    await connectToIp(ip);
    setConnected(true);
  }

  function ipChange(text) {
    setIp(text)
  }

  return !connected ? (
    <View style={styles.container}>
      <StatusBar /> 
      <Text>Connect to a car:</Text>
      <TextInput ref={ipRef} onChangeText={ipChange} placeholder="Car ip"></TextInput>
      <Button title="Connect" onPress={connect}></Button>
    </View>
  ) : (
    <View style={styles.container}>
      <Text>Connected to car</Text>
      <Text>{carState}</Text>
      <Button title="Disconnect" onPress={disconnect}></Button>

      <Button title="Go Forwards" onPress={() => sendCommand("f")}></Button>
      <Button title="Go Backwards" onPress={() => sendCommand("b")}></Button>
      <Button title="Turn Left" onPress={() => sendCommand("l")}></Button>
      <Button title="Turn Right" onPress={() => sendCommand("r")}></Button>

      <Button title="Center Steering" onPress={() => sendCommand("c")}></Button>

      <Button title="Start Driving" onPress={() => sendCommand("s")}></Button>
      <Button title="Stop Driving" onPress={() => sendCommand("q")}></Button>



    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
  },
});
