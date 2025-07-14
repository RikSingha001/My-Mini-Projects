const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const resultDisplay = document.getElementById('result');
const end = document.getElementById('end');
const tilesize=20;
const tileCount = canvas.width / tilesize;
let snake = [{ x: 5, y: 5 }];
let direction = { x: 1, y: 0 };
let food = randomFood();
let result =0;
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
function updateSnake(){
  const head={
    x: snake[0].x + direction.x,
    y: snake[0].y + direction.y,
  };
  if(
    head.x < 0 || head.x >= tileCount ||
    head.y < 0 || head.y >= tileCount ||
    snake.some(part => part.x === head.x && part.y === head.y)
  ){
    gameOver = true;
    end.style.display = 'block';
    return;
  }
  snake.unshift(head);
  if(head.x === food.x && head.y === food.y){
    result +=1;
    resultDisplay.textContent = `Result: ${result}`;
    speed += 1;
    food = randomFood();
  }else{
    snake.pop();
  }
}

function gameLoop(timestamp){
  if(gameOver) return;
  const frameTime= 1200/speed;
  if(timestamp - lastFrameTime > frameTime){
    updateSnake();
    draw();
    lastFrameTime = timestamp;
  }
  requestAnimationFrame(gameLoop);
}
document.addEventListener("keydown",(e)=>{
  if(gameOver && e.key.toLowerCase()==="r"){
    restartGame();
    return;
  }
  if(e.key === "ArrowUp"){
    direction = {x:0, y:-1};
  }
  if(e.key === "ArrowDown"){
    direction = {x:0, y:1};
  }
  if(e.key === "ArrowLeft"){
    direction = {x:-1, y:0};
  }
  if(e.key === "ArrowRight"){
    direction = {x:1, y:0};
  }
  if(snake.length===1 && direction.x===0){
    requestAnimationFrame(gameLoop);
  }
  if(snake.length===1 && direction.x===1){
    requestAnimationFrame(gameLoop);
  }
  if(snake.length===1 && direction.y===0){
    requestAnimationFrame(gameLoop);
  }
  if(snake.length===1 && direction.y===1){
    requestAnimationFrame(gameLoop);
  }
  if(snake.length===1 && direction.x===-1){
    requestAnimationFrame(gameLoop);
  }
  if(snake.length===1 && direction.y===-1){
    requestAnimationFrame(gameLoop);
  }
  

});
function restartGame(){
  snake= [{x:5,y:5}];
  direction={x:1,y:0};
  food=randomFood();
  gameOver=false;
  gameOverDisplay.style.display="none";
  requestAnimationFrame(gameLoop);
  }
    requestAnimationFrame(gameLoop);

