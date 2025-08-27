// Exemplo de Widget sem estado em Flutter: Exibição estática de texto

import 'package:flutter/material.dart';
void main() {
  runApp(const MaterialApp(home: WidgetSemEstado()));
}

class WidgetSemEstado extends StatelessWidget {
  const WidgetSemEstado({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[50],
      appBar: AppBar(title: const Text('Widget sem Estado')),
      body: const Center(child: Text('Este widget não tem estado')),
    ); // Scaffold
  }
}
