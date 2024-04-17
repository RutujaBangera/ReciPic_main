const menus = document.querySelector('nav ul');
const header = document.querySelector('header');
const menubtn = document.querySelector('.menu');
const closebtn = document.querySelector('.close');

menubtn.addEventListener('click', ()=> {
    menus.classList.add("display");
})

closebtn.addEventListener('click', ()=> {
    menus.classList.remove("display");
})