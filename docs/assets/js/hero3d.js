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
    const seg = Math.round(L * (mob() ? 18 : 26));
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
    line([[x, -0.62, 0], [x, -1.3, 0], [x + sp * 0.18, -2.3, 0.45], [x + sp * 0.62 + 0.35, -3.7, 1.25], [x + sp * 1.05 + 0.8, -6.4, 2.3]], 0.11, i % 2 === 1, i + 1);
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
  let W = 1, H = 1, base = { x: 0, y: 0, z: 14, s: 1 };
  const ptr = { x: 0, y: 0, tx: 0, ty: 0 };
  let dragRot = 0, dragVel = 0, dragging = false, dx0 = 0, moved = 0;

  function layout() {
    const r = canvas.getBoundingClientRect();
    W = Math.max(1, r.width); H = Math.max(1, r.height);
    renderer.setSize(W, H, false);
    camera.aspect = W / H; camera.updateProjectionMatrix();
    const halfH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * 14, halfW = halfH * camera.aspect;
    if (camera.aspect > 1.05) {
      base = { x: Math.min(halfW * 0.35 + 0.7, 4.3), y: 0.05, z: 14, s: Math.min(0.98, halfH / 4.2) };
    } else {
      const s = Math.min(1, (halfW * 2 * 0.86) / 5.6);
      base = { x: 0.2 * s, y: 0.6, z: 14, s };
    }
    rig.scale.setScalar(base.s);
  }
  layout();
  addEventListener('resize', layout);

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

  /* ---------- render loop ---------- */
  let visible = true, raf = 0, last = performance.now(), T = 0, ready = false;
  const ease = (a, b, k) => a + (b - a) * k;
  const easeOut = x => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);

  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now; T += dt;
    const it = (now - introAt) / 1000;

    // intro: inlet fills, valve turns, outlets fill, gauge rises
    if (!introDone) {
      handleA = -Math.PI / 2 + Math.PI / 2 * easeOut((it - 1.2) / 0.8);
      inlet.fill = easeOut((it - 0.3) / 1.0);
      lines.forEach(l => { if (l.ord > 0) l.fill = easeOut((it - 2.0 - l.ord * 0.12) / 1.3); });
      gaugeV = 3.0 * easeOut((it - 1.9) / 1.6) + Math.sin(Math.max(0, it - 1.9) * 9) * Math.exp(-Math.max(0, it - 1.9) * 2.5) * 0.35 * (it > 1.9 ? 1 : 0);
      if (it > 2.2) Object.values(co).forEach(el => el.classList.add('is-on'));
      if (it > 4) { introDone = true; lines.forEach(l => l.target = 1); gaugeTarget = 3; }
    } else {
      handleA = ease(handleA, handleTarget, 0.12);
      lines.forEach(l => { const sp = l.target > l.fill ? 0.9 : 1.6; l.fill += Math.sign(l.target - l.fill) * Math.min(Math.abs(l.target - l.fill), dt * sp / (l.ord ? 1 : 1)); });
      gaugeV = ease(gaugeV, gaugeTarget + (open ? Math.sin(T * 7) * 0.03 : 0), 0.06);
    }
    handle.rotation.y = handleA;
    needle.rotation.z = -(-135 + gaugeV * 27) * Math.PI / 180;
    lines.forEach(l => { l.mat.uniforms.fill.value = l.fill; l.mat.uniforms.t.value = RM ? 0 : T * (open || !introDone ? 1 : 0.15); });
    if (barTxt) barTxt.textContent = Math.max(0, gaugeV).toFixed(1).replace('.', ',') + ' bar';

    // motion: intro swing + pointer + drag + scroll
    const sc = Math.min(1.2, Math.max(0, scrollY / Math.max(1, hero.offsetHeight)));
    ptr.x = ease(ptr.x, ptr.tx, 0.05); ptr.y = ease(ptr.y, ptr.ty, 0.05);
    if (!dragging) { dragVel *= 0.94; dragRot += dragVel; dragRot *= 0.985; }
    const intro = easeOut(it / 2.2);
    const sway = RM ? 0 : Math.sin(T * 0.45) * 0.07;
    rig.rotation.y = -0.55 + intro * 0.25 + ptr.x * 0.22 + sway + dragRot + sc * 0.9;
    rig.rotation.x = 0.12 + ptr.y * 0.08 - sc * 0.15;
    rig.position.set(base.x, base.y + sc * 2.4 - (1 - intro) * 0.6, 0);
    camera.position.set(0, 0.5, base.z + sc * 2);
    camera.lookAt(0, 0.2, 0);

    renderer.render(scene, camera);
    if (!ready) { ready = true; canvas.classList.add('is-ready'); }

    // callouts
    for (const k in co) {
      if (!anchors[k]) continue;
      tmp.copy(anchors[k]); assy.localToWorld(tmp); tmp.project(camera);
      const x = (tmp.x * 0.5 + 0.5) * W, y = (-tmp.y * 0.5 + 0.5) * H;
      co[k].style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)' + (co[k].classList.contains('co--l') ? ' translateX(-100%)' : '');
      co[k].style.visibility = (tmp.z < 1 && x > 8 && x < W - 8 && y > 70 && y < H - 8) ? '' : 'hidden';
    }
    if (visible) raf = requestAnimationFrame(frame);
  }

  const startLoop = () => { if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); } };
  const stopLoop = () => { cancelAnimationFrame(raf); raf = 0; };
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(en => { visible = en[0].isIntersecting && !document.hidden; visible ? startLoop() : stopLoop(); }).observe(hero);
  }
  document.addEventListener('visibilitychange', () => { visible = !document.hidden; visible ? startLoop() : stopLoop(); });
  if (RM) introAt = performance.now() - 5000;
  startLoop();
}
