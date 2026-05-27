const Controls = (() => {
  const byId = (id) => document.getElementById(id);

  const el = {
    alpha:          byId('alpha'),
    alphaReadout:   byId('alpha-readout'),
    fadeEnabled:    byId('fade-enabled'),
    fadeAmount:     byId('fade-amount'),
    fadeReadout:    byId('fade-readout'),
    fadeField:      byId('fade-field'),
    functionX:      byId('fn-x'),
    functionY:      byId('fn-y'),
    color:          byId('color'),
    expression:     byId('expression'),
    apply:          byId('apply'),
    errorIndicator: byId('expr-error'),
  };

  const DEFAULT_EXPRESSION = '1';
  let lastValidText     = DEFAULT_EXPRESSION;
  let parsedExpression  = math.parse(DEFAULT_EXPRESSION);

  function applyExpression() {
    const text = el.expression.value.trim() || DEFAULT_EXPRESSION;
    try {
      const candidate = math.parse(text);
      candidate.evaluate({ x: 0, y: 0 });
      parsedExpression = candidate;
      lastValidText = text;
      el.expression.value = text;
    } catch {
      el.expression.value = lastValidText;
      flashError();
    }
  }

  function flashError() {
    el.errorIndicator.classList.add('is-visible');
    setTimeout(() => el.errorIndicator.classList.remove('is-visible'), 1400);
  }

  function wireReadouts() {
    const updateAlpha = () => {
      el.alphaReadout.textContent = parseFloat(el.alpha.value).toFixed(2);
    };
    const updateFade = () => {
      el.fadeReadout.textContent = el.fadeAmount.value;
    };
    el.alpha.addEventListener('input', updateAlpha);
    el.fadeAmount.addEventListener('input', updateFade);
    updateAlpha();
    updateFade();
  }

  function wireApply() {
    el.apply.addEventListener('click', applyExpression);
    el.expression.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        applyExpression();
      }
    });
  }

  function wireFadeToggle() {
    const sync = () => {
      const on = el.fadeEnabled.checked;
      el.fadeAmount.disabled = !on;
      el.fadeField.classList.toggle('is-disabled', !on);
    };
    el.fadeEnabled.addEventListener('change', sync);
    sync();
  }

  function wirePresets() {
    document.querySelectorAll('[data-preset]').forEach((btn) => {
      btn.addEventListener('click', () => {
        el.expression.value = btn.dataset.preset;
        applyExpression();
      });
    });
  }

  wireReadouts();
  wireApply();
  wireFadeToggle();
  wirePresets();

  return {
    read() {
      return {
        alpha:        parseFloat(el.alpha.value),
        fadeEnabled:  el.fadeEnabled.checked,
        fadeAmount:   parseFloat(el.fadeAmount.value),
        functionX:    el.functionX.value,
        functionY:    el.functionY.value,
        color:        el.color.value,
        expression:   parsedExpression,
      };
    },
  };
})();
