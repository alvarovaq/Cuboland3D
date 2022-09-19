# Cuboland3D
Cuboland es un juego de construcción en 3D, inspirado en el famoso juego "Minecraft". Mundo repleto de cubos de colores personalizados, para la construcción
de ciudades, figuras, zona de parkour, texto en 3D y todo lo que nuestra mente pueda imaginar, no existen límites.

<!-- <img src="https://user-images.githubusercontent.com/113897176/191010606-8af305fc-7b08-471e-a613-0300e5b8a8b0.png" width="400"> -->
<img src="https://user-images.githubusercontent.com/113897176/191012000-28ab60ba-dcaa-4c2a-9a77-468856fc665d.png" width="400">

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
| Movimiento hacia arriba  | ESPACE |
| Movimiento hacia abajo  | SHIFT |
| Traspasar/No Traspasar bloques  | C |

## Inventario

El juego nos permite construir con bloques de colores personalizados. En el inventario tenemos 8 bloques, que podemos acceder a ellos
pulsando el número del dicho bloque. Cuando abrimos el inventario podemos elegir el color de cada bloque, así como la opacidad del mismo.

Cuando se cierra el juego, se guarda el mapa, sin embargo, la configuración del color de cada bloque vuelve a su estado inicial, por ello
es importante conocer el cógido de color del bloque, este aparece en la esquina superior de la izquierda.

<img src="https://user-images.githubusercontent.com/113897176/191015293-3b77e7a4-ad4f-4b21-90a1-0034b2925d07.png" width="400">

## Script Player

El juego te da la posibilidad de dar acciones a los bloques de un mismo color.
Para ello, el código debe ser modificado en la función *script_update* de la clase *Script_Player*

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

En este caso, cuando el jugador toca un objeto con el color *(100,200,100)*, hace que el jugador salte. Si toca un objeto con el color *(200,100,100)*,
el jugador muere, y este aparecerá en el punto de inicio.

## Ejecución

Para la ejecución del juego, es imprescindible tener instalado en el ordenador las siguientes librerias
1.  pyglet

Ejecutar archivo *main.py*
