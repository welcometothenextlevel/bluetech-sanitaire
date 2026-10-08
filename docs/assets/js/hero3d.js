/* Bluetech Sanitaire — hero 3D: brass manifold, quarter-turn valve, gauge, water flowing through clear PE-X lines.
   Tap / click the valve to close or open it. */
import * as THREE from './vendor/three.module.min.js';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

const canvas = document.querySelector('[data-gl]');
const hero = document.querySelector('[data-hero]');
if (canvas && hero) init();

function init() {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const FINE = matchMedia('(pointer: fine)').matches;
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { document.documentElement.classList.add('no-webgl'); return; }
  const mob = () => innerWidth <= 900;
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, mob() ? 1.75 : 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 100);
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(4, 7, 9); scene.add(key);
  const rim = new THREE.DirectionalLight(0x9cc8ff, 1.2); rim.position.set(-6, 2, -6); scene.add(rim);

  /* ---------- materials ---------- */
  const brass = new THREE.MeshStandardMaterial({ color: new THREE.Color('#D2A85E'), metalness: 1, roughness: 0.26 });
  const brassDark = new THREE.MeshStandardMaterial({ color: new THREE.Color('#B48A45'), metalness: 1, roughness: 0.34 });
  const chrome = new THREE.MeshStandardMaterial({ color: new THREE.Color('#EEF2F6'), metalness: 1, roughness: 0.1 });
  const steel = new THREE.MeshStandardMaterial({ color: new THREE.Color('#C3CBD4'), metalness: 0.9, roughness: 0.42 });
  const blue = new THREE.MeshStandardMaterial({ color: new THREE.Color('#2A5598'), metalness: 0.15, roughness: 0.32 });
  const red = new THREE.MeshStandardMaterial({ color: new THREE.Color('#D9452E'), metalness: 0.15, roughness: 0.35 });
  const ink = new THREE.MeshStandardMaterial({ color: new THREE.Color('#0B1626'), metalness: 0.2, roughness: 0.5 });
  const glass = new THREE.MeshPhysicalMaterial({ color: new THREE.Color('#EAF2FB'), metalness: 0, roughness: 0.05, transparent: true, opacity: 0.3, clearcoat: 1, clearcoatRoughness: 0.04, depthWrite: false });

  const waterMats = [];
  function waterMat(len, hot) {
    const m = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false,
      uniforms: { t: { value: 0 }, fill: { value: 0 }, len: { value: len }, hot: { value: hot ? 1 : 0 } },
      vertexShader: 'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
      fragmentShader: [
        'uniform float t;uniform float fill;uniform float len;uniform float hot;varying vec2 vUv;',
        'void main(){',
        ' if(vUv.x>fill)discard;',
        ' float s=fract(vUv.x*len*.55-t*.75);',
        ' float pulse=smoothstep(0.,.06,s)*smoothstep(.42,.06,s);',
        ' float s2=fract(vUv.x*len*1.3-t*1.4);float fine=smoothstep(0.,.05,s2)*smoothstep(.2,.05,s2);',
        ' vec3 base=mix(vec3(.03,.22,.75),vec3(.75,.16,.08),hot);',
        ' vec3 hi=mix(vec3(.42,.85,1.),vec3(1.,.62,.35),hot);',
        ' vec3 col=mix(base,hi,pulse*.9+fine*.25);',
        ' float ring=abs(sin(vUv.y*6.2832));col*=.7+.45*ring;',
        ' float front=smoothstep(fill,fill-.025,vUv.x);',
        ' gl_FragColor=vec4(col,.9*front);',
        ' #include <colorspace_fragment>',
        '}'].join('\n')
    });
    waterMats.push(m);
    return m;
  }

  /* ---------- geometry helpers ---------- */
  const rig = new THREE.Group(); scene.add(rig);
  const assy = new THREE.Group(); rig.add(assy);
  const X = new THREE.Vector3(1, 0, 0);
  function cyl(r, h, seg, mat, axis) {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg), mat);
    if (axis === 'x') m.rotation.z = Math.PI / 2;
    if (axis === 'z') m.rotation.x = Math.PI / 2;
    return m;
  }
  function add(m, x, y, z, parent) { m.position.set(x, y, z); (parent || assy).add(m); return m; }

  // manifold bar (hex brass)
  add(cyl(0.21, 3.7, 6, brass, 'x'), 0, 0, 0).rotation.x = Math.PI / 6;
  // end plug + nut (right)
  add(cyl(0.25, 0.2, 6, brassDark, 'x'), 1.95, 0, 0);
  add(new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), brass), 2.06, 0, 0).rotation.z = -Math.PI / 2;
  // union nut (left)
  add(cyl(0.26, 0.22, 6, brassDark, 'x'), -1.96, 0, 0);
  // ball valve (chrome lathe) on the inlet
  const prof = [[0.15, -0.45], [0.2, -0.43], [0.2, -0.3], [0.27, -0.22], [0.31, -0.06], [0.31, 0.06], [0.27, 0.22], [0.2, 0.3], [0.2, 0.43], [0.15, 0.45]].map(p => new THREE.Vector2(p[0], p[1]));
  const vBody = new THREE.Mesh(new THREE.LatheGeometry(prof, 40), chrome); vBody.rotation.z = Math.PI / 2; add(vBody, -2.6, 0, 0);
  add(cyl(0.24, 0.16, 6, chrome, 'x'), -3.12, 0, 0);
  add(cyl(0.24, 0.16, 6, chrome, 'x'), -2.08, 0, 0);
  add(cyl(0.06, 0.32, 16, chrome), -2.6, 0.38, 0);
  const handle = new THREE.Group(); add(handle, -2.6, 0.54, 0);
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.1, 24), blue); handle.add(hub);
  const lever = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.07, 0.17), blue); lever.position.set(0.5, 0.0, 0); handle.add(lever);
  const leverTip = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.085, 0.075, 24), blue); leverTip.position.set(1.02, 0, 0); handle.add(leverTip);
  const nut = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.06, 6), chrome); nut.position.y = 0.07; handle.add(nut);
  const clickables = [hub, lever, leverTip, vBody];

  // gauge on top of the manifold
  add(cyl(0.065, 0.62, 16, brass), -0.85, 0.42, 0);
  add(cyl(0.11, 0.12, 6, brassDark), -0.85, 0.2, 0);
  const gauge = new THREE.Group(); add(gauge, -0.85, 1.12, 0.02);
  const bezel = new THREE.Mesh(new THREE.TorusGeometry(0.5, 0.06, 16, 64), chrome); gauge.add(bezel);
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.18, 48), steel); body.rotation.x = Math.PI / 2; body.position.z = -0.08; gauge.add(body);
  const face = new THREE.Mesh(new THREE.CircleGeometry(0.47, 64), new THREE.MeshBasicMaterial({ map: dialTexture(), toneMapped: false })); face.position.z = 0.012; gauge.add(face);
  const needle = new THREE.Group(); needle.position.z = 0.03; gauge.add(needle);
  const nd = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.38, 0.012), red); nd.position.y = 0.15; needle.add(nd);
  needle.add(new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.03, 20), ink).rotateX(Math.PI / 2));
  const lensM = new THREE.Mesh(new THREE.CircleGeometry(0.47, 48), new THREE.MeshPhysicalMaterial({ transparent: true, opacity: 0.12, roughness: 0, clearcoat: 1, color: 0xffffff, depthWrite: false })); lensM.position.z = 0.05; gauge.add(lensM);

  // wall brackets
  [-1.45, 1.35].forEach(x => {
    add(new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.9, 0.06), steel), x, -0.1, -0.42);
    add(new THREE.Mesh(new THREE.TorusGeometry(0.24, 0.035, 10, 32, Math.PI * 1.2), steel), x, 0, -0.05).rotation.set(0, Math.PI / 2, -Math.PI * 0.1);
  });

  // pipes: inlet + 5 outlets (clear tube + water core)
  const lines = [];
  function line(points, r, hot, ord) {
    const curve = new THREE.CatmullRomCurve3(points.map(p => new THREE.Vector3(p[0], p[1], p[2])), false, 'centripetal');
    const L = curve.getLength();
    const seg = Math.round(L * (mob() ? 12 : 18));
    const outer = new THREE.Mesh(new THREE.TubeGeometry(curve, seg, r, mob() ? 14 : 20, false), glass);
    const mat = waterMat(L, hot);
    const inner = new THREE.Mesh(new THREE.TubeGeometry(curve, seg, r * 0.6, 10, false), mat);
    inner.renderOrder = 1; outer.renderOrder = 2;
    assy.add(inner); assy.add(outer);
    const o = { mat, fill: 0, target: 0, ord, L };
    lines.push(o);
    return o;
  }
  const inlet = line([[-3.2, 0, 0], [-3.7, 0, 0], [-4.15, 0.35, -0.5], [-4.35, 1.8, -2.2], [-4.4, 5.5, -4.2]].reverse(), 0.15, false, 0);
  const outX = [-1.3, -0.6, 0.1, 0.8, 1.5];
  outX.forEach((x, i) => {
    add(cyl(0.095, 0.34, 16, brass), x, -0.36, 0);
    add(cyl(0.14, 0.13, 6, brassDark), x, -0.56, 0);
    const sp = (i - 2);
    line([[x, -0.62, 0], [x, -1.3, 0], [x + sp * 0.22, -2.5, 0.45], [x + sp * 0.42, -4.4, 0.85], [x + sp * 0.48, -7, 1.0], [x + sp * 0.4, -10, 0.8], [x + sp * 0.32, -13.5, 0.6], [x + sp * 0.26, -19, 0.45], [x + sp * 0.22, -25, 0.35], [x + sp * 0.2, -31, 0.3]], 0.11, i % 2 === 1, i + 1);
  });
  // colour caps on outlets (blue = cold, red = hot)
  outX.forEach((x, i) => add(cyl(0.075, 0.08, 20, i % 2 === 1 ? red : blue), x, -0.17, 0.2).rotation.x = Math.PI / 2);

  assy.position.set(0.45, 0.15, 0);

  /* ---------- dial texture ---------- */
  function dialTexture() {
    const c = document.createElement('canvas'); c.width = c.height = 512;
    const g = c.getContext('2d');
    g.fillStyle = '#fff'; g.beginPath(); g.arc(256, 256, 256, 0, Math.PI * 2); g.fill();
    g.translate(256, 256);
    const a0 = Math.PI * 0.75, span = Math.PI * 1.5;
    g.lineWidth = 16; g.strokeStyle = 'rgba(34,160,107,.35)'; g.beginPath(); g.arc(0, 0, 200, a0 + span * 0.2, a0 + span * 0.4); g.stroke();
    g.strokeStyle = 'rgba(229,87,61,.35)'; g.beginPath(); g.arc(0, 0, 200, a0 + span * 0.85, a0 + span); g.stroke();
    for (let k = 0; k <= 50; k++) {
      const a = a0 + span * k / 50, big = k % 5 === 0;
      g.strokeStyle = '#0B1626'; g.lineWidth = big ? 5 : 2;
      g.beginPath(); g.moveTo(Math.cos(a) * 214, Math.sin(a) * 214); g.lineTo(Math.cos(a) * (big ? 178 : 196), Math.sin(a) * (big ? 178 : 196)); g.stroke();
    }
    g.fillStyle = '#0B1626'; g.font = '500 38px "JetBrains Mono", monospace'; g.textAlign = 'center'; g.textBaseline = 'middle';
    for (let k = 0; k <= 10; k += 2) { const a = a0 + span * k / 10; g.fillText(String(k), Math.cos(a) * 142, Math.sin(a) * 142); }
    g.font = '500 30px "JetBrains Mono", monospace'; g.fillStyle = '#7A879B'; g.fillText('BAR', 0, 92);
    g.font = '700 30px "Cabinet Grotesk", sans-serif'; g.fillStyle = '#2A5598'; g.fillText('BLUETECH', 0, 150);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
    return t;
  }
  // redraw the dial once the webfonts are in
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { face.material.map = dialTexture(); face.material.needsUpdate = true; });

  /* ---------- callouts ---------- */
  const co = {};
  document.querySelectorAll('[data-co]').forEach(el => co[el.getAttribute('data-co')] = el);
  const barTxt = document.querySelector('[data-bar]'), hint = document.querySelector('[data-valve-hint]');
  const anchors = { valve: new THREE.Vector3(-2.6, 0.62, 0), gauge: new THREE.Vector3(-0.35, 1.32, 0.05), mani: new THREE.Vector3(0.45, -0.3, 0.2) };
  const tmp = new THREE.Vector3();
  const verb = FINE ? 'Cliquez' : 'Touchez';

  /* ---------- state ---------- */
  let open = true, handleA = 0, handleTarget = 0, gaugeV = 0, gaugeTarget = 0;
  let introAt = performance.now(), introDone = false;
  let W = 1, H = 1, base = { x: 0, y: 0, s: 1, look: 0.2, camY: 0.5, dive: 10 };
  const ptr = { x: 0, y: 0, tx: 0, ty: 0 };
  let dragRot = 0, dragVel = 0, dragging = false, dx0 = 0, moved = 0;

  function layout() {
    const r = canvas.getBoundingClientRect();
    W = Math.max(1, r.width); H = Math.max(1, r.height);
    renderer.setSize(W, H, false);
    const aspect = W / H;
    camera.aspect = aspect;
    if (aspect > 1.05) {
      camera.fov = 28;
      const halfH = Math.tan(THREE.MathUtils.degToRad(14)) * 14, halfW = halfH * aspect;
      // fit the whole assembly between the end of the headline and the right edge
      let textRight = W * 0.42;
      const inEl = hero.querySelector('[data-hero-in]');
      if (inEl) {
        const rg = document.createRange(), cr = canvas.getBoundingClientRect();
        textRight = 0;
        inEl.querySelectorAll('.hero__t, .hero__p, .hero__b').forEach(el => { rg.selectNodeContents(el); textRight = Math.max(textRight, rg.getBoundingClientRect().right - cr.left); });
        if (!textRight) textRight = W * 0.42;
      }
      const left = Math.min(W * 0.62, textRight + 28), right = W - Math.max(28, W * 0.03);
      const wpp = 2 * halfW / W, bandW = (right - left) * wpp;
      const s = Math.max(0.42, Math.min(0.98, halfH / 4.2, bandW * 0.9 / 6.7));
      const cxWorld = ((left + right) / 2 - W / 2) * wpp;
      base = { x: cxWorld + 0.62 * s, y: 0.05, s, look: 0.2, camY: 0.5, dive: 10.5 * s };
    } else {
      // portrait: keep the horizontal field constant so the manifold fills the width
      camera.fov = Math.min(62, Math.max(28, 2 * THREE.MathUtils.radToDeg(Math.atan(3.1 / 14 / aspect))));
      const halfH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * 14;
      // fit the manifold in the band between the header and the hero text, whatever the phone height
      const inEl = hero.querySelector('[data-hero-in]'), hd = document.querySelector('[data-hd]');
      const top = (hd ? hd.offsetHeight : 66) + 6, textTop = inEl ? inEl.offsetTop + (inEl.firstElementChild ? inEl.firstElementChild.offsetTop : 0) : H * 0.5;
      const band = Math.max(H * 0.22, textTop - top - 8);
      const worldBand = band / H * 2 * halfH;
      const s = Math.max(0.5, Math.min(0.9, worldBand / 2.75));
      const py = top + band * 0.5;
      base = { x: 0.1, y: (0.5 - py / H) * 2 * halfH - 0.62 * s, s, look: 0, camY: 0, dive: 11 * s };
    }
    camera.updateProjectionMatrix();
    rig.scale.setScalar(base.s);
  }
  layout();
  addEventListener('resize', layout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);

  // pointer
  if (FINE) addEventListener('pointermove', e => { ptr.tx = (e.clientX / innerWidth) * 2 - 1; ptr.ty = (e.clientY / innerHeight) * 2 - 1; }, { passive: true });
  canvas.addEventListener('pointerdown', e => { dragging = true; dx0 = e.clientX; moved = 0; dragVel = 0; });
  addEventListener('pointermove', e => {
    if (!dragging) return;
    const dx = e.clientX - dx0; dx0 = e.clientX; moved += Math.abs(dx);
    dragVel = dx * 0.006; dragRot += dragVel;
  }, { passive: true });
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  function hit(e) {
    const r = canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    return ray.intersectObjects(clickables, false).length > 0;
  }
  addEventListener('pointerup', e => {
    if (!dragging) return; dragging = false;
    if (moved < 8 && e.target === canvas && hit(e)) toggle();
  });
  addEventListener('pointercancel', () => { dragging = false; });
  if (FINE) canvas.addEventListener('pointermove', e => { canvas.style.cursor = hit(e) ? 'pointer' : 'grab'; });

  function toggle() {
    open = !open;
    handleTarget = open ? 0 : -Math.PI / 2;
    lines.forEach(l => { if (l.ord > 0) l.target = open ? 1 : 0; });
    gaugeTarget = open ? 3 : 0;
    if (hint) hint.textContent = verb + (open ? ' pour fermer' : ' pour ouvrir');
  }
  if (hint) hint.textContent = verb + ' pour fermer';

  /* ---------- scroll scene: the hero stays pinned while the camera follows the water down the pipes ---------- */
  const stick = hero.querySelector('.hero__stick');
  const heroIn = hero.querySelector('[data-hero-in]'), spec = hero.querySelector('[data-hero-spec]'), cue = hero.querySelector('[data-hero-cue]');
  const calloutWrap = hero.querySelector('[data-callouts]'), meter = hero.querySelector('[data-hero-meter]');
  const story = hero.querySelector('.hero__story'), qs = [...hero.querySelectorAll('[data-q]')];
  const clamp01 = x => Math.min(1, Math.max(0, x));
  const smooth = (a, b, x) => { const t = clamp01((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  function progress() {
    if (RM) return 0;
    const r = hero.getBoundingClientRect();
    return clamp01(-r.top / Math.max(1, r.height - innerHeight));
  }
  let lastP = -1;
  function applyDom(p) {
    if (Math.abs(p - lastP) < 0.0005) return; lastP = p;
    const out = smooth(0.0, 0.16, p);
    heroIn.style.opacity = (1 - out).toFixed(3);
    heroIn.style.transform = out ? 'translate3d(0,' + (-70 * out).toFixed(1) + 'px,0)' : '';
    heroIn.style.visibility = out > 0.99 ? 'hidden' : '';
    if (spec) spec.style.opacity = (1 - smooth(0, 0.08, p)).toFixed(3);
    if (cue) cue.style.opacity = (1 - smooth(0, 0.06, p)).toFixed(3);
    if (calloutWrap) calloutWrap.style.opacity = (1 - smooth(0.02, 0.12, p)).toFixed(3);
    stick.style.setProperty('--veil', (1 - out).toFixed(3));
    let sb = 0;
    qs.forEach((q, i) => {
      const a = i === 0 ? [0.2, 0.32, 0.5, 0.6] : [0.6, 0.72, 0.95, 1.01];
      const inn = smooth(a[0], a[1], p), o = smooth(a[2], a[3], p), v = inn * (1 - o);
      q.style.opacity = v.toFixed(3);
      q.style.transform = 'translate3d(0,' + ((1 - inn) * 44 - o * 44).toFixed(1) + 'px,0)';
      sb = Math.max(sb, v);
    });
    if (story) story.style.setProperty('--sb', sb.toFixed(3));
    if (meter) meter.style.transform = 'scaleY(' + p.toFixed(4) + ')';
  }

  /* ---------- render loop ---------- */
  let visible = true, raf = 0, last = performance.now(), T = 0, ready = false, lastSY = scrollY, boost = 0;
  const ease = (a, b, k) => a + (b - a) * k;
  const easeOut = x => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);

  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    // scrolling pushes the water: the faster you scroll, the faster it flows
    const v = Math.abs(scrollY - lastSY) / Math.max(0.001, dt); lastSY = scrollY;
    boost = ease(boost, Math.min(3, v / 700), 0.08);
    T += dt * (1 + boost * 2.2);
    const it = (now - introAt) / 1000;

    // intro: inlet fills, valve turns, outlets fill, gauge rises
    if (!introDone) {
      handleA = -Math.PI / 2 + Math.PI / 2 * easeOut((it - 1.2) / 0.8);
      inlet.fill = easeOut((it - 0.3) / 1.0);
      lines.forEach(l => { if (l.ord > 0) l.fill = easeOut((it - 2.0 - l.ord * 0.12) / 2.2); });
      gaugeV = 3.0 * easeOut((it - 1.9) / 1.6) + Math.sin(Math.max(0, it - 1.9) * 9) * Math.exp(-Math.max(0, it - 1.9) * 2.5) * 0.35 * (it > 1.9 ? 1 : 0);
      if (it > 2.2) Object.values(co).forEach(el => el.classList.add('is-on'));
      if (it > 5) { introDone = true; lines.forEach(l => l.target = 1); gaugeTarget = 3; }
    } else {
      handleA = ease(handleA, handleTarget, 0.12);
      lines.forEach(l => { const sp = l.target > l.fill ? 0.55 : 1.2; l.fill += Math.sign(l.target - l.fill) * Math.min(Math.abs(l.target - l.fill), dt * sp); });
      gaugeV = ease(gaugeV, gaugeTarget + (open ? Math.sin(T * 7) * 0.03 : 0), 0.06);
    }
    handle.rotation.y = handleA;
    needle.rotation.z = -(-135 + gaugeV * 27) * Math.PI / 180;
    lines.forEach(l => { l.mat.uniforms.fill.value = l.fill; l.mat.uniforms.t.value = RM ? 0 : T * (open || !introDone ? 1 : 0.15); });
    if (barTxt) barTxt.textContent = Math.max(0, gaugeV).toFixed(1).replace('.', ',') + ' bar';

    // scene progress (0 = hero, 1 = end of the pinned scroll)
    const p = progress();
    applyDom(p);
    const a = smooth(0, 0.3, p), b = smooth(0.18, 1, p);
    ptr.x = ease(ptr.x, ptr.tx, 0.05); ptr.y = ease(ptr.y, ptr.ty, 0.05);
    if (!dragging) { dragVel *= 0.94; dragRot += dragVel; dragRot *= 0.985; }
    const intro = easeOut(it / 2.2);
    const sway = RM ? 0 : Math.sin(T * 0.45) * 0.07;
    rig.rotation.y = -0.55 + intro * 0.25 + ptr.x * 0.22 + sway + dragRot + a * 0.22 - b * 0.12;
    rig.rotation.x = 0.12 + ptr.y * 0.08 + a * 0.1;
    rig.position.set(base.x, base.y - (1 - intro) * 0.6, 0);
    camera.position.set(0, base.camY - b * base.dive, 14 - b * 3);
    camera.lookAt(0, base.look - b * (base.dive + 2.2), 0);

    renderer.render(scene, camera);
    if (!ready) { ready = true; canvas.classList.add('is-ready'); }

    // callouts
    if (p < 0.13) for (const k in co) {
      if (!anchors[k]) continue;
      tmp.copy(anchors[k]); assy.localToWorld(tmp); tmp.project(camera);
      const x = (tmp.x * 0.5 + 0.5) * W, y = (-tmp.y * 0.5 + 0.5) * H;
      co[k].style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)' + (co[k].classList.contains('co--l') ? ' translateX(-100%)' : '');
      const cw = co[k].offsetWidth || 0, isL = co[k].classList.contains('co--l');
      const fits = isL ? x - cw > 8 : x + cw < W - 8;
      co[k].style.visibility = (fits && tmp.z < 1 && y > 70 && y < H - 8) ? '' : 'hidden';
    }
    if (visible) raf = requestAnimationFrame(frame);
  }

  const startLoop = () => { if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); } };
  const stopLoop = () => { cancelAnimationFrame(raf); raf = 0; };
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(en => { visible = en[0].isIntersecting && !document.hidden; visible ? startLoop() : stopLoop(); }).observe(hero);
  }
  document.addEventListener('visibilitychange', () => { visible = !document.hidden; visible ? startLoop() : stopLoop(); });
  addEventListener('scroll', () => { if (!raf && visible) startLoop(); }, { passive: true });
  if (RM) introAt = performance.now() - 6000;
  startLoop();
}
