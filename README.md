# A simple mandelbrot/julia renderer

## Controls
| action                            | key(s)        |
| --------------------------------- | ------------- |
| quit                              | q             |
| move around                       | arrow keys    |
| zoom in/out                       | + / -         |
| reset parameters                  | r             |
| pause/resume rendering            | space         |
| increase/decrease rendering depth | . / ,         |
| toggle julia                      | j             |
| move julia constant               | w / a / s / d |

## Example renderings

![Example mandelbrot rendering](./screenshots/mandelbrot.png)

![Example julia rendering](./screenshots/julia.png)

The color distribution for red, green and blue is as follows:

![Color distribution](./color_distribution.png)

The X axis represents the amount of iterations it took for a mandelbrot series to escape the set threshold, depending on the depth.
The Y axis represents the value of the color component (red, green, or blue).
