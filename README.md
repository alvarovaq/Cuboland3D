# Cuboland3D
Cuboland es un juego de construcción en 3D, inspirado en el famoso juego "Minecraft". Mundo repleto de cubos de colores personalizados, para la construcción
de ciudades, figuras, texto y todo lo que nuestra mente pueda imaginar, no existen límites.

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
| Subir  | ESPACE |
| Bajar | SHIFT |
| Traspasar/No Traspasar bloques  | C |

## Inventario

El juego nos permite construir con bloques de colores personalizados. En el inventario tenemos 8 bloques, que podemos acceder a ellos
pulsando el número del dicho bloque. Cuando abrimos el inventario podemos elegir el color de cada bloque, así como la opacidad del mismo.

Cuando se cierra el juego, se guarda el mapa, sin embargo, la configuración del color de cada bloque vuelve a su estado inicial, es por ello
que es importante conocer el cógido de color del bloque, este aparece en la esquina superior de la izquierda.

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

En este caso, cuando el jugador toca un bloque con el color *(100,200,100)* hace que el jugador salte. Si toca un bloque con el color *(200,100,100)*,
el jugador muere y este aparecerá en el punto de inicio.

## Vídeos

En este apartado podeís ver algunos vídeos sobre juego para que podáis tener alguna pequeña idea sobre la dinámica o funcionamiento del mismo.

https://user-images.githubusercontent.com/113897176/198677532-4862b3f1-9102-44f7-bb9b-1d77b3f857ac.mp4

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
