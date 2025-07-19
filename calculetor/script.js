const text = document.getElementById('textarea');
const allClr = document.getElementById('allClr');
const clear = document.getElementById('clear');
const delet = document.getElementById('delete');
const equal = document.getElementById('equal');

const btnArray = [
  'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
  'eight', 'nine', 'divide', 'multiply', 'minus', 'plus', 'point'
];

btnArray.forEach((id) => {
  const btn = document.getElementById(id);
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    text.value += btn.value;
  });
});

clear.addEventListener('click', (e) => {
  e.preventDefault();
  text.value = text.value.slice(0, -1);
});

allClr.addEventListener('click', (e) => {
  e.preventDefault();
  text.value = '';
});

delet.addEventListener('click', (e) => {
  e.preventDefault();
  text.value = text.value.slice(0, -1);
});

equal.addEventListener('click', (e) => {
  e.preventDefault();
  try {
    text.value = eval(text.value);
  } catch {
    text.value = 'Error';
  }
});
