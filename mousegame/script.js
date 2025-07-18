
const canvas = document.getElementById("c");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const total = 1000;
    const seg = [];

    let mouse = { x: canvas.width / 2, y: canvas.height / 2 };

    document.addEventListener("mousemove", (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });

    for (let i = 0; i < total; i++) {
      seg.push({ x: mouse.x, y: mouse.y });
    }

    function update() {
      seg[0].x += (mouse.x - seg[0].x) * 0.2;
      seg[0].y += (mouse.y - seg[0].y) * 0.2;

      for (let i = 1; i < seg.length; i++) {
        seg[i].x += (seg[i - 1].x - seg[i].x) * 0.3;
        seg[i].y += (seg[i - 1].y - seg[i].y) * 0.3;
      }
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < seg.length; i++) {
        ctx.beginPath();
        ctx.fillStyle = `hsl(${i * 20}, 100%, 70%)`;
        ctx.arc(seg[i].x, seg[i].y, 8, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    function animate() {
      update();
      draw();
      requestAnimationFrame(animate);
    }

    animate();

