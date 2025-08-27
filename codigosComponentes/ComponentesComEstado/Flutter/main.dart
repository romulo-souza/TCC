// Exemplo de Widget com estado em Flutter: Contador com um botão incrementador

import 'package:flutter/material.dart';
void main() {
  runApp(MaterialApp(home: WidgetComEstado()));
}

class WidgetComEstado extends StatefulWidget {
  const WidgetComEstado({super.key});
  @override
  WidgetComEstadoState createState() => WidgetComEstadoState();
}

class WidgetComEstadoState extends State<WidgetComEstado> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[50],
      appBar: AppBar(title: Text('Widget com Estado')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text('Contador: $_counter'),
            ElevatedButton(
              onPressed: _incrementCounter,
              child: const Text('Incrementar'),
            ), // ElevatedButton
          ], // <Widget>[]
        ), // Column
      ), // Center
    ); // Scaffold
  }
}
