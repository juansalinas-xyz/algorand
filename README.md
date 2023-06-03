# Índice

- [Índice](#índice)
- [¿Qué es una blockchain?](#qué-es-una-blockchain)
- [Bloques](#bloques)
  - [¿Cómo se agregan los bloques a la cadena?](#cómo-se-agregan-los-bloques-a-la-cadena)
- [¿Cómo blockchain beneficia mis aplicaciones?](#cómo-blockchain-beneficia-mis-aplicaciones)
- [Ejemplo de caso de uso: La subasta de Alice y Bob](#ejemplo-de-caso-de-uso-la-subasta-de-alice-y-bob)
- [¿Por qué Algorand?](#por-qué-algorand)
- [Los principios fundacionales](#los-principios-fundacionales)
- [El protocolo de concenso](#el-protocolo-de-concenso)
- [Proof-of-stake vs proof-of-work](#proof-of-stake-vs-proof-of-work)
- [La moneda nativa](#la-moneda-nativa)
- [Fees](#fees)
- [Abierto y sin permisos](#abierto-y-sin-permisos)
- [Descentralización](#descentralización)
- [Forking](#forking)
- [Rendimiento](#rendimiento)
- [Finalidad](#finalidad)
- [Características principales](#características-principales)
- [Herramientas para developers](#herramientas-para-developers)
- [El equipo y el ecosistema](#el-equipo-y-el-ecosistema)
- [Gobernanza](#gobernanza)
- [¿Qué es una dApp?](#qué-es-una-dapp)
- [Smart Contracts](#smart-contracts)
- [¿Por dónde empezar para desarrollar con Algorand?](#por-dónde-empezar-para-desarrollar-con-algorand)
- [AlgoKit](#algokit)
- [Interactuando rapidamente con Algorand](#interactuando-rapidamente-con-algorand)


# ¿Qué es una blockchain?

Una blockchain es un registro distribuido de transacciones que se almacena en múltiples computadoras llamadas nodos, conectados en una red. Los nodos trabajan en conjunto utilizando el mismo software y reglas para verificar las transacciones y agregarlas al registro de forma segura e inmutable.


# Bloques

La palabra "blockchain" se refiere al hecho de que cada registro de transacciones se agrupa en bloques, y cada bloque también contiene una prueba criptográfica del bloque anterior en la cadena. Esto crea un registro público verificable y a prueba de manipulaciones de todas las transacciones, lo que significa que si alguien intenta manipular un registro, en cualquier parte de la cadena, será detectado y rechazado por los nodos de la red.

![enter image description here](https://github.com/jmsalinas88/algorand/blob/main/static/blockchain.png)

Prácticamente, ésto significa que si se trata de manipular incluso un simple registro, en cualquier parte de la cadena, será identificable y rechazado por los nodos de la red. 

## ¿Cómo se agregan los bloques a la cadena?

Cada nodo corre un software que contiene las instrucciones necesarias para verificar las transacciones y la forma de agregar bloques a la cadena. Éstas instrucciones son conocidas como **"protocolo de consenso"**. 

La naturaleza de éstas instrucciones  son uno de los factores diferenciales de las diferentes blockchains. Aprenderemos sobre el protocolo de consenso de Algorand más adelante en ésta guía y cómo difiere de las otras blockchains. 

# ¿Cómo blockchain beneficia mis aplicaciones?

Blockchain es una tecnología de innovación, en cómo transferimos valor. Entonces, si tu aplicación intercambia valor de alguna forma, blockchain podría ser una tecnología candidata para impulsar tu aplicación al siguiente nivel. 

Pero, antes de sumergirnos en blockchain, es importante entender específicamente cómo podría beneficar tu aplicación, de tal forma de diseñar un sistema que al aplicar ésos beneficios no agregue complejidad innecesaria a otras partes de tu aplicación. Esto usualmente se logra pensando en qué componentes poner sobre blockchain ("on-chain") versus fuera de la blockchain ("off-chain") 

A continuación, podemos encontrar algunas características de blockchain que las hace una tecnología atractiva para aplicaciones basadas en la transferencia de valores: 

 - Seguridad
 - Confianza
 - Inmutabilidad
 - Transparencia
 - Bajo costo
 - Eficiencia
 - Integrabilidad
 
 No todas éstas características podrían ser importantes en tu aplicación, posiblemente alguna de ellas podría ser más importante que otras, por lo tanto, la primera pregunta que debes hacerte es **¿Cuál de éstas son importantes para mi caso de uso?**
 
 Si elegís al menos una, entonces la siguiente pregunta sería **¿Ésta falta o es insuficiente en el diseño actual de mi aplicación?**
 
 Si la respuesta a ésta segunda pregunta es "si", a cualquiera de las características que elegiste, entonces estás en el lugar correcto. 
 
Por ejemplo, enviando un pago internacional a través de bancos, usualmente toma días y es de alto costo, porque hay muchos intermediarios involucrados para garantizar que el valor es enviado con seguridad. Costos altos, y generalmente ineficiencia son las características que encontramos ante éste escenario, y blockchain puede mejorarlas, esto no quiere decir que el resto de las características no son importantes. Por ejemplo, no deseamos costos bajos a expensas de la seguridad, pero si sólo la seguridad importara, podríamos decir que el proceso actual es lo suficientemente bueno (asumiendo que confiamos en el banco que hace la transferencia). En éste escenario, blockchain mejora las deficiencias, sin escatimar en otro lugar. 

# Ejemplo de caso de uso: La subasta de Alice y Bob

Alice es una artista talentosa, buscando ampliar su cantidad de fans y su reputación como artista.
Bob es un developer y es amigo de Alice, y la quiere ayudar. 

Alice vende sus obras de arte por medio de las personas conocidas de su entorno, de voz en voz, y a veces por medio de publicidad en redes sociales. Una de sus piezas de arte las vende a $ 100, en promedio, utilizando la técnica actual de venta. Alice cree que podría generar más ganancias si escala y llega a un público más amplio, entonces considera las características importantes para su caso de uso: 

 1. Eficiencia: Pierde mucho tiempo buscando un nuevo comprador, y últimamente no encuentra un público más amplio. 


 2. Confiancia/Transparencia: Alice quiere una audiencia más amplia, pero ella todavía está construyendo su reputación, y necesita una manera para que tanto ella como los compradores potenciales sepan que no están siendo estafados. 


 3. Costo: Le mejor opción de escalar es utilizar un e-commerce, pero sabe que deberá renunciar a una buena parte de lo que gana en comisiones. 

 Mencionamos 4 propiedades de blockchain que podría ayudar a Alice. Alice y Bob analizan juntos considerando los objetivos principales y los aspectos que ella quiere optimizar. Se les ocurre la siguiente idea: 

 Planean tokenizar el arte de Alice como un NFT en la blockchain. Esto les da un punto de entrada al ecosistema blockchain y la posibilidad de planear lo que deseen hacer a continucación. Por lo tanto, construirán una dApp para subastas en la blockchain que permitirá a Alice vender sus obras de arte a un precio fijado por el mercado. 

 La subasta será programada en la blockchain para que todas puedan verla y verificarla. Alice puede garantizar a sus compradores que no serán estafados y viceversa sin necesidad de conocerlos personalmente. Dado que eliminan la necesidad de que en tercero garantice el comercio, pueden reducir sustancialmente las tarifas y Alice puede ganar más dinero. 

 Alice puede concentrarse en publicitar su trabajo a una audiencia tan amplia como quiera a través de sus cuentas de redes sociales o en cualquier otro lugar sin necesidad de reunirse individualmente y generar confianza con compradores potenciales.

 # ¿Por qué Algorand? 

Hasta ahora, hemos discutido la tecnología blockchain y los beneficios que ofrece a las aplicaciones que transfieren valor. Es importante destacar que no todas las blockchains son iguales y no todas ofrecen los mismos beneficios.

Como desarrollador, es importante investigar y elegir una blockchain en la que se pueda confiar para todas las propiedades que promete. En esta sección, describiremos las principales categorías para evaluar al elegir una blockchain y explicaremos cómo se desempeña Algorand en cada una de ellas.

 # Los principios fundacionales

 Algorand fue fundado por Silvio Micali, ganador del premio Turing, co-inventor del protocolo de Prueba de conocimiento cero, y lider de renombre mundial en el campo de la criptografia y la seguridad de la información. 

 Fundó Algorand con la visión de democratizar las finanzas y complir la promesa de blockchain.

 # El protocolo de concenso
 El problema de muchas blockchains es que sacrifican al menos una de las propiedades claves de **seguridad**, **escalabilidad** y **descentralización**, conocido como el trilema de blockchain. Silvio Micali y su equipo resolvieron el trilema de blockchain inventando un nuevo protoloco de concenso llamado **Pure Proof of Stake (PPoS)**, que es el protocolo de concenso que utiliza Algorand. 

 El protocolo de consenso de Algorand funciona mediante la selección de un proponente de bloque y un conjunto de comités de votación en cada ronda de bloque, para proponer un bloque y validar la propuesta, respectivamente. El proponente y los comités se eligen al azar del grupo de todos los poseedores de tokens (las cuentas que tienen algos), y la probabilidad de ser elegido es proporcional a la participación de la cuenta en la red (es decir, cuántos algos tiene en relación con el total). Hay un montón de algoritmos criptográficos realmente geniales que intervienen en este proceso, con nombres elegantes como "funciones aleatorias verificables" y "clasificación criptográfica" para garantizar que la votación sea justa y que el sistema en general sea muy seguro.

 # Proof-of-stake vs proof-of-work

 La mayoría de las blockchains optan por la categoría general de proof-of-stake o proof-of-work.

 En pocas palabras, una blockchain **proof-of-stake** ofrece a los usuarios que tienen más participación (quien tiene más monedas nativa del sistema) más influencia para proponer y validar nuevos bloques, usualmente, por medio de un mecanismo de votos. 

 En **proof-of-work**, los nodos compiten para resolver un problema criptográfico y ofrecen su solución junto con una propuesta de un nuevo bloque (conocido como "minería" y los nodos conocidos como "mineros"). El ganador es recompensado con la moneda del sistema y el bloque forma parte de la blockchain.

 A raíz de que **proof-of-work** requiere que se resuelva un problema criptográfico antes que nadie, el poder de cómputo juega un papel importante en la estrategia para ganar. Esto ha generado muchos debates sobre el consumo de energía y sus efectos sobre el clima. 

 La mayoría de los protocolos **proof-of-stake**, incluyendo el protocolo de Algorand, no requiere grandes cantidades de energía para producir un bloque. 

 # La moneda nativa
 Cada blockchain tiene su propia moneda nativa que juega un papel fundamental para incentivar el buen comportamiento de la red. La moneda nativa de Algorand se llama **Algo**. 

 Si posee Algos, puede registrarse para participar en el consenso, lo que significa que participará en el proceso de propuesta y votación de nuevos bloques. 

 Algo también actua como un token de utilidad. Cuando esta creando una aplicación necesita algos para pagar las tarifas de transacción y como saldo mínimo si desea almacenar datos en la blockchain. 

 El costo de estas tarifas y saldos mínimos es muy bajo, fracciones de centavo en la mayoría de los casos.

 # Fees
 Los fees son calculados basado en el tamaño de la transacción y un usuario puede elegir aumentar el fee para ayudar a priorizar la aceptación dentro de un bloque cuando el tráfico de la red es alto y los bloques estan constantemente llenos. En Algorand, no existe el concepto de gas fee. 

 El fee mínimo por una transacción son solo 1.000 microAlgos o 0.001 Algos. 

 # Abierto y sin permisos
Anteriormente, comparamos una blockchain que es distribuída con un libro mayor tradicional que es propiedad de una sola entidad. Técnicamente, una blockchain podría ser propiedad de unas pocas entidades y operarlo, pero no sería una blockchain muy buena, ya que un conjunto de nodos centralizados podría manipular fácilmente el estado de la blockchain. 

Algorand es completamente abierto y sin permisos. Cualquiera, en cualquier parte del mundo, que sea propietario de Algos puede participar en el concenso. 

# Descentralización
Si todas las personas que ejecutan nodos son la misma empresa o conjunto de empresas, entonces nos encontramos en una situación similar a la de tener una base de datos centralizada, controlada por unas pocas personas. 

En Algorand, dado que el protocolo es abierto y no requiere permisos, los nodos pueden existir y de hecho, existen en todo el mundo.

# Forking
Forking es cuando una blockchain sufre una bifurcación. A veces, esta bifurcación es intencional, como cuando una parte importante de la comunidad quiere cambiar los fundamentos del protocolo. Otras veces, esta bifurcación es accidental y ocurre cuando dos mineros encuentran un bloque al mismo tiempo. 

Eventualmente, una de las ramas será abandonada, lo que significa que todas las transacciones que ocurrieron desde esa bifurcación en la rama abandonada no serán validadas. Esto tiene implicaciones importantes para la finalización de la transacción. 

Dado que Algorand es proof-of-stake y utiliza un mecanismo de votación para validar los bloques, el forking es imposible. En el peor de los casos, si el comité tarda más en llegar a un acuerdo, la blockchain se relentizará o se detendrá temporalmente. 

# Rendimiento
Desea elegir una blockchain que pueda escalar y manejar un alto rendimiento para que sus usuarios no experimenten largos tiempos de espera al interactuar con su aplicación. 

En Algorand, los bloques se producen cada 3,9 segundos y pueden contener hasta 25.000 transacciones, lo que da como resultado un rendimiento al rededor de 6.000 transacciones por segundo (6.000 TPS)

# Finalidad
En blockchains proof-of-work, dado que el forking es una posibilidad, las transacciones no pueden considerarse definitivas hasta que transcurre un cierto periodo de tiempo. Esto significa que el rendimiento real de este tipo de blockchains se ve afectado por un retrazo en el fin de la transacción. Los procesos posteriores en una aplicación deben tener esto en cuenta para evitar problemas complejos si una transacción termina siendo inválida. 

Como mencionamos anteriormente, Algorand no tiene forking, por lo que las transacciones son definitivas tan pronto como se confirman en un bloque. Un rendimiento de 6.000 TPS significa en realidad 6.000 transacciones finalizadas por segundo. 

# Características principales
Algorand facilita la tokenización, la transferencia y la programación de condiciones en cualquier instrumento de valor. Cree tokens fungibles y no fungibles con una sola transacción (no se requiere progrmar un smart contract). O programe aplicaciones descentralizadas sofisticadas (dApps) con smart contracts de Algorand.

# Herramientas para developers
Los developers pueden escribir smart contracts en Python y pueden usar uno de cuatro SDKs (Python, JavaScript, Golang, Java) para conectar a on-chain assets o aplicaciones. 

# El equipo y el ecosistema
Algorad cuenta con los mejores investigadores y developers del mundo que desarrollan y mejoran activamente el protocolo central de Algorand. La Fundación Algorand invierte mucho en la gobernanza y el crecimiento del ecosistema para promover valor a largo plazo para todos los poseedores de algo. 

# Gobernanza
La Fundación Algorand, una organización sin fines de lucro que lanzó Algorand MainNet, gobierna la red de Algorand y está comprometida a continuar descentralizándola y poner más toma de decisiones en manos de la comunidad de Algorand en general.

# ¿Qué es una dApp?
Aplicaciones descentralizadas o dApps, son aplicaciones que se ejecutan en un entorno de procesamiento descentralizado como una blockchain.
En las secciones anteriores descrubrimos algunas de las propiedades de blockchain y cómo ofrecen opciones para innovar en casos de uso que intercambian elementos de valor. 

Una aplicación de pago, donde los usuarios pueden intercambiar activos entre sí, es una dApp muy simple. En este caso de uso, la transacción de pago es la única lógica on-chain requerida para transferir estos activos. 

Pero, ¿cómo implementamos un escenario más complejo, como por ejemplo, pujar en una subasta?. Podríamos crear un sitio web, hacer que los usuarios inicien sesión, enviarnos sus ofertas y luego emitir la transferencia on-chain del artículo al mejor postor. 

Entonces tendríamos que enviar el monto de la oferta más alta al vendedor y devolver el resto de los fondos al resto de los postores perdedores. El problema con esto, es que sus usuarios tendrían que confiar en que usted no saldrá corriendo con sus ofertas, que el código que escribió para retener fondos es sólido (probablemente sin llegar a verlo), que implementa excelentes prácticas de seguridad para que no lo hackeen, etc. 

Esta implementación pierde por completo la marca de lo que promete blockchain y no estamos mejor usando blockchain que simplemente usando algunos de los sitios de subastas centralizados que ya existen. Si es una empresa de renombre, es probable que la gente confíe en usted, pero si es un desarrollador independiente, que está tratando de construir su reputación desde cero, tendrá dificultades para conseguir usuarios.

 Y en el primer escenario, aún corre mucho riesgo para los atacantes que pueden saber que tiene una gran concentración de fondos. La moraleja de esta historia es que necesitamos una forma de implementar esta lógica de licitación, de forma segura, on-chain.

 Aquí es donde entran en juego los smart contracts. 

 # Smart Contracts
 Los smart contracts son programas lógicos on-chain, que pueden implementar condiciones de transferencia de valor altamente personalizadas. Se pueden componer con todas las demás funciones de capa 1 (incluyendo Algos, NFT, tokens fungibles) para producir aplicaciones descentralizadas potentes y sofisticadas. 

 Volvamos al escenario de licitación de subastas y usemos smart contracts para implementar licitaciones on-chain. Lo que esto significa es que en lugar de enviar ofertas a una cuenta controlada por una entidad centralizada, sujeta a ataques y puntos de falla, podemos enviar esas ofertas a un contrato inteligente, regido por código, que es abierto y verificable públicamente por cualquier persona. Y ese código no cambiará inesperadamente. Eso no significa que no pueda cambiar, pero si lo hace, será público y evidente para los usuarios. Y si no le gusta la idea de que pueda cambiar, incluso puede programarlo desde el principio para restringir ciertos cambios o rechazar todos los cambios en el contrato.

 En resumen, se pasa de confiar en una entidad y esperar que haga lo que prometió, a confiar en el código y saber que hará lo que prometió, independientemente de los diferentes actores involucrados y las diferentes motivaciones que puedan tener.

Es fundamental que el código del smart contract sea revisado y auditado en busca de fallas de seguridad. El código mal escrito que no tiene en cuenta todos los posibles vectores de ataque, por supuesto, no protegerá nada.

# ¿Por dónde empezar para desarrollar con Algorand?
Algorand proporciona una serie de SDKs para desarrollar sobre su blockchain: 

- Python
- JavaScript
- Go
- Java

Los developers podemos escribir smart contracts en Python y podemos usar cualquiera de los cuatro SDK para conectar a on-chain assets o aplicaciones.

Además, existen otras SDK soportadas por la comunidad, como Rust, C# y Dart. 

# AlgoKit
Algorand provee una herramienta para desarrollar smart contracts llamada **AlgoKit**

AlgoKit es la herramienta principal utilizada por la comunidad de Algorand para desarrollar smart contracts en la blockchain de Algorand. Proporciona las capacidades para desarrollar, probar e implementar smart contracts de Algorand en minutos. 

# Interactuando rapidamente con Algorand
A continuación, veremos cómo podemos interactuar con Algorand rápidamente con el SDK para JavaScript. Para lograr esto, construiremos un pequeño proyecto en node. 




