/**
 * 3D Dashboard Background (Three.js)
 * - Wireframe grid
 * - Dust particles
 * - Floating shapes
 * - Ambient orbs
 * - Theme-adaptive via `themeChanged` event
 */
(function () {
  "use strict";

  const THEMES = {
    light: {
      bgColor: 0xf0f6ff,
      gridColor: 0x8896b0,
      gridOpacity: 0.06,
      dustColor: 0x7b8fb5,
      dustOpacity: 0.45,
      dustSize: 0.12,
      orbColor1: 0x8896b0,
      orbColor2: 0xb08d60,
      orbOpacity: 0.04,
      fogColor: 0xf0f6ff,
      useNormalBlending: true,
    },
    dark: {
      bgColor: 0x09121f,
      gridColor: 0x00d4ff,
      gridOpacity: 0.06,
      dustColor: 0x00d4ff,
      dustOpacity: 0.36,
      dustSize: 0.08,
      orbColor1: 0x00d4ff,
      orbColor2: 0x7c3aed,
      orbOpacity: 0.015,
      fogColor: 0x09121f,
      useNormalBlending: false,
    },
  };

  const DUST_COUNT = 60;
  const canvas = document.getElementById("dashBg3d");
  if (!canvas) return;

  // If Three.js is not available, show a CSS fallback (static neon/orbs)
  if (typeof THREE === "undefined") {
    canvas.classList.add("bg-fallback");
    return;
  }

  const renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: false,
    antialias: false,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    50,
    window.innerWidth / window.innerHeight,
    0.1,
    80,
  );
  camera.position.set(0, 6, 18);
  camera.lookAt(0, 0, 0);

  let currentTheme =
    document.documentElement.getAttribute("data-theme") === "dark"
      ? "dark"
      : "dark";
  // Prefer dark by default to match design
  if (document.documentElement.getAttribute("data-theme") === "light")
    currentTheme = "light";

  // Grid
  const gridGeo = new THREE.PlaneGeometry(40, 40, 30, 30);
  const gridMat = new THREE.MeshBasicMaterial({
    color: THEMES[currentTheme].gridColor,
    wireframe: true,
    transparent: true,
    opacity: THEMES[currentTheme].gridOpacity,
    depthWrite: false,
  });
  const grid = new THREE.Mesh(gridGeo, gridMat);
  grid.rotation.x = -Math.PI / 2.4;
  grid.position.y = -4;
  scene.add(grid);

  // Dust
  const dustGeo = new THREE.BufferGeometry();
  const dustPos = new Float32Array(DUST_COUNT * 3);
  const dustVel = new Float32Array(DUST_COUNT * 3);

  for (let i = 0; i < DUST_COUNT; i++) {
    dustPos[i * 3] = (Math.random() - 0.5) * 34;
    dustPos[i * 3 + 1] = (Math.random() - 0.5) * 18;
    dustPos[i * 3 + 2] = (Math.random() - 0.5) * 22;
    dustVel[i * 3] = (Math.random() - 0.5) * 0.005;
    dustVel[i * 3 + 1] = Math.random() * 0.003 + 0.001;
    dustVel[i * 3 + 2] = (Math.random() - 0.5) * 0.003;
  }
  dustGeo.setAttribute("position", new THREE.BufferAttribute(dustPos, 3));

  const dustMat = new THREE.PointsMaterial({
    color: THEMES[currentTheme].dustColor,
    size: THEMES[currentTheme].dustSize,
    transparent: true,
    opacity: THEMES[currentTheme].dustOpacity,
    blending: THEMES[currentTheme].useNormalBlending
      ? THREE.NormalBlending
      : THREE.AdditiveBlending,
    depthWrite: false,
    sizeAttenuation: true,
  });

  const dust = new THREE.Points(dustGeo, dustMat);
  scene.add(dust);

  // Floating shapes
  const shapes = [];
  const shapeGeos = [
    new THREE.OctahedronGeometry(0.6, 0),
    new THREE.IcosahedronGeometry(0.5, 0),
    new THREE.TetrahedronGeometry(0.4, 0),
  ];

  for (let i = 0; i < 3; i++) {
    const mat = new THREE.MeshBasicMaterial({
      color: THEMES[currentTheme].gridColor,
      wireframe: true,
      transparent: true,
      opacity: THEMES[currentTheme].gridOpacity * 1.5,
      depthWrite: false,
    });
    const mesh = new THREE.Mesh(shapeGeos[i], mat);
    mesh.position.set(
      (Math.random() - 0.5) * 24,
      (Math.random() - 0.5) * 10,
      -3 - Math.random() * 6,
    );
    mesh.userData = {
      rotX: (Math.random() - 0.5) * 0.004,
      rotY: (Math.random() - 0.5) * 0.006,
      baseY: mesh.position.y,
      floatPhase: Math.random() * Math.PI * 2,
    };
    scene.add(mesh);
    shapes.push(mesh);
  }

  // --- Crystal shards (transparent refractive pieces) ---
  const SHARD_COUNT = 20;
  const shards = [];

  // helper to create a tapered shard from a Tetrahedron scaled non-uniformly
  function createShardMesh(theme) {
    const geo = new THREE.TetrahedronGeometry(1.0, 0);
    // scale to make it shard-like
    geo.scale(0.9, 1.8 + Math.random() * 2.4, 0.35 + Math.random() * 0.6);

    const mat = new THREE.MeshPhysicalMaterial({
      color: theme.orbColor1,
      transparent: true,
      opacity: 0.18,
      transmission: 0.88,
      roughness: 0.02,
      metalness: 0.0,
      ior: 1.45,
      reflectivity: 0.4,
      clearcoat: 0.06,
      clearcoatRoughness: 0.02,
      side: THREE.DoubleSide,
    });

    const m = new THREE.Mesh(geo, mat);
    return m;
  }

  for (let i = 0; i < SHARD_COUNT; i++) {
    const s = createShardMesh(THEMES[currentTheme]);
    s.position.set(
      (Math.random() - 0.5) * 28,
      -1 + Math.random() * 12,
      -2 - Math.random() * 18,
    );
    s.rotation.set(Math.random() * 2, Math.random() * 2, Math.random() * 2);
    s.scale.setScalar(0.6 + Math.random() * 1.6);
    s.userData = {
      vel: new THREE.Vector3(
        (Math.random() - 0.5) * 0.02,
        (Math.random() - 0.5) * 0.02,
        (Math.random() - 0.5) * 0.02,
      ),
      rotVel: new THREE.Vector3(
        (Math.random() - 0.5) * 0.004,
        (Math.random() - 0.5) * 0.006,
        (Math.random() - 0.5) * 0.004,
      ),
      baseY: s.position.y,
      wobblePhase: Math.random() * Math.PI * 2,
    };
    scene.add(s);
    shards.push(s);
  }

  // Orbs
  const orbs = [];
  for (let i = 0; i < 4; i++) {
    const orbGeo = new THREE.SphereGeometry(1.5 + Math.random() * 2, 12, 12);
    const orbMat = new THREE.MeshBasicMaterial({
      color:
        i < 2 ? THEMES[currentTheme].orbColor1 : THEMES[currentTheme].orbColor2,
      transparent: true,
      opacity: THEMES[currentTheme].orbOpacity,
      blending: THEMES[currentTheme].useNormalBlending
        ? THREE.NormalBlending
        : THREE.AdditiveBlending,
      depthWrite: false,
    });
    const orb = new THREE.Mesh(orbGeo, orbMat);
    orb.position.set(
      (Math.random() - 0.5) * 24,
      (Math.random() - 0.5) * 10,
      -6 - Math.random() * 8,
    );
    orb.userData = {
      speedX: (Math.random() - 0.5) * 0.006,
      speedY: (Math.random() - 0.5) * 0.004,
      phase: Math.random() * Math.PI * 2,
      baseOpacity: THEMES[currentTheme].orbOpacity,
    };
    scene.add(orb);
    orbs.push(orb);
  }

  // Mouse tracking
  let targetMouseX = 0,
    targetMouseY = 0,
    mouseX = 0,
    mouseY = 0;
  document.addEventListener("mousemove", (e) => {
    targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  scene.fog = new THREE.Fog(THEMES[currentTheme].fogColor, 14, 45);
  renderer.setClearColor(THEMES[currentTheme].bgColor, 1);

  function applyTheme(themeName) {
    currentTheme = themeName;
    const t = THEMES[currentTheme];

    gridMat.color.setHex(t.gridColor);
    gridMat.opacity = t.gridOpacity;

    dustMat.color.setHex(t.dustColor);
    dustMat.opacity = t.dustOpacity;
    dustMat.size = t.dustSize;
    dustMat.blending = t.useNormalBlending
      ? THREE.NormalBlending
      : THREE.AdditiveBlending;
    dustMat.needsUpdate = true;

    shapes.forEach((s) => {
      s.material.color.setHex(t.gridColor);
      s.material.opacity = t.gridOpacity * 1.5;
    });

    orbs.forEach((o, i) => {
      o.material.color.setHex(i < 2 ? t.orbColor1 : t.orbColor2);
      o.material.opacity = t.orbOpacity;
      o.material.blending = t.useNormalBlending
        ? THREE.NormalBlending
        : THREE.AdditiveBlending;
      o.material.needsUpdate = true;
      o.userData.baseOpacity = t.orbOpacity;
    });

    // update shards to match theme - tint and transparency
    if (typeof shards !== "undefined") {
      shards.forEach((sh) => {
        if (sh && sh.material) {
          sh.material.color.setHex(t.orbColor1);
          sh.material.opacity = currentTheme === "dark" ? 0.16 : 0.22;
          sh.material.transmission = currentTheme === "dark" ? 0.9 : 0.8;
          sh.material.ior = currentTheme === "dark" ? 1.5 : 1.35;
          sh.material.needsUpdate = true;
        }
      });
    }

    // update rim light if present
    if (typeof rimLight !== "undefined" && rimLight) {
      rimLight.color.setHex(t.orbColor2);
      rimLight.intensity = currentTheme === "dark" ? 0.28 : 0.18;
    }

    scene.fog.color.setHex(t.fogColor);
    renderer.setClearColor(t.bgColor, 1);
  }

  window.addEventListener("themeChanged", (e) => {
    if (e && e.detail && e.detail.theme) applyTheme(e.detail.theme);
  });

  // add a few lights to create colored refraction highlights for shards
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
  dirLight.position.set(5, 10, 7);
  scene.add(dirLight);

  const rimLight = new THREE.PointLight(
    THEMES[currentTheme].orbColor2,
    0.25,
    40,
    2,
  );
  rimLight.position.set(-8, 6, 6);
  scene.add(rimLight);

  const ambient = new THREE.AmbientLight(0xffffff, 0.14);
  scene.add(ambient);

  // pointer (click) interaction: small rumble impulse to nearby shards
  canvas.addEventListener("pointerdown", (ev) => {
    // compute normalized device coords
    const rect = canvas.getBoundingClientRect();
    const ndc = new THREE.Vector2(
      ((ev.clientX - rect.left) / rect.width) * 2 - 1,
      -((ev.clientY - rect.top) / rect.height) * 2 + 1,
    );
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(ndc, camera);
    const clickPoint = raycaster.ray.at(8, new THREE.Vector3());

    shards.forEach((sh) => {
      const d = sh.position.distanceTo(clickPoint);
      if (d < 6.5) {
        // add impulse away from click
        const dir = new THREE.Vector3()
          .subVectors(sh.position, clickPoint)
          .normalize();
        const force = (6.5 - d) / 6.5;
        sh.userData.vel.addScaledVector(dir, 0.12 * force);
        sh.userData.rotVel.addScaledVector(
          new THREE.Vector3(Math.random(), Math.random(), Math.random()),
          0.08 * force,
        );
      }
    });

    // small camera rumble
    const originalZ = camera.position.z;
    const rumble = { t: 0 };
    const rumbleDur = 0.34;
    const start = performance.now();
    (function rumbleStep() {
      const p = (performance.now() - start) / (rumbleDur * 1000);
      if (p >= 1) {
        camera.position.z = originalZ;
        return;
      }
      camera.position.z =
        originalZ + Math.sin(p * Math.PI * 4) * 0.35 * (1 - p);
      requestAnimationFrame(rumbleStep);
    })();
  });

  // Animate
  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const elapsed = clock.getElapsedTime();

    mouseX += (targetMouseX - mouseX) * 0.06;
    mouseY += (targetMouseY - mouseY) * 0.06;

    const vh =
      2 *
      camera.position.z *
      Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const vw = vh * camera.aspect;
    const sceneMouseX = mouseX * (vw / 2);
    const sceneMouseY = -mouseY * (vh / 2);

    const parallaxStrength = currentTheme === "dark" ? 1.0 : 0.6;
    camera.position.x += (mouseX * parallaxStrength - camera.position.x) * 0.03;
    camera.position.y +=
      (-mouseY * parallaxStrength * 0.6 + 6 - camera.position.y) * 0.03;
    camera.lookAt(0, 0, 0);

    grid.rotation.z = Math.sin(elapsed * 0.08) * 0.05;
    grid.position.y = -4 + Math.sin(elapsed * 0.15) * 0.3;

    const gridPositions = gridGeo.attributes.position.array;
    for (let i = 0; i < gridPositions.length; i += 3) {
      const x = gridPositions[i];
      const y = gridPositions[i + 1];
      gridPositions[i + 2] =
        Math.sin(x * 0.3 + elapsed * 0.4) * 0.3 +
        Math.cos(y * 0.3 + elapsed * 0.3) * 0.3;
    }
    gridGeo.attributes.position.needsUpdate = true;

    const dPos = dustGeo.attributes.position.array;
    for (let i = 0; i < DUST_COUNT; i++) {
      dPos[i * 3] += dustVel[i * 3];
      dPos[i * 3 + 1] += dustVel[i * 3 + 1];
      dPos[i * 3 + 2] += dustVel[i * 3 + 2];

      const dx = dPos[i * 3] - sceneMouseX;
      const dy = dPos[i * 3 + 1] - sceneMouseY;
      const distSq = dx * dx + dy * dy;
      const repelRadius = 4.0;

      if (distSq < repelRadius * repelRadius) {
        const dist = Math.sqrt(distSq);
        const force = (repelRadius - dist) / repelRadius;
        dPos[i * 3] += (dx / dist) * force * 0.025;
        dPos[i * 3 + 1] += (dy / dist) * force * 0.025;
      }

      if (dPos[i * 3 + 1] > 9) {
        dPos[i * 3 + 1] = -9;
        dPos[i * 3] = (Math.random() - 0.5) * 34;
        dPos[i * 3 + 2] = (Math.random() - 0.5) * 22;
      }
      if (Math.abs(dPos[i * 3]) > 17) dustVel[i * 3] *= -1;
    }
    dustGeo.attributes.position.needsUpdate = true;

    shapes.forEach((s) => {
      let speedMult = 1;
      const dx = s.position.x - sceneMouseX;
      const dy = s.position.y - sceneMouseY;
      if (dx * dx + dy * dy < 12) speedMult = 1.4;

      s.rotation.x += s.userData.rotX * speedMult;
      s.rotation.y += s.userData.rotY * speedMult;
      s.position.y =
        s.userData.baseY +
        Math.sin(elapsed * 0.3 + s.userData.floatPhase) * 0.5;
    });

    // update shards: gentle float, apply velocities, damping
    shards.forEach((sh) => {
      // gentle float
      const floatY = Math.sin(elapsed * 0.5 + sh.userData.wobblePhase) * 0.18;
      sh.position.y = sh.userData.baseY + floatY;

      // apply velocity and rotation
      sh.position.add(sh.userData.vel);
      sh.rotation.x += sh.userData.rotVel.x;
      sh.rotation.y += sh.userData.rotVel.y;
      sh.rotation.z += sh.userData.rotVel.z;

      // damping
      sh.userData.vel.multiplyScalar(0.94);
      sh.userData.rotVel.multiplyScalar(0.92);

      // keep within bounds
      if (sh.position.y > 12) sh.position.y = 12;
      if (sh.position.y < -6) sh.position.y = -6;
      if (sh.position.x > 35 || sh.position.x < -35)
        sh.position.x = (Math.random() - 0.5) * 28;
    });

    orbs.forEach((orb) => {
      orb.position.x += orb.userData.speedX;
      orb.position.y += Math.sin(elapsed * 0.2 + orb.userData.phase) * 0.003;
      orb.material.opacity =
        orb.userData.baseOpacity +
        Math.sin(elapsed * 0.3 + orb.userData.phase) *
          (orb.userData.baseOpacity * 0.4);

      if (Math.abs(orb.position.x) > 14) orb.userData.speedX *= -1;
    });

    renderer.render(scene, camera);
  }

  animate();

  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
})();
