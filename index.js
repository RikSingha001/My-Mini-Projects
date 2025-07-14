const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const resultDisplay = document.getElementById('result');
const end = document.getElementById('end');

const tilesize = 20;
const tileCount = canvas.width / tilesize;

let snake = [{ x: 5, y: 5 }];
let direction = { x: 1, y: 0 };
let food = randomFood();
let result = 0;
let gameOver = false;
let speed = 7;
let lastFrameTime = 0;

function randomFood() {
  let pos;
  do {
    pos = {
      x: Math.floor(Math.random() * tileCount),
      y: Math.floor(Math.random() * tileCount),
    };
  } while (snake.some(part => part.x === pos.x && part.y === pos.y));
  return pos;
}

function draw() {
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw food
  ctx.fillStyle = 'red';
  ctx.fillRect(food.x * tilesize, food.y * tilesize, tilesize, tilesize);

  // Draw snake
  ctx.fillStyle = '#0f0';
  for (const segment of snake) {
    ctx.fillRect(segment.x * tilesize, segment.y * tilesize, tilesize, tilesize);
  }
}

function updateSnake() {
  const head = {
    x: snake[0].x + direction.x,
    y: snake[0].y + direction.y,
  };

  // Check collision
  if (
    head.x < 0 || head.x >= tileCount ||
    head.y < 0 || head.y >= tileCount ||
    snake.some(part => part.x === head.x && part.y === head.y)
  ) {
    gameOver = true;
    end.style.display = 'block';
    return;
  }

  snake.unshift(head);

  if (head.x === food.x && head.y === food.y) {
    result += 1;
    resultDisplay.textContent = `Result: ${result}`;
    speed += 1;
    food = randomFood();
  } else {
    snake.pop();
  }
}

function gameLoop(timestamp) {
  if (gameOver) return;

  const frameTime = 1200 / speed;
  if (timestamp - lastFrameTime > frameTime) {
    updateSnake();
    draw();
    lastFrameTime = timestamp;
  }

  requestAnimationFrame(gameLoop);
}

document.addEventListener("keydown", (e) => {
  if (gameOver && e.key.toLowerCase() === "r") {
    restartGame();
    return;
  }

  const key = e.key;
  if (key === "ArrowUp" && direction.y === 0) {
    direction = { x: 0, y: -1 };
  } else if (key === "ArrowDown" && direction.y === 0) {
    direction = { x: 0, y: 1 };
  } else if (key === "ArrowLeft" && direction.x === 0) {
    direction = { x: -1, y: 0 };
  } else if (key === "ArrowRight" && direction.x === 0) {
    direction = { x: 1, y: 0 };
  }
});
function setDirection(dir) {
  if (dir === 'up' && direction.y === 0) {
    direction = { x: 0, y: -1 };
  } else if (dir === 'down' && direction.y === 0) {
    direction = { x: 0, y: 1 };
  } else if (dir === 'left' && direction.x === 0) {
    direction = { x: -1, y: 0 };
  } else if (dir === 'right' && direction.x === 0) {
    direction = { x: 1, y: 0 };
  }
}

function restartGame() {
  snake = [{ x: 5, y: 5 }];
  direction = { x: 1, y: 0 };
  food = randomFood();
  result = 0;
  resultDisplay.textContent = `Result: ${result}`;
  gameOver = false;
  speed = 7;
  lastFrameTime = 0;
  end.style.display = "none";
  requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);


//npx http-server -p 3000

