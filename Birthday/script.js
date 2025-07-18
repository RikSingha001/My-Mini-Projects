
let c = document.getElementById("c"),
    ctx = c.getContext("2d"),
    w = c.width = window.innerWidth,
    h = c.height = window.innerHeight,
    hw = w / 2, hh = h / 2,
    name = prompt("Enter your name"),
    msg = ["HAPPY", "BIRTHDAY!", "To You", name || "Friend"];

ctx.font = "50px sans-serif";
ctx.textAlign = "center";
ctx.textBaseline = "middle";

let letters = [];
msg.forEach((line, i) => {
  [...line].forEach((ch, j) => {
    letters.push({
      char: ch,
      x: hw + (j - line.length / 2) * 40,
      y: hh + (i - msg.length / 2) * 60,
      phase: "launch",
      tick: 0,
      color: `hsl(${Math.random() * 360},80%,60%)`
    });
  });
});

function drawFirework(letter) {
  let p = letter.tick / 30;
  let y = hh + (letter.y - hh) * p;
  ctx.strokeStyle = letter.color;
  ctx.beginPath();
  ctx.moveTo(letter.x, hh);
  ctx.lineTo(letter.x, y);
  ctx.stroke();
  if (letter.tick >= 30) letter.phase = "show"; 
}

function drawText(letter) {
  ctx.fillStyle = letter.color;
  ctx.fillText(letter.char, letter.x, letter.y);
  if (++letter.tick > 100) letter.phase = "balloon";
}

function drawBalloon(letter) {
  letter.y -= 1.5;
  ctx.beginPath();
  ctx.fillStyle = letter.color;
  ctx.ellipse(letter.x, letter.y, 20, 30, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.moveTo(letter.x, letter.y + 30);
  ctx.lineTo(letter.x, letter.y + 50);
  ctx.stroke();
  ctx.fillText(letter.char, letter.x, letter.y + 60);
  if (letter.y + 60 < 0) letter.phase = "done";
}

function animate() {
  ctx.fillStyle = "#111";
  ctx.fillRect(0, 0, w, h);
  letters.forEach(l => {
    if (l.phase === "launch") drawFirework(l);
    else if (l.phase === "show") drawText(l);
    else if (l.phase === "balloon") drawBalloon(l);
    l.tick++;
  });
  requestAnimationFrame(animate);
}
animate();

window.addEventListener("resize", () => {
  w = c.width = window.innerWidth;
  h = c.height = window.innerHeight;
  hw = w / 2;
  hh = h / 2;
});
