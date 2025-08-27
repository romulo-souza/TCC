//Exemplo de componente sem estado em React Native: Exibição estática de texto

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const ComponenteSemEstado = () => {
  return (
    <View style={estilos.container}>
      <Text style={estilos.texto}>Exemplo de componente sem estado</Text>
    </View>
  );
};

const estilos = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#81cdd5ff',
  },
  texto: {
    fontSize: 20,
    color: 'black',
  },
});

export default ComponenteSemEstado;
