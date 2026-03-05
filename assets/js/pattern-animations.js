/**
 * 20 Coding Interview Pattern Animations - Vanilla JS Port
 * Ported from coding-patterns-v2.jsx
 */

const T = {
  bg: "#03050d",
  surface: "#070c1a",
  card: "#0b1120",
  border: "#131d35",
  borderHover: "#1f2e55",
  text: "#c8d4f0",
  muted: "#3a4a70",
  faint: "#1a2240",
  colors: {
    cyan: "#00e5ff", cyanDim: "#00e5ff22",
    violet: "#b47fff", violetDim: "#b47fff22",
    green: "#00ff9f", greenDim: "#00ff9f22",
    amber: "#ffb700", amberDim: "#ffb70022",
    rose: "#ff4d7d", roseDim: "#ff4d7d22",
    sky: "#4da8ff", skyDim: "#4da8ff22",
    teal: "#00ffd5", tealDim: "#00ffd522",
    orange: "#ff7340", orangeDim: "#ff734022",
    lime: "#b3ff4d", limeDim: "#b3ff4d22",
    pink: "#ff5df0", pinkDim: "#ff5df022",
  }
};

class PatternAnimator {
  constructor(containerId, renderFn, interval) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const color = el.dataset.color || T.colors.cyan;
    let tick = 0;
    let paused = false;
    let speed = interval || 600;

    // Build UI
    const svgWrap = document.createElement('div');
    svgWrap.style.cssText = 'min-height:80px;';

    const statusEl = document.createElement('div');
    statusEl.style.cssText = 'font-family:monospace;font-size:11px;color:' + T.muted + ';text-align:center;margin:6px 0;min-height:18px;';

    const controls = document.createElement('div');
    controls.style.cssText = 'display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:8px;';

    const makeBtn = (label, col) => {
      const b = document.createElement('button');
      b.innerHTML = label;
      b.style.cssText = 'background:' + T.card + ';border:1px solid ' + col + '55;color:' + col + ';border-radius:6px;padding:4px 12px;font-size:11px;font-weight:700;font-family:monospace;cursor:pointer;';
      return b;
    };

    const playBtn = makeBtn('⏸ Pause', color);
    playBtn.onclick = () => { paused = !paused; playBtn.innerHTML = paused ? '▶ Play' : '⏸ Pause'; };

    const stepBtn = makeBtn('⏭ Step', T.muted);
    stepBtn.onclick = () => { paused = true; playBtn.innerHTML = '▶ Play'; tick++; render(); };

    const resetBtn = makeBtn('↺ Reset', T.muted);
    resetBtn.onclick = () => { tick = 0; render(); };

    const sel = document.createElement('select');
    sel.style.cssText = 'background:' + T.card + ';border:1px solid ' + T.border + ';color:' + color + ';border-radius:4px;padding:3px 6px;font-size:10px;cursor:pointer;font-family:monospace;margin-left:auto;';
    [['0.5×', 1200], ['1×', 600], ['2×', 300], ['3×', 150]].forEach(([lbl, ms]) => {
      const o = document.createElement('option');
      o.value = ms; o.textContent = lbl;
      if (ms === (interval || 600)) o.selected = true;
      sel.appendChild(o);
    });
    sel.onchange = () => { speed = +sel.value; };

    const tickEl = document.createElement('span');
    tickEl.style.cssText = 'font-family:monospace;font-size:10px;color:' + T.muted + ';';

    controls.append(playBtn, stepBtn, resetBtn, sel, tickEl);
    el.append(svgWrap, statusEl, controls);

    function render() {
      svgWrap.innerHTML = renderFn(tick, color);
      tickEl.textContent = 'step ' + tick;
    }

    render();
    setInterval(() => { if (!paused) { tick++; render(); } }, speed);
  }
}


