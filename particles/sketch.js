const CONFIG = Object.freeze({
  maxParticles: 2000,
  spawnPerFrame: 11,
  damping: 150,
  viewport: { x0: 0.15, x1: 0.85, y0: 0.2, y1: 0.85 },
});


const STEP_FUNCTIONS = Object.freeze({
  sin:    (v, a) => Math.sin(v * a),
  cos:    (v, a) => Math.cos(v * a),
  tan:    (v, a) => Math.tan(v * a),
  atan:   (v, a) => Math.atan(v * a),
  square: (v, a) => v * v * a,
  linear: (v, a) => v * a,
});

let particles = [];
let stage;

function setup() {
  stage = document.getElementById('canvas-stage');
  const canvas = createCanvas(stage.clientWidth, stage.clientHeight);
  canvas.parent(stage);
  pixelDensity(1);
  strokeWeight(1);
}

function windowResized() {
  resizeCanvas(stage.clientWidth, stage.clientHeight);
}

function draw() {
  const state = Controls.read();

  if (state.fadeEnabled) {
    background(0, state.fadeAmount);
  } else {
    background(0);
  }
  stroke(state.color);

  const fresh = Array.from(
    { length: CONFIG.spawnPerFrame },
    () => p5.Vector.random3D()
  );
  particles = particles.slice(-CONFIG.maxParticles).concat(fresh);

  const stepX = STEP_FUNCTIONS[state.functionX];
  const stepY = STEP_FUNCTIONS[state.functionY];
  const expr  = state.expression;

  const w = width, h = height;
  const { x0, x1, y0, y1 } = CONFIG.viewport;
  const { alpha, damping } = { alpha: state.alpha, damping: CONFIG.damping };

  for (const v of particles) {
    let r;
    try {
      r = expr.evaluate({ x: v.x, y: v.y });
    } catch {
      r = 1;
    }

    v.x += stepX(v.x * r, alpha) / damping;
    v.y += stepY(v.y * r, alpha) / damping;

    point(
      map(v.x, -1, 1, w * x0, w * x1),
      map(v.y, -1, 1, h * y0, h * y1)
    );
  }
}
