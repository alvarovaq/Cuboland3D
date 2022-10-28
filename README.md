# Cuboland3D
Cuboland es un juego de construcción en 3D, inspirado en el famoso juego "Minecraft". Mundo repleto de cubos de colores personalizados, para la construcción
de ciudades, figuras, texto y todo lo que nuestra mente pueda imaginar, no existen límites.

<!-- <img src="https://user-images.githubusercontent.com/113897176/191010606-8af305fc-7b08-471e-a613-0300e5b8a8b0.png" width="400"> -->
<img src="https://user-images.githubusercontent.com/113897176/191012000-28ab60ba-dcaa-4c2a-9a77-468856fc665d.png" width="400">

## Inventario

Una de principales ventajas que presenta el juego es que se puede elegir de una manera personaliza los colores y la opacidad de los cubos. Para ello accedemos al inventario presionando la tecla `Q`. Cuando accedemos al inventario podemos ver 8 cubos de colores que podemos ir seleccionando pulsando el número correspondiente de dicho bloque. Para cambiar el color y opacidad del bloque seleccionado, podemos variar las barras de la parte superior derecha y obtener ese color através de un código RGBA.

<img src="https://user-images.githubusercontent.com/113897176/191015293-3b77e7a4-ad4f-4b21-90a1-0034b2925d07.png" width="400">

## Script Player

Unas de las funcionalidades que presenta el juego es poder programar ciertos comportamientos cuando colisionamos con cubos de un determinado color. Para ello debemos entrar en el código y modificar la función `script_update` de la clase `Script_Player` en el archivo `.\cuboland3d.py`. Siguiendo el patrón que se muestra en las siguientes líneas de código y entendiendo un poco el código del juego es facil dar un comportamiento a los cubos. Esto te da un mundo de posibilidades.

``` python
  class Script_Player (Player) :
    def __init__ (self,*args,**kwargs) :
        super().__init__(*args,**kwargs)
        
    def script_update (self) :
        if not self.flying :
          if self.collision_color((100,200,100)) :
            self.jump(2*self.JUMP_SPEED)
          if self.collision_color((200,100,100)) :
            self.death = True
```


``` python
  if self.collision_color(#Color) :
    #Comportamiento
```

En este caso, cuando el jugador toca un bloque con el color *(100,200,100)* (Verde) hace que el jugador de un salto muy alto. Si toca un bloque con el color *(200,100,100)* (Rojo), el jugador muere y este aparecerá en el punto de inicio.

Si que es cierto que no es una gran manera que el jugador tenga que acceder al código y que tenga que conocer una base del código para establecer esos determinados comportamientos. Para un futuro me gustaría crear una nueva ventana donde puedas configurar esos comportamientos de una manera que no tenga que escribir código y no tenga que acceder a los archivos, si no que se haga através de una interfaz del juego.

## Controles

|    | Tecla       |
| ----------|:---------:|
| Salir  | ESC |
| Ver/Ocultar cursor  | E |
| Movimiento hacia alante  | W |
| Movimiento hacia atrás  | S |
| Movimiento hacia la izquierda  | A |
| Movimiento hacia la derecha  | D |
| Saltar | ESPCACE |
| Ver/Ocultar inventario  | Q |
| Volar/No volar  | F |
| Romper  | Clic Izquierdo  |
| Construir  | Clic Derecho |
| Cambiar bloque  | NUMBERS |

Controles cuando el jugador está volando

|    | Tecla       |
| ----------|:---------:|
| Subir  | ESPACE |
| Bajar | SHIFT |
| Traspasar/No Traspasar bloques  | C |

## Vídeos

En este apartado podeís ver algunos vídeos sobre el juego para que podáis tener alguna pequeña idea sobre la dinámica o funcionamiento del mismo.

En el siguiente vídeo podeís ver la base del juego, poder escoger un cubo, elegir su color y su opacidad mediante un código RGBA, colocarlo por el mundo y poder también eliminarlo.

https://user-images.githubusercontent.com/113897176/198677532-4862b3f1-9102-44f7-bb9b-1d77b3f857ac.mp4

En el siguiente vídeo podeís ver de una mejor manera lo ya explicado en el apartado de *Script Player*, en la cual, através de programar unas pequeñas líneas de código podemos dar ciertos comportamientos a los cubos que tengan un determinado color. Podemos ver que al tocar los cubos verdes damos un gran salto, y al tocar los cubos rojos morimos y volvemos al inicio.

https://user-images.githubusercontent.com/113897176/198693001-6fe148e6-fc4a-4ff6-92e2-58c1cc558301.mp4

Incorporando todo esto podemos llegar a hacer grandes construcciones o incluso poder hacer un circuito de parkour como podemos ver en el siguiente vídeo.

https://user-images.githubusercontent.com/113897176/198694720-2df0d947-6fb1-4a50-b445-4342ba0981e4.mp4

## Desarrollo

*Diciembre de 2020 - 3 Semanas*

Este juego ha sido desarrollado por mí con el obejtivo y la motivación de adrentrarme al desarrollo 3D en python. Aunque este no tenga en sí una meta, o diciendolo de otra manera, un objetivo, tienes la libertad de poder crear y diseñar un mundo a nuestra manera en forma de cubos, con el color y la opacidad que deseemos.

Para un futuro me gustaría mejorar el juego poniendo muchas más funcionalidades, como crear más mundos (En esta última versión solo te deja crear un mundo), crear una  interfaz más intuitiva, dar una meta u objetivos, dar la posibilidad de poder jugar Online por red local (LAN), introducir sonidos y mejorar la eficiencia del código.

## Paquetes

*  pyglet

Ejecuta el siguiente comando para instalarlos

`$ pip install -r requirements.txt`
o bien
`$ pip install pyglet`

Ejecuta el archivo *main.py* para iniciar el juego

`$ python main.py`

## Contacto

* Email: alvaro.vaquero.tel@gmail.com
* LinkedIn: https://www.linkedin.com/in/alvaro-vaquero-gimenez/
* Twitter: https://twitter.com/AlvaroVaqGim
* Página Web: https://alvarovaq.github.io
