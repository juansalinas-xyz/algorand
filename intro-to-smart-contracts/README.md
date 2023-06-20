# Introducción
Los smart contracts son piezas de lógica que residen en la blockchain de Algorand y se pueden invocar de forma remota. Estos contratos son responsables de implementar la lógica asociada a una applicación distribuída. 

Los smart contracts pueden generar transacciones de assets y de pagos, lo cual los habilita a funcionar como una cuenta de Escrow en Algorand. 

Los smart contracts tambien almacenan valores en la blockchain. El almacenamiento puede ser global, local o boxes. 

El almacenamiento local se refiere al almacenamiento de valores en un registro de saldo de cuentas si esa cuenta participa en el contrato.

El almacenamiento global son datos que se almacenan específicamente en la cadena de bloques para el contrato a nivel mundial.

El almacenamiento en boxes también es global y permite que los contratos utilicen segmentos de almacenamiento más grandes.

Al igual que los smart signatures, los smart contracts se escriben en Python usando PyTeal o TEAL y se pueden implementar en la blockchain usando la herramienta de línea de comandos ```goal``` o los SDK. 

El enfoque recomendado para escribir smart contracts es usar el SDK de Python con la biblioteca PyTeal.

# Desarrollando nuestros primeros smart contracts
- [Hello World](https://github.com/jmsalinas88/algorand/tree/main/intro-to-smart-contracts/HelloWorld)
- [Auction](https://github.com/jmsalinas88/algorand/tree/main/intro-to-smart-contracts/Auction) - [Demo](https://www.loom.com/share/54b7620a6acd43b5bab7d8b37a977854) - [App](https://testnet.algoscan.app/app/245358739)
- [AlgoSwap](https://github.com/jmsalinas88/algorand/tree/main/intro-to-smart-contracts/AlgoSwap) - [Demo](https://www.loom.com/share/760ee7d8774d49f899744264c4325482) - [App](https://testnet.algoscan.app/app/245377555)



