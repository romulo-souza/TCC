//Exemplo de componente com estado em React Native: Contador com um botão incrementador

import React, { useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";

const ComponenteComEstado = () => {
  const [counter, setCounter] = useState(0);

  return (
    <View style={estilos.tela}>
      <Text style={estilos.texto}>Contador: {counter}</Text>
      <Button title="Incrementar" onPress={() => setCounter(counter + 1)} />
    </View>
  );
};

const estilos = StyleSheet.create({
  tela: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f0f0f0",
    padding: 20,
  },
  texto: {
    fontSize: 20,
    marginBottom: 10,
    color: "black",
  },
});

export default ComponenteComEstado;
