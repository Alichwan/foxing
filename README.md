# Antes de empezar:
Estimado ayudante corrector:
Recuerde mantener manos y piernas dentro del juego :D 
# Importante para corregir:
Antes de empezar, para disfrutar al maximo la experiencia de DCCells, por favor descarga la siguiente carpeta (de musica predefinida) y ponla donde se encuentre el juego :D (para no llenar lo servidores de git y si los de google muajajajaja)

https://drive.google.com/drive/folders/19c-I83zfzjOCM4gMMoiC_3Jb8zjKuDWa?usp=sharing

Además me gustaria pedirte si puedes revisar en el modulo elementos en la linea 88 en la funcion animation movement si esta "self.colision_with()", en caso de que no te pido si puedes añadirlo, es para la interaccion con la bomba con los elementos. Solamente chequea si se esta en contacto e imprime bomba. Olvide esta linea por estar tratando de implementar la explosion. 

Para esta tarea realize los siguientes supuestos:
- el jugador ingresa a la save zone y se resguarda en el area que limita dicho objeto
- save zone hace rebotar a los enemigos
- los otros elementos pueden ser atravesados por los enemigos
- save zone no aumenta de tamaño ya que al ir creciendo y subiendo de nivel, cada vez eres mas op y no necesitas de esas ayudas :D 

# Modelacion de la tarea
Dividi la tarea en 3 modulos principales: 
- FrontEnd: Es el modulo principal se encarga de juntar los otros 2 modulos. Cuenta con la clase MainWindow, la cual es encargada de administrar los objetos y realizar correctamente la interfaz, mediannte QGraphicsScene. Esta agrega los elementos, y llama a las funciones de estas para ekecutar todo el juego. Recibe los inputs de teclado y mouse y gatilla las funciones en los elementos del juego. 
- players: Aqui estan creados los jugadores, su movimiento e interaccion entre ellos. los sonidos asociados al golpe con las murallas (en caso de chocar y ser un jugador).
- elementos: Modulo de los objetos que se ven en partida como bombas, vida, safe zone, etc.

# Cosas Realizadas :D
- Entidades:
    Todas las entidades (Enemigos y jugador) cumplen con los requisitos minimos que son pedidos (salvo la constante c de jugador ya que no esta implementada la tienda :C. Pese a ello es facil de añadir mediante una variable o diccionario que guarde los elementos que posee)
- Jugador principal: 
    El jugador principal es capas de subir de nivel, moverse en cualquier direccion tal como es pedido. puede ganar experiencia. posee barra de vida (se ve muy pequeña en el primer nivel) y posee la barra de experiencia. 
- Enemigo:
    El enemigo tiene definido una funcion basica de movimiento, sin embargo no tiene definido conductas especificas al interactuar con el jugador(no es inteligente). No implemente el tiempo de reaccion. Si esta implementado el rango de vision y el rango de escape, es visible en el juego (no lo desactive como referencia) como circulos concentricos. Estos se realiza mediante la llamada a collideswith() de la elipse obteniendo todos los atributos que estan en el radio, si es un jugador, se realiza una accion. Idem con el radio de escape. 
- Colisiones:
    se encuentran definidas todas las colsiones, sin embargo la bomba no explota y elimina objetos (pero si esta definida la interaccion con el objeto) 
- Etapas: 
    Actualmente el juego no cambia de etapa, sin embargo estan todos los elementos definidos para ello. al llegar al tope de nivel el jugador retorna true, esto se chequea constantemente. si es True se toman todos los enemigos y se eliminan. Se resetean las variables de aparicion subiendo en una unidad el nivel en la clase Mainwindow del frontend y se deberia volver a resstablecer las caracteristica de xp al jugador a 0, sin embargo esta ultima funcion no esta implementada. 
- Elementos del juego:
 Como comente anteriormente, estan todos implementados salvo la explosion (tristemente :c) sin embargo se hacia poniendo un timer adicional a la bomba, con esto se seteaba el factor de detonacion y a los 3 segundos se calculaba todos los elementos dentro del radio de explosion de la bomba (si implementado) con colliding items y se eliminaban, 
- Aparicion de enemigos por etapa:
    te pido que revises la funcion, esta correctamente definida y recibe como parametro el nivel en el que se encuentra por lo que al avanzar de nivel deberia ir actualizando los valores para la funcion triangular. Sin embargo no sube de nivel mi juego.
- Puntaje
    esta implementado el puntaje, pero sin los ponderadores solocitados. se suma puntaje por segundo, por eliminar enemigos, por tomar monedas pero no por subir de nivel (no implemente subir de nivel) 
- Tienda
     no pierdas el tiempo, no esta implementado nada de la tienda ni inventario :c
- Interfaz del juego:
    esta todo implementado salvo el boton de tienda, boton de pausa. Boton de salida no funciona :c pero si esta :D
- Representacion Grafica:
    estan los sprites basicos, y estan los sprites de otros objetos animados :D

# Bonus
- Estiloso
    cambio de sprite: los jugadores no fueron reemplazados sin embargo se añadieron a otros objetos
    Fondo: creo que cumpli con ello, salvo el de Qprogressbar de experiencia.
- Desarrollador:
    efectos sonoros: implementado :D, ademas de tener musica de fondo
    busqueda y seleccion de musica: implementado :D
    fullscreen: implementado :D
- Cooperativo:
    implementado :D (salvo pasar de nivel ya que el juego no lo hace) 

# No realizado :c
- La seccion de highscore, la pestaña se abre pero no tiene nada por ahora :c sera agregado en una futura revision del juego :D. Sin embargo era abrir un archivo, ordenarlo y añadirlo a qlabels (que no hice, lo se :c) sin embargo la estructura esta y puedes volver de un lugar a otro :D (ademas que la musica es pegajosa, realmente tienes que descargar sounds y añadirla a la carpeta del juego) 

# Finalmente
Gracias por el esfuerzo de tener los feedbacks, las ayudantias, las ayudas y el esfuerzo que hacen como grupo por hacer de este ramo lo mas ameno posible para nosotros. Te deseo un muy buen final de semestre y que pases todos tus ramos :D 