/* 1 · Sliding Window */
function renderSlidingWindow(tick, color) {
  const arr = [4, 2, 7, 1, 9, 3, 5, 8, 6];
  const K = 3;
  const maxSteps = arr.length - K + 1;
  const w = tick % (maxSteps + 1);
  const wi = Math.min(w, maxSteps - 1);
  const sum = arr.slice(wi, wi + K).reduce((a, b) => a + b, 0);
  const maxSum = Math.max(...Array.from({ length: maxSteps }, (_, i) => arr.slice(i, i + K).reduce((a, b) => a + b, 0)));
  const pct = sum / maxSum;

  let boxes = arr.map((v, i) => {
    const inW = i >= wi && i < wi + K;
    const isEdge = i === wi || i === wi + K - 1;
    const boxCol = inW ? (isEdge ? `${color}30` : `${color}18`) : T.surface;
    const strokeCol = inW ? color : T.border;
    const strokeWidth = inW ? 1.8 : 1;
    const shadow = inW ? `style="filter: drop-shadow(0 0 4px ${color}80); transition: all 0.35s ease;"` : 'style="transition: all 0.35s ease;"';

    return `
      <g ${shadow}>
        <rect x="${8 + i * 27}" y="14" width="23" height="23" rx="4"
          fill="${boxCol}" stroke="${strokeCol}" stroke-width="${strokeWidth}"/>
        <text x="${19.5 + i * 27}" y="30" text-anchor="middle"
          fill="${inW ? color : T.muted}" font-size="11" font-weight="${inW ? '700' : '400'}"
          font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 72" width="100%">
      <defs>
        <linearGradient id="sw-win" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="${color}" stop-opacity="0.05"/>
          <stop offset="50%" stop-color="${color}" stop-opacity="0.15"/>
          <stop offset="100%" stop-color="${color}" stop-opacity="0.05"/>
        </linearGradient>
      </defs>
      ${boxes}
      <rect x="${6 + wi * 27}" y="11" width="${K * 27 + 2}" height="29" rx="5"
        fill="url(#sw-win)" stroke="${color}" stroke-width="2"
        style="transition: x 0.35s cubic-bezier(0.4,0,0.2,1); filter: drop-shadow(0 0 8px ${color}50);"/>
      <rect x="8" y="46" width="243" height="6" rx="3" fill="${T.border}"/>
      <rect x="8" y="46" width="${243 * pct}" height="6" rx="3" fill="${color}"
        style="transition: width 0.35s ease; filter: drop-shadow(0 0 4px ${color});"/>
      <text x="8" y="63" fill="${T.muted}" font-size="9" font-family="monospace">sum</text>
      <text x="130" y="63" text-anchor="middle" fill="${color}" font-size="9" font-family="monospace" font-weight="700">${sum}</text>
      <text x="251" y="63" text-anchor="end" fill="${T.muted}" font-size="9" font-family="monospace">max ${maxSum}</text>
    </svg>`;
}

/* 2 · Two Pointers */
function renderTwoPointers(tick, color) {
  const arr = [1, 3, 5, 6, 8, 11, 14, 17];
  const target = 19;
  const steps = [];
  {
    let l = 0, r = arr.length - 1;
    while (l < r) { steps.push([l, r]); const s = arr[l] + arr[r]; if (s === target) break; else if (s < target) l++; else r--; }
    steps.push([l, steps[steps.length - 1][1]]);
  }

  const si = tick % (steps.length + 2);
  const [left, right] = steps[Math.min(si, steps.length - 1)];
  const s = arr[left] + arr[right];
  const found = s === target;

  let elements = arr.map((v, i) => {
    const isL = i === left, isR = i === right;
    const col = found && (isL || isR) ? T.colors.green : isL ? color : isR ? T.colors.violet : T.border;
    const active = isL || isR;
    return `
      <g style="transition:all 0.4s ease">
        <rect x="${6 + i * 30}" y="14" width="26" height="23" rx="4"
          fill="${active ? `${col}25` : T.surface}" stroke="${col}" stroke-width="${active ? 2 : 1}"
          style="${active ? `filter:drop-shadow(0 0 6px ${col})` : ""}"/>
        <text x="${19 + i * 30}" y="30" text-anchor="middle" fill="${active ? col : T.muted}"
          font-size="10" font-weight="${active ? "700" : "400"}" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 72" width="100%">
      ${elements}
      <g style="transition:all 0.4s ease">
        <text x="${19 + left * 30}" y="48" text-anchor="middle" fill="${color}" font-size="9" font-family="monospace">L</text>
        <line x1="${19 + left * 30}" y1="38" x2="${19 + left * 30}" y2="44" stroke="${color}" stroke-width="1.5"/>
      </g>
      <g style="transition:all 0.4s ease">
        <text x="${19 + right * 30}" y="48" text-anchor="middle" fill="${T.colors.violet}" font-size="9" font-family="monospace">R</text>
        <line x1="${19 + right * 30}" y1="38" x2="${19 + right * 30}" y2="44" stroke="${T.colors.violet}" stroke-width="1.5"/>
      </g>
      <text x="130" y="64" text-anchor="middle" fill="${found ? T.colors.green : T.muted}" font-size="9" font-family="monospace">
        ${found ? `✓ ${arr[left]} + ${arr[right]} = ${target}` : `${arr[left]} + ${arr[right]} = ${s}  (target: ${target})`}
      </text>
    </svg>`;
}

/* 3 · Fast & Slow Pointers */
function renderFastSlow(tick, color) {
  const N = 9, cycleStart = 3;
  const next = i => i === N - 1 ? cycleStart : i + 1;
  const slow = tick % N;
  const fast = (tick * 2) % N;
  const met = slow === fast && tick > 2;
  const cx = i => 130 + 90 * Math.cos((i / N) * 2 * Math.PI - Math.PI / 2);
  const cy = i => 36 + 28 * Math.sin((i / N) * 2 * Math.PI - Math.PI / 2);

  let edges = Array.from({ length: N }).map((_, i) => {
    const isCycle = i >= cycleStart;
    return `<line x1="${cx(i)}" y1="${cy(i)}" x2="${cx(next(i))}" y2="${cy(next(i))}"
      stroke="${isCycle ? `${color}40` : T.border}" stroke-width="${isCycle ? 2 : 1.5}" marker-end="url(#fs-arr)"/>`;
  }).join('');

  let nodes = Array.from({ length: N }).map((_, i) => {
    const isSlow = i === slow, isFast = i === fast, both = isSlow && isFast;
    const col = both ? T.colors.green : isSlow ? T.colors.amber : isFast ? color : T.border;
    const isCycle = i >= cycleStart;
    return `
      <g style="transition:all 0.2s ease">
        <circle cx="${cx(i)}" cy="${cy(i)}" r="${isSlow || isFast ? 13 : 11}"
          fill="${isSlow || isFast ? `${col}25` : T.surface}"
          stroke="${isCycle ? `${color}60` : col}" stroke-width="${isSlow || isFast ? 2.5 : 1}"
          style="${isSlow || isFast ? `filter:drop-shadow(0 0 7px ${col})` : ""}"/>
        <text x="${cx(i)}" y="${cy(i) + 4}" text-anchor="middle" fill="${isSlow || isFast ? col : T.muted}"
          font-size="9" font-weight="700" font-family="monospace">${i}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 75" width="100%">
      <defs>
        <marker id="fs-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="${T.muted}"/>
        </marker>
      </defs>
      ${edges}
      ${nodes}
      <circle cx="12" cy="66" r="5" fill="${T.colors.amber}30" stroke="${T.colors.amber}" stroke-width="1.5"/>
      <text x="20" y="70" fill="${T.colors.amber}" font-size="8" font-family="monospace">slow×1</text>
      <circle cx="70" cy="66" r="5" fill="${color}30" stroke="${color}" stroke-width="1.5"/>
      <text x="78" y="70" fill="${color}" font-size="8" font-family="monospace">fast×2</text>
      <text x="150" y="70" fill="${met ? T.colors.green : T.muted}" font-size="9" font-family="monospace" font-weight="700">
        ${met ? "⚡ CYCLE DETECTED" : "hunting..."}
      </text>
    </svg>`;
}

/* 4 · Merge Intervals */
function renderMergeIntervals(tick, color) {
  const phase = tick % 8;
  const showMerged = phase >= 4;
  const raw = [[1, 4], [2, 6], [8, 10], [9, 12]];
  const merged = [[1, 6], [8, 12]];
  const scale = v => 10 + v * 19;
  const rowCols = [color, T.colors.violet, T.colors.amber, T.colors.teal];

  let intervals = "";
  if (!showMerged) {
    intervals = raw.map((iv, i) => `
      <g style="animation:fadeIn 0.4s ease">
        <rect x="${scale(iv[0])}" y="${12 + i * 11}" width="${scale(iv[1]) - scale(iv[0])}" height="9" rx="2"
          fill="${rowCols[i]}25" stroke="${rowCols[i]}" stroke-width="1.5"/>
        <text x="${(scale(iv[0]) + scale(iv[1])) / 2}" y="${20 + i * 11}" text-anchor="middle"
          fill="${rowCols[i]}" font-size="7" font-family="monospace">[${iv[0]},${iv[1]}]</text>
      </g>`).join('');
  } else {
    intervals = merged.map((iv, i) => `
      <g style="animation:fadeIn 0.4s ease">
        <rect x="${scale(iv[0])}" y="${20 + i * 22}" width="${scale(iv[1]) - scale(iv[0])}" height="14" rx="3"
          fill="${color}30" stroke="${color}" stroke-width="2"
          style="filter:drop-shadow(0 0 6px ${color}60)"/>
        <text x="${(scale(iv[0]) + scale(iv[1])) / 2}" y="${31 + i * 22}" text-anchor="middle"
          fill="${color}" font-size="9" font-weight="700" font-family="monospace">[${iv[0]},${iv[1]}]</text>
      </g>`).join('');
  }

  return `
    <svg viewBox="0 0 260 72" width="100%">
      <line x1="10" y1="62" x2="240" y2="62" stroke="${T.border}" stroke-width="1"/>
      ${[0, 2, 4, 6, 8, 10, 12].map(v => `
        <g>
          <line x1="${scale(v)}" y1="60" x2="${scale(v)}" y2="64" stroke="${T.muted}" stroke-width="1"/>
          <text x="${scale(v)}" y="71" text-anchor="middle" fill="${T.muted}" font-size="7" font-family="monospace">${v}</text>
        </g>`).join('')}
      ${intervals}
      <text x="130" y="10" text-anchor="middle" fill="${showMerged ? color : T.muted}" font-size="8" font-family="monospace">
        ${showMerged ? "✓ merged — 4→2 intervals" : "sort by start, then sweep →"}
      </text>
    </svg>`;
}

/* 5 · Cyclic Sort */
function renderCyclicSort(tick, color) {
  const base = [3, 1, 5, 2, 4];
  const N = base.length;
  const cycleLen = N + 3;
  const step = tick % cycleLen;

  const simulate = () => {
    const a = [...base]; let i = 0; const swaps = [];
    while (i < a.length) {
      const ci = a[i] - 1;
      if (a[i] !== a[ci]) { swaps.push({ arr: [...a], i, ci, type: "swap" });[a[i], a[ci]] = [a[ci], a[i]]; }
      else { swaps.push({ arr: [...a], i, ci: i, type: "ok" }); i++; }
    }
    swaps.push({ arr: [...a], i: a.length, ci: -1, type: "done" });
    return swaps;
  };
  const frames = simulate();
  const frame = frames[Math.min(step, frames.length - 1)];

  let nodes = frame.arr.map((v, idx) => {
    const correct = v === idx + 1;
    const isI = idx === frame.i;
    const isTarget = frame.type === "swap" && idx === frame.ci;
    const col = frame.type === "done" ? T.colors.green
      : correct ? T.colors.green
        : isI ? color
          : isTarget ? T.colors.amber
            : T.muted;
    return `
      <g style="transition:all 0.3s ease">
        <rect x="${16 + idx * 46}" y="14" width="38" height="32" rx="6"
          fill="${col}15" stroke="${col}" stroke-width="${isI || isTarget ? 2.5 : 1}"
          style="${isI || isTarget ? `filter:drop-shadow(0 0 8px ${col})` : "drop-shadow(0 0 2px #0005)"}"/>
        <text x="${35 + idx * 46}" y="34" text-anchor="middle" fill="${col}"
          font-size="14" font-weight="700" font-family="monospace">${v}</text>
        <text x="${35 + idx * 46}" y="54" text-anchor="middle" fill="${T.muted}"
          font-size="8" font-family="monospace">→${idx + 1}</text>
      </g>`;
  }).join('');

  let swapArrow = "";
  if (frame.type === "swap") {
    swapArrow = `<path d="M${35 + frame.i * 46} 12 C${35 + frame.i * 46} 2,${35 + frame.ci * 46} 2,${35 + frame.ci * 46} 12"
      fill="none" stroke="${T.colors.amber}" stroke-width="2" stroke-dasharray="4 2"
      marker-end="url(#cs-swap)" opacity="0.8"/>`;
  }

  return `
    <svg viewBox="0 0 260 68" width="100%">
      <defs>
        <marker id="cs-swap" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
          <path d="M0,0 L5,2.5 L0,5 Z" fill="${T.colors.amber}"/>
        </marker>
      </defs>
      ${nodes}
      ${swapArrow}
    </svg>`;
}

/* 6 · In-place Reversal */
function renderInPlaceReversal(tick, color) {
  const N = 6;
  const step = tick % (N + 3);
  const revCount = Math.min(step, N);
  const nx = i => 22 + i * 40;
  const Y = 32;

  let fArrows = Array.from({ length: N - 1 }).map((_, i) => i >= revCount - 1 ? `
    <line x1="${nx(i) + 14}" y1="${Y}" x2="${nx(i + 1) - 14}" y2="${Y}"
      stroke="${T.colors.violet}" stroke-width="1.5" marker-end="url(#rev-f)" opacity="0.5"/>` : "").join('');

  let bArrows = Array.from({ length: revCount }).map((_, i) => i > 0 ? `
    <line x1="${nx(i) - 14}" y1="${Y - 3}" x2="${nx(i - 1) + 14}" y2="${Y - 3}"
      stroke="${color}" stroke-width="2" marker-end="url(#rev-b)"
      style="filter:drop-shadow(0 0 3px ${color}80)"/>` : "").join('');

  let nodes = Array.from({ length: N }).map((_, i) => {
    const rev = i < revCount;
    const isCurr = i === revCount - 1;
    const col = rev ? color : T.colors.violet;
    return `
      <g style="transition:all 0.35s ease">
        <circle cx="${nx(i)}" cy="${Y}" r="13" fill="${col}20" stroke="${col}"
          stroke-width="${isCurr ? 2.5 : 1.5}" style="${isCurr ? `filter:drop-shadow(0 0 8px ${col})` : "none"}"/>
        <text x="${nx(i)}" y="${Y + 4}" text-anchor="middle" fill="${col}"
          font-size="10" font-weight="700" font-family="monospace">${i + 1}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 65" width="100%">
      <defs>
        <marker id="rev-f" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
          <path d="M0,0 L5,2.5 L0,5 Z" fill="${T.colors.violet}"/>
        </marker>
        <marker id="rev-b" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
          <path d="M0,0 L5,2.5 L0,5 Z" fill="${color}"/>
        </marker>
      </defs>
      ${fArrows}
      ${bArrows}
      ${nodes}
      <text x="${nx(Math.max(0, revCount - 1))}" y="53" text-anchor="middle" fill="${color}" font-size="8" font-family="monospace">curr</text>
      <text x="${nx(Math.max(0, revCount - 2))}" y="53" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">prev</text>
      <text x="130" y="63" text-anchor="middle" fill="${revCount >= N ? T.colors.green : T.muted}" font-size="9" font-family="monospace">
        ${revCount >= N ? "✓ reversed in O(1) space" : "reversing pointers..."}
      </text>
    </svg>`;
}

/* 7 · Tree BFS */
function renderTreeBFS(tick, color) {
  const pos = [[130, 10], [75, 32], [185, 32], [45, 58], [105, 58], [155, 58], [215, 58]];
  const edges = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]];
  const levels = [0, 1, 1, 2, 2, 2, 2];
  const bfsOrder = [0, 1, 2, 3, 4, 5, 6];
  const n = (tick % (bfsOrder.length + 3));
  const visited = new Set(bfsOrder.slice(0, Math.min(n, bfsOrder.length)));
  const levelCols = [color, T.colors.violet, T.colors.amber];

  let edgeElements = edges.map(([a, b], i) => `
    <line x1="${pos[a][0]}" y1="${pos[a][1] + 11}" x2="${pos[b][0]}" y2="${pos[b][1] - 11}"
      stroke="${visited.has(b) ? `${levelCols[levels[b]]}80` : T.border}" stroke-width="${visited.has(b) ? 2 : 1}"
      style="transition:stroke 0.3s"/>`).join('');

  let nodeElements = pos.map(([x, y], i) => {
    const lit = visited.has(i);
    const orderNum = bfsOrder.indexOf(i);
    const isLast = (n - 1) === orderNum && n > 0 && n <= bfsOrder.length;
    const col = lit ? levelCols[levels[i]] : T.muted;
    return `
      <g style="transition:all 0.3s ease">
        <circle cx="${x}" cy="${y + 11}" r="${isLast ? 14 : 11}"
          fill="${lit ? `${col}25` : T.surface}" stroke="${col}"
          stroke-width="${isLast ? 2.5 : lit ? 2 : 1}"
          style="${isLast ? `filter:drop-shadow(0 0 10px ${col})` : lit ? `filter:drop-shadow(0 0 4px ${col})` : "none"}"/>
        <text x="${x}" y="${y + 15}" text-anchor="middle" fill="${lit ? col : T.muted}"
          font-size="9" font-weight="700" font-family="monospace">${i}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 72" width="100%">
      ${edgeElements}
      ${nodeElements}
      <text x="130" y="72" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">
        Level 0:<tspan fill="${levelCols[0]}"> ${bfsOrder.filter(n => levels[n] === 0 && visited.has(n)).join(",")}</tspan>
        &nbsp;&nbsp;L1:<tspan fill="${levelCols[1]}"> ${bfsOrder.filter(n => levels[n] === 1 && visited.has(n)).join(",")}</tspan>
        &nbsp;&nbsp;L2:<tspan fill="${levelCols[2]}"> ${bfsOrder.filter(n => levels[n] === 2 && visited.has(n)).join(",")}</tspan>
      </text>
    </svg>`;
}

/* 8 · Tree DFS */
function renderTreeDFS(tick, color) {
  const pos = [[130, 10], [75, 32], [185, 32], [45, 58], [105, 58], [155, 58], [215, 58]];
  const edges = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]];
  const dfsOrder = [0, 1, 3, 4, 2, 5, 6];
  const n = (tick % (dfsOrder.length + 3));
  const visitedSeq = dfsOrder.slice(0, Math.min(n, dfsOrder.length));
  const visited = new Set(visitedSeq);

  let edgeElements = edges.map(([a, b], i) => `
    <line x1="${pos[a][0]}" y1="${pos[a][1] + 11}" x2="${pos[b][0]}" y2="${pos[b][1] - 11}"
      stroke="${visited.has(a) && visited.has(b) ? `${color}60` : T.border}" stroke-width="1.5"
      style="transition:stroke 0.3s"/>`).join('');

  let nodeElements = pos.map(([x, y], i) => {
    const seq = visitedSeq.indexOf(i);
    const lit = visited.has(i);
    const isLast = visitedSeq[visitedSeq.length - 1] === i && visitedSeq.length > 0;
    return `
      <g style="transition:all 0.3s ease">
        <circle cx="${x}" cy="${y + 11}" r="${isLast ? 14 : 11}"
          fill="${lit ? `${color}20` : T.surface}" stroke="${lit ? color : T.muted}"
          stroke-width="${isLast ? 2.5 : lit ? 2 : 1}"
          style="${isLast ? `filter:drop-shadow(0 0 10px ${color})` : lit ? `filter:drop-shadow(0 0 4px ${color}80)` : "none"}"/>
        ${lit ? `<text x="${x}" y="${y + 15}" text-anchor="middle" fill="${color}"
          font-size="9" font-weight="700" font-family="monospace">${seq + 1}</text>` :
        `<text x="${x}" y="${y + 15}" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">${i}</text>`}
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 72" width="100%">
      ${edgeElements}
      ${nodeElements}
      <text x="130" y="72" text-anchor="middle" fill="${T.muted}" font-size="9" font-family="monospace">
        preorder: <tspan fill="${color}">${visitedSeq.join(" → ")}</tspan>
      </text>
    </svg>`;
}

/* 9 · Two Heaps */
function renderTwoHeaps(tick, color) {
  const stream = [8, 3, 10, 1, 6, 14, 4, 9, 7];
  const n = Math.min((tick % (stream.length + 2)) + 1, stream.length);
  const sorted = [...stream.slice(0, n)].sort((a, b) => a - b);
  const half = Math.floor(sorted.length / 2);
  const maxH = sorted.slice(0, sorted.length % 2 === 0 ? half : half + 1);
  const minH = sorted.slice(sorted.length % 2 === 0 ? half : half + 1);
  const median = sorted.length % 2 === 0
    ? (maxH[maxH.length - 1] + minH[0]) / 2
    : maxH[maxH.length - 1];

  const renderStack = (vals, col, x) => vals.slice(-4).map((v, i, a) => {
    const isTop = i === a.length - 1;
    const y = 50 - i * 13;
    return `
      <g style="transition:all 0.4s ease">
        <rect x="${x - 16}" y="${y - 8}" width="32" height="14" rx="3"
          fill="${col}${isTop ? "35" : "18"}" stroke="${col}" stroke-width="${isTop ? 2 : 1}"
          style="${isTop ? `filter:drop-shadow(0 0 6px ${col})` : ""}"/>
        <text x="${x}" y="${y + 4}" text-anchor="middle" fill="${isTop ? col : `${col}aa`}"
          font-size="9" font-weight="${isTop ? "700" : "400"}" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 72" width="100%">
      <text x="60" y="10" text-anchor="middle" fill="${color}" font-size="8" font-family="monospace" letter-spacing="1">MAX-HEAP</text>
      <text x="200" y="10" text-anchor="middle" fill="${T.colors.violet}" font-size="8" font-family="monospace" letter-spacing="1">MIN-HEAP</text>
      ${renderStack(maxH, color, 60)}
      ${renderStack(minH, T.colors.violet, 200)}
      <line x1="130" y1="8" x2="130" y2="58" stroke="${T.border}" stroke-width="1" stroke-dasharray="4 3"/>
      <rect x="105" y="26" width="50" height="22" rx="5"
        fill="${T.colors.green}15" stroke="${T.colors.green}" stroke-width="1.5"
        style="filter:drop-shadow(0 0 6px ${T.colors.green}60)"/>
      <text x="130" y="34" text-anchor="middle" fill="${T.muted}" font-size="7" font-family="monospace">MEDIAN</text>
      <text x="130" y="44" text-anchor="middle" fill="${T.colors.green}"
        font-size="10" font-weight="700" font-family="monospace">${median}</text>
      <text x="130" y="68" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">
        small:${maxH.length}  large:${minH.length}
      </text>
    </svg>`;
}

/* 10 · Subsets */
function renderSubsets(tick, color) {
  const phase = tick % (4 * 3);
  const step = Math.min(Math.floor(phase / 3), 3);
  const allSteps = [[[]], [[], [1]], [[], [1], [2], [1, 2]], [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]];
  const subsets = allSteps[step];
  const prevSubsets = step > 0 ? allSteps[step - 1] : [];
  const newOnes = subsets.filter(s => !prevSubsets.some(ps => ps.join() === s.join()));

  let subsetsElements = subsets.map((s, i) => {
    const isNew = step > 0 && newOnes.some(n => n.join() === s.join());
    const col = isNew ? color : T.muted;
    const label = s.length === 0 ? "∅" : `{${s.join(",")}}`;
    const numRows = Math.ceil(subsets.length / 5);
    const perRow = Math.ceil(subsets.length / numRows);
    const row = Math.floor(i / perRow);
    const colIdx = i % perRow;
    const w = label.length * 6 + 10;
    const x = 14 + colIdx * (248 / perRow);
    const y = 18 + row * 20;
    return `
      <g style="animation:${isNew ? "fadeIn 0.3s ease" : "none"}">
        <rect x="${x}" y="${y}" width="${w}" height="15" rx="3"
          fill="${isNew ? `${col}25` : `${T.muted}10`}" stroke="${col}" stroke-width="${isNew ? 1.5 : 0.8}"
          style="${isNew ? `filter:drop-shadow(0 0 4px ${col})` : ""}"/>
        <text x="${x + w / 2}" y="${y + 10}" text-anchor="middle" fill="${col}"
          font-size="8" font-weight="${isNew ? "700" : "400"}" font-family="monospace">${label}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 68" width="100%">
      <text x="130" y="11" text-anchor="middle" fill="${T.muted}" font-size="9" font-family="monospace">
        ${step === 0 ? "start: {∅}" : step === 1 ? "add 1 →" : "add " + (step === 2 ? 2 : 3) + " →"} <tspan fill="${color}">${subsets.length} subsets</tspan>
      </text>
      ${subsetsElements}
    </svg>`;
}

/* 11 · Modified Binary Search */
function renderBinarySearch(tick, color) {
  const arr = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 81, 90];
  const target = 38;
  const steps = [];
  {
    let lo = 0, hi = arr.length - 1;
    while (lo <= hi) { const m = Math.floor((lo + hi) / 2); steps.push({ lo, hi, m }); if (arr[m] === target) break; else if (arr[m] < target) lo = m + 1; else hi = m - 1; }
  }
  const si = tick % (steps.length + 2);
  const { lo, hi, m } = steps[Math.min(si, steps.length - 1)];
  const found = arr[m] === target;

  let boxes = arr.map((v, i) => {
    const inRange = i >= lo && i <= hi;
    const isMid = i === m;
    const col = found && isMid ? T.colors.green : isMid ? T.colors.amber : inRange ? color : T.border;
    return `
      <g style="transition:all 0.4s ease">
        <rect x="${3 + i * 21}" y="16" width="19" height="18" rx="3"
          fill="${inRange ? `${col}20` : T.surface}" stroke="${col}" stroke-width="${isMid ? 2.5 : inRange ? 1.5 : 0.8}"
          opacity="${inRange ? 1 : 0.3}"
          style="${isMid ? `filter:drop-shadow(0 0 8px ${col})` : ""}"/>
        <text x="${12.5 + i * 21}" y="29" text-anchor="middle" fill="${inRange ? col : T.muted}"
          font-size="8" font-weight="${isMid ? "700" : "400"}" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 65" width="100%">
      ${boxes}
      <rect x="${2 + lo * 21}" y="13" width="${(hi - lo + 1) * 21}" height="24" rx="4"
        fill="none" stroke="${color}" stroke-width="1" stroke-dasharray="5 3" opacity="0.4"
        style="transition:all 0.4s ease"/>
      <line x1="${12.5 + m * 21}" y1="38" x2="${12.5 + m * 21}" y2="43" stroke="${T.colors.amber}" stroke-width="1.5"
        style="transition:all 0.4s ease"/>
      <text x="${12.5 + m * 21}" y="52" text-anchor="middle" fill="${T.colors.amber}" font-size="8" font-family="monospace"
        style="transition:all 0.4s ease">mid</text>
      <text x="130" y="63" text-anchor="middle"
        fill="${found ? T.colors.green : T.muted}" font-size="9" font-family="monospace">
        ${found ? `✓ found ${target} at index ${m}` : `arr[${m}]=${arr[m]} ${arr[m] < target ? "&lt;" : "&gt;"} ${target}`}
      </text>
    </svg>`;
}

/* 12 · Top K Elements */
function renderTopKElements(tick, color) {
  const stream = [3, 7, 1, 9, 2, 8, 4, 6, 5];
  const K = 3;
  const n = Math.min((tick % (stream.length + 2)) + 1, stream.length);
  const seen = stream.slice(0, n);
  const heap = [...seen].sort((a, b) => a - b).slice(-K);
  const latest = seen[seen.length - 1];

  let streamNodes = stream.map((v, i) => {
    const inHeap = heap.includes(v) && i < n;
    const isLatest = i === n - 1 && i < stream.length;
    const processed = i < n;
    const col = isLatest ? T.colors.amber : inHeap ? T.colors.green : processed ? T.muted : T.border;
    return `
      <g>
        <circle cx="${14 + i * 26}" cy="22" r="${isLatest ? 11 : 9}"
          fill="${col}20" stroke="${col}" stroke-width="${isLatest ? 2 : 1}"
          style="${isLatest ? `filter:drop-shadow(0 0 7px ${col})` : ""};transition:all 0.3s"/>
        <text x="${14 + i * 26}" y="26" text-anchor="middle" fill="${col}" font-size="9"
          font-weight="${isLatest ? "700" : "400"}" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  let heapNodes = heap.map((v, i) => {
    const cx = [130, 90, 170][i] || 130;
    const cy = i === 0 ? 50 : 64;
    const col = i === 0 ? T.colors.rose : color;
    return `
      <g>
        <circle cx="${cx}" cy="${cy}" r="11" fill="${col}25" stroke="${col}" stroke-width="${i === 0 ? 2.5 : 1.5}"
          style="${i === 0 ? `filter:drop-shadow(0 0 6px ${col})` : ""};transition:all 0.4s"/>
        <text x="${cx}" y="${cy + 4}" text-anchor="middle" fill="${col}" font-size="10"
          font-weight="700" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 70" width="100%">
      <text x="6" y="11" fill="${T.muted}" font-size="8" font-family="monospace">input stream</text>
      ${streamNodes}
      <text x="6" y="42" fill="${T.muted}" font-size="8" font-family="monospace">min-heap (K=${K})</text>
      ${heap.length > 0 ? `<line x1="130" y1="50" x2="90" y2="64" stroke="${T.border}" stroke-width="1"/>` : ""}
      ${heap.length > 1 ? `<line x1="130" y1="50" x2="170" y2="64" stroke="${T.border}" stroke-width="1"/>` : ""}
      ${heapNodes}
      <text x="220" y="56" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">top-${K}:</text>
      <text x="220" y="67" text-anchor="middle" fill="${T.colors.green}" font-size="8"
        font-weight="700" font-family="monospace">[${[...heap].sort((a, b) => b - a).join(",")}]</text>
    </svg>`;
}

/* 13 · K-way Merge */
function renderKWayMerge(tick, color) {
  const lists = [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]];
  const flat = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  const n = Math.min((tick % (flat.length + 3)), flat.length);
  const merged = flat.slice(0, n);
  const listCols = [color, T.colors.violet, T.colors.amber, T.colors.teal];

  let listElements = lists.map((lst, li) => `
    <g>
      ${lst.map((v, vi) => {
    const used = merged.includes(v);
    const isFront = !used && lst.slice(0, vi).every(x => merged.includes(x));
    const col = listCols[li];
    return `
          <g style="transition:opacity 0.3s">
            <rect x="${4 + vi * 20}" y="${4 + li * 15}" width="18" height="12" rx="2"
              fill="${used ? `${col}08` : `${col}25`}" stroke="${used ? `${col}30` : col}"
              stroke-width="${isFront ? 2 : 1}" opacity="${used ? 0.3 : 1}"
              style="${isFront ? `filter:drop-shadow(0 0 5px ${col})` : ""}"/>
            <text x="${13 + vi * 20}" y="${13 + li * 15}" text-anchor="middle"
              fill="${used ? `${col}50` : col}" font-size="8" font-family="monospace">${v}</text>
          </g>`;
  }).join('')}
    </g>`).join('');

  let mergedElements = merged.map((v, i) => {
    const li = lists.findIndex(l => l.includes(v));
    const col = listCols[li];
    const isLatest = i === merged.length - 1;
    return `
      <g style="transition:all 0.3s">
        <rect x="${84 + i * 14}" y="14" width="13" height="13" rx="2"
          fill="${col}25" stroke="${col}" stroke-width="${isLatest ? 2 : 1}"
          style="${isLatest ? `filter:drop-shadow(0 0 5px ${col})` : ""}"/>
        <text x="${90.5 + i * 14}" y="24" text-anchor="middle" fill="${col}"
          font-size="8" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  let heapElements = lists.map((lst, li) => {
    const front = lst.find(v => !merged.includes(v));
    if (!front) return "";
    const col = listCols[li];
    return `
      <g>
        <circle cx="${90 + li * 28}" cy="58" r="10" fill="${col}25" stroke="${col}" stroke-width="1.5"
          style="filter:drop-shadow(0 0 4px ${col}60)"/>
        <text x="${90 + li * 28}" y="${62}" text-anchor="middle" fill="${col}"
          font-size="9" font-weight="700" font-family="monospace">${front}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 70" width="100%">
      ${listElements}
      <text x="86" y="10" fill="${T.muted}" font-size="8" font-family="monospace">merged →</text>
      ${mergedElements}
      <text x="130" y="40" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">heap fronts</text>
      ${heapElements}
    </svg>`;
}

/* 14 · Topological Sort */
function renderTopoSort(tick, color) {
  const nodes = ["A", "B", "C", "D", "E", "F"];
  const edges = [["A", "C"], ["B", "C"], ["B", "D"], ["C", "E"], ["D", "E"], ["E", "F"]];
  const order = ["A", "B", "C", "D", "E", "F"];
  const pos = { A: [22, 38], B: [22, 60], C: [90, 28], D: [90, 60], E: [168, 44], F: [240, 44] };
  const n = tick % (order.length + 3);
  const done = new Set(order.slice(0, Math.min(n, order.length)));

  let edgeElements = edges.map(([a, b], i) => {
    const resolved = done.has(a) && done.has(b);
    return `<line x1="${pos[a][0] + 11}" y1="${pos[a][1]}" x2="${pos[b][0] - 11}" y2="${pos[b][1]}"
      stroke="${resolved ? color : T.muted}" stroke-width="${resolved ? 2 : 1}"
      marker-end="${resolved ? "url(#tp-b)" : "url(#tp-a)"}"
      style="${resolved ? `filter:drop-shadow(0 0 3px ${color})` : ""}"
      opacity="${resolved ? 1 : 0.4}"/>`;
  }).join('');

  let nodeElements = nodes.map(nd => {
    const [x, y] = pos[nd];
    const isDone = done.has(nd);
    const ready = !isDone && edges.filter(([_, b]) => b === nd).every(([a]) => done.has(a));
    const col = isDone ? color : ready ? T.colors.amber : T.muted;
    return `
      <g style="transition:all 0.35s ease">
        <circle cx="${x}" cy="${y}" r="12" fill="${col}20" stroke="${col}"
          stroke-width="${isDone ? 2.5 : ready ? 2 : 1}"
          style="${isDone ? `filter:drop-shadow(0 0 7px ${col})` : ready ? `drop-shadow(0 0 5px ${col})` : ""}"/>
        <text x="${x}" y="${y + 4}" text-anchor="middle" fill="${col}"
          font-size="10" font-weight="700" font-family="monospace">${nd}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 72" width="100%">
      <defs>
        <marker id="tp-a" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
          <path d="M0,0 L5,2.5 L0,5 Z" fill="${T.muted}"/>
        </marker>
        <marker id="tp-b" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto">
          <path d="M0,0 L5,2.5 L0,5 Z" fill="${color}"/>
        </marker>
      </defs>
      ${edgeElements}
      ${nodeElements}
      <text x="130" y="72" text-anchor="middle" fill="${T.muted}" font-size="9" font-family="monospace">
        order: <tspan fill="${color}">${[...done].join(" → ")}</tspan>
      </text>
    </svg>`;
}

/* 15 · Prefix Sum */
function renderPrefixSum(tick, color) {
  const arr = [3, 1, 4, 1, 5, 9, 2, 6];
  const step = Math.min(tick % (arr.length + 3), arr.length);
  const prefix = [0, ...arr.map((_, i) => arr.slice(0, i + 1).reduce((a, b) => a + b, 0))];
  const qL = 2, qR = 5;
  const showQuery = step === arr.length || step >= arr.length;

  let numsElements = arr.map((v, i) => `
    <g>
      <rect x="${4 + i * 31}" y="12" width="28" height="14" rx="3"
        fill="${T.surface}" stroke="${T.border}" stroke-width="1"/>
      <text x="${18 + i * 31}" y="23}" text-anchor="middle" fill="${T.muted}" font-size="9" font-family="monospace">${v}</text>
    </g>`).join('');

  let prefixElements = prefix.map((v, i) => {
    const active = i <= step;
    const isCurr = i === step;
    const inQuery = showQuery && i >= qL && i <= qR + 1;
    const col = inQuery ? T.colors.amber : isCurr ? color : active ? `${color}88` : T.border;
    return `
      <g style="transition:all 0.35s ease">
        <rect x="${4 + i * 29}" y="28" width="27" height="14" rx="3"
          fill="${active ? `${col}20` : T.surface}" stroke="${col}" stroke-width="${isCurr || inQuery ? 2 : active ? 1.5 : 0.8}"
          style="${isCurr ? `filter:drop-shadow(0 0 7px ${col})` : ""}"/>
        <text x="${17.5 + i * 29}" y="${39}" text-anchor="middle" fill="${active ? col : T.muted}"
          font-size="8" font-weight="${isCurr || inQuery ? "700" : "400"}" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 70" width="100%">
      <text x="6" y="10" fill="${T.muted}" font-size="8" font-family="monospace">nums[]</text>
      ${numsElements}
      <text x="6" y="38" fill="${T.muted}" font-size="8" font-family="monospace">prefix[]</text>
      ${prefixElements}
      ${showQuery ? `
        <rect x="${3 + qL * 29}" y="27" width="${(qR - qL + 2) * 29}" height="16" rx="4"
          fill="none" stroke="${T.colors.amber}" stroke-width="2" stroke-dasharray="5 2" opacity="0.7"/>
        <text x="130" y="58" text-anchor="middle" fill="${T.colors.amber}" font-size="9" font-family="monospace">
          sum[${qL}..${qR}] = P[${qR + 1}]-P[${qL}] = ${prefix[qR + 1]}-${prefix[qL]} = ${prefix[qR + 1] - prefix[qL]}
        </text>` : `
        <text x="130" y="58" text-anchor="middle" fill="${T.muted}" font-size="9" font-family="monospace">
          building prefix array... ${step}/${arr.length}
        </text>`}
    </svg>`;
}

/* 16 · Monotonic Stack */
function renderMonotonicStack(tick, color) {
  const arr = [2, 1, 5, 6, 2, 3, 4];
  const n = Math.min(tick % (arr.length + 3), arr.length);
  const stack = [], result = new Array(arr.length).fill(-1);
  for (let i = 0; i < n; i++) {
    while (stack.length && arr[i] > arr[stack[stack.length - 1]]) {
      result[stack.pop()] = arr[i];
    }
    stack.push(i);
  }

  let nodes = arr.map((v, i) => {
    const inStack = stack.includes(i);
    const resolved = result[i] !== -1;
    const isCurr = i === n - 1 && n > 0 && n <= arr.length;
    const col = resolved ? T.colors.green : inStack ? color : i < n ? T.muted : T.border;
    return `
      <g style="transition:all 0.35s ease">
        <rect x="${6 + i * 34}" y="8" width="30" height="26" rx="4"
          fill="${col}18" stroke="${col}" stroke-width="${isCurr ? 2.5 : 1.5}"
          style="${isCurr ? `filter:drop-shadow(0 0 8px ${col})` : ""}"/>
        <text x="${21 + i * 34}" y="26" text-anchor="middle" fill="${col}"
          font-size="14" font-weight="700" font-family="monospace">${v}</text>
        ${resolved ? `<text x="${21 + i * 34}" y="42" text-anchor="middle" fill="${T.colors.green}"
          font-size="8" font-family="monospace">→${result[i]}</text>` : ""}
      </g>`;
  }).join('');

  let stackElements = stack.map((si, pos) => `
    <g>
      <rect x="${42 + pos * 24}" y="48" width="22" height="14" rx="3"
        fill="${color}20" stroke="${color}" stroke-width="${pos === stack.length - 1 ? 2 : 1}"/>
      <text x="${53 + pos * 24}" y="59" text-anchor="middle" fill="${color}"
        font-size="9" font-family="monospace">${arr[si]}</text>
    </g>`).join('');

  return `
    <svg viewBox="0 0 260 70" width="100%">
      ${nodes}
      <text x="6" y="55" fill="${T.muted}" font-size="8" font-family="monospace">stack:</text>
      ${stackElements}
    </svg>`;
}

/* 17 · Union Find */
function renderUnionFind(tick, color) {
  const all = [0, 1, 2, 3, 4, 5];
  const edges = [[0, 1], [2, 3], [1, 2], [4, 5], [3, 4]];
  const n = tick % (edges.length + 3);
  const parent = [...all];
  const find = i => { while (parent[i] !== i) { parent[i] = parent[parent[i]]; i = parent[i]; } return i; };
  for (let i = 0; i < Math.min(n, edges.length); i++) {
    const [a, b] = edges[i];
    const ra = find(a), rb = find(b);
    if (ra !== rb) parent[rb] = ra;
  }
  const roots = [...new Set(all.map(i => find(i)))];
  const compCols = [color, T.colors.violet, T.colors.amber, T.colors.teal];
  const nodeCol = i => compCols[roots.indexOf(find(i))] || T.muted;
  const pos = [[38, 36], [78, 18], [118, 36], [158, 18], [198, 36], [238, 36]];

  let edgeElements = edges.slice(0, Math.min(n, edges.length)).map(([a, b], i) => {
    const col = find(a) === find(b) ? nodeCol(a) : T.muted;
    return `<line x1="${pos[a][0]}" y1="${pos[a][1]}" x2="${pos[b][0]}" y2="${pos[b][1]}"
      stroke="${col}" stroke-width="${find(a) === find(b) ? 2.5 : 1}"
      style="${find(a) === find(b) ? `filter:drop-shadow(0 0 5px ${col}60)` : ""};transition:all 0.4s"/>`;
  }).join('');

  let nodeElements = all.map(i => {
    const col = nodeCol(i);
    const isRoot = find(i) === i;
    return `
      <g style="transition:all 0.4s ease">
        <circle cx="${pos[i][0]}" cy="${pos[i][1]}" r="${isRoot ? 13 : 11}"
          fill="${col}25" stroke="${col}" stroke-width="${isRoot ? 2.5 : 1.5}"
          style="filter:drop-shadow(0 0 ${isRoot ? 6 : 3}px ${col}70)"/>
        <text x="${pos[i][0]}" y="${pos[i][1] + 4}" text-anchor="middle" fill="${col}"
          font-size="10" font-weight="700" font-family="monospace">${i}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 68" width="100%">
      ${edgeElements}
      ${nodeElements}
      <text x="130" y="58" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">
        components: <tspan fill="${color}" font-weight="700">${roots.length}</tspan>
        &nbsp;&nbsp;edges added: <tspan fill="${T.colors.amber}">${Math.min(n, edges.length)}</tspan>
      </text>
    </svg>`;
}

/* 18 · Dynamic Programming */
function renderDP(tick, color) {
  const coins = [1, 2, 5];
  const MAX = 9;
  const dpArr = new Array(MAX + 1).fill(Infinity);
  dpArr[0] = 0;
  for (let i = 1; i <= MAX; i++)for (const c of coins) if (c <= i && dpArr[i - c] + 1 < dpArr[i]) dpArr[i] = dpArr[i - c] + 1;
  const step = Math.min(tick % (MAX + 3), MAX);
  const colForVal = v => v === 0 ? T.muted : v === 1 ? T.colors.green : v === 2 ? T.colors.teal : v === 3 ? color : T.colors.violet;

  let boxes = dpArr.map((v, i) => {
    const active = i <= step;
    const isCurr = i === step;
    const col = isCurr ? T.colors.amber : active ? colForVal(v) : T.border;
    return `
      <g style="transition:all 0.4s ease">
        <rect x="${3 + i * 26}" y="15" width="24" height="26" rx="4"
          fill="${active ? `${col}20` : T.surface}" stroke="${active ? col : T.border}"
          stroke-width="${isCurr ? 2.5 : active ? 1.5 : 0.8}"
          style="${isCurr ? `filter:drop-shadow(0 0 9px ${col})` : active ? `drop-shadow(0 0 3px ${col}60)` : "none"}"/>
        <text x="${15 + i * 26}" y="30" text-anchor="middle"
          fill="${active ? col : T.muted}" font-size="10" font-weight="${active ? "700" : "400"}" font-family="monospace">
          ${active ? (v === Infinity ? "∞" : v) : "·"}
        </text>
        <text x="${15 + i * 26}" y="50" text-anchor="middle" fill="${T.muted}" font-size="7" font-family="monospace">${i}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 70" width="100%">
      <text x="6" y="11" fill="${T.muted}" font-size="8" font-family="monospace">coins: [1,2,5]   target amount →</text>
      ${boxes}
      <text x="130" y="63" text-anchor="middle" fill="${T.muted}" font-size="9" font-family="monospace">
        dp[${step}] = <tspan fill="${T.colors.amber}" font-weight="700">${dpArr[step] === Infinity ? "∞" : dpArr[step]}</tspan>
        ${dpArr[step] < Infinity ? `<tspan fill="${T.muted}"> coin${dpArr[step] !== 1 ? "s" : ""}</tspan>` : ""}
      </text>
    </svg>`;
}

/* 19 · Greedy */
function renderGreedy(tick, color) {
  const arr = [2, 3, 1, 1, 4];
  const phase = tick % (arr.length + 3);
  const step = Math.min(phase, arr.length - 1);
  let maxR = 0;
  const reachable = arr.map((v, i) => { if (i > maxR) return false; maxR = Math.max(maxR, i + v); return true; });

  let boxes = arr.map((v, i) => {
    const isStep = i === step;
    const reach = Math.min(i + v, arr.length - 1);
    const isGoal = i === arr.length - 1;
    const col = isGoal ? T.colors.green : isStep ? T.colors.amber : reachable[i] ? color : T.muted;
    return `
      <g style="transition:all 0.35s ease">
        <rect x="${14 + i * 46}" y="16" width="38" height="32" rx="5"
          fill="${col}18" stroke="${col}" stroke-width="${isStep ? 2.5 : 1.5}"
          style="${isStep ? `filter:drop-shadow(0 0 10px ${col})` : ""}"/>
        <text x="${33 + i * 46}" y="36" text-anchor="middle" fill="${col}"
          font-size="16" font-weight="700" font-family="monospace">${v}</text>
        ${isStep && v > 0 && i < arr.length - 1 ? `
          <path d="M${33 + i * 46} 14 C${33 + i * 46} 4,${33 + reach * 46} 4,${33 + reach * 46} 14"
            fill="none" stroke="${T.colors.amber}" stroke-width="2" stroke-dasharray="4 2" opacity="0.8"/>` : ""}
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 68" width="100%">
      <text x="130" y="10" text-anchor="middle" fill="${T.muted}" font-size="8" font-family="monospace">jump game · greedy max-reach</text>
      ${boxes}
      ${step < arr.length ? `<rect x="14" y="52" width="${Math.min(step + (arr[step] || 0), arr.length - 1) * 46 + 32}" height="4" rx="2"
        fill="${color}" opacity="0.4" style="transition:width 0.35s ease;filter:drop-shadow(0 0 4px ${color})"/>` : ""}
      <text x="130" y="67" text-anchor="middle" fill="${T.colors.green}" font-size="9" font-family="monospace">
        maxReach: ${Math.min(reachable.reduce((acc, r, i) => r ? i : acc, 0) + arr[reachable.reduce((acc, r, i) => r ? i : acc, 0)], arr.length - 1)} ✓
      </text>
    </svg>`;
}

/* 20 · Bit Manipulation */
function renderBits(tick, color) {
  const nums = [4, 1, 2, 1, 2];
  const step = Math.min(tick % (nums.length + 3), nums.length);
  const states = [0];
  for (const n of nums) states.push(states[states.length - 1] ^ n);
  const current = states[step];
  const bin = v => v.toString(2).padStart(4, "0");

  let boxes = nums.map((v, i) => {
    const proc = i < step;
    const isCurr = i === step - 1 && step > 0;
    const col = isCurr ? T.colors.amber : proc ? T.colors.violet : T.border;
    return `
      <g>
        <rect x="${6 + i * 46}" y="10" width="42" height="30" rx="4"
          fill="${col}18" stroke="${col}" stroke-width="${isCurr ? 2.5 : 1}"
          style="${isCurr ? `filter:drop-shadow(0 0 8px ${col})` : ""}"/>
        <text x="${27 + i * 46}" y="24" text-anchor="middle" fill="${col}"
          font-size="8" font-family="monospace" letter-spacing="2">${bin(v)}</text>
        <text x="${27 + i * 46}" y="34" text-anchor="middle" fill="${col}99"
          font-size="8" font-family="monospace">${v}</text>
      </g>`;
  }).join('');

  return `
    <svg viewBox="0 0 260 70" width="100%">
      ${boxes}
      <line x1="6" y1="44" x2="244" y2="44" stroke="${T.border}" stroke-width="1"/>
      <text x="6" y="55" fill="${T.muted}" font-size="8" font-family="monospace">XOR:</text>
      <text x="40" y="55" fill="${current > 0 ? color : T.muted}" font-size="8"
        font-family="monospace" letter-spacing="2" font-weight="700">${bin(current)}</text>
      <rect x="130" y="46" width="120" height="20" rx="4"
        fill="${step >= nums.length ? `${T.colors.green}18` : T.surface}"
        stroke="${step >= nums.length ? T.colors.green : T.border}" stroke-width="1.5"/>
      <text x="190" y="59" text-anchor="middle"
        fill="${step >= nums.length ? T.colors.green : T.muted}" font-size="9"
        font-family="monospace" font-weight="${step >= nums.length ? "700" : "400"}">
        ${step >= nums.length ? `unique = ${current}` : `running XOR = ${current}`}
      </text>
    </svg>`;
}

// Function aliases so generator names work
const renderTopK = renderTopKElements;
const renderBitManip = renderBits;
