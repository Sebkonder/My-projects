# Particles

A hobby project exploring generative art through mathematical particle motion. Built with JavaScript, p5.js, and math.js, it draws an animated particle field and lets you experiment with the rules that shape its movement directly in the browser.

Change the movement functions, adjust their shared parameter, or enter a custom expression to see how simple mathematical rules produce different patterns and trails.

## How It Works

Particles begin at random positions and move according to the selected functions. Each frame, the application evaluates the custom expression `r(x, y)` at each particle's position, then uses that value to update its coordinates:

```text
r = expression(x, y)
x = x + stepX(x * r, α) / 150
y = y + stepY(y * r, α) / 150
```

The movement functions and scalar field determine the resulting patterns. A translucent background creates trails by gradually fading earlier frames.

The default settings use `sin(v * α)` for horizontal movement, `cos(v * α)` for vertical movement, `α = 3`, and the constant expression `1`.

## Controls

| Control | Effect |
| --- | --- |
| **Parameter α** | Adjusts the shared parameter of the movement functions from −10 to 10. |
| **Background fade** | Enables fading trails. Turning it off clears the background fully each frame. |
| **Opacity** | Controls how quickly trails disappear: lower values retain them longer. |
| **x-axis / y-axis functions** | Selects the movement rule for each coordinate. |
| **Scalar field r(x, y)** | Accepts a mathematical expression using `x` and `y`. Click **Apply expression** or press **Enter** to apply it. |
| **Preset buttons** | Selects and immediately applies a predefined expression. |
| **Particle ink** | Changes the drawing color. |

### Expression Presets

| Preset | Expression |
| --- | --- |
| Identity | `1` |
| Polynomial | `9*(x+y-5)^2+(1-x-y)^2+5` |
| Coupled trig | `sin(x*y*10)` |
| Gaussian | `exp(-(x^2+y^2))` |

Expressions are parsed with math.js, so powers can be written using `^`. If an expression fails the initial validation, the input returns to the last accepted expression and briefly shows an error indicator.

## Files

| File | Purpose |
| --- | --- |
| [index.html](index.html) | Page layout, styling, control panel, and script loading. |
| [controls.js](controls.js) | Control state, live readouts, expression parsing, validation, and presets. |
| [sketch.js](sketch.js) | Particle creation, movement rules, drawing loop, and canvas resizing. |
| [libraries/](libraries/) | Bundled copies of p5.js and math.js. The current page loads these libraries from a CDN instead. |
| [sketch.properties](sketch.properties) | Processing editor metadata for p5.js mode. |

## Running

Download the project folder and open `index.html` in a web browser. No package installation or build step is required.

Alternatively, serve the folder locally with Python 3. From the `particles` directory, run:

```bash
python -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

The current HTML loads **p5.js 1.9.4**, **math.js 12.4.1**, and Google Fonts from external services, so an internet connection is needed to load those resources.

