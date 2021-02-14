// Переход по вкладкам
function switch_to(section_id, btn) {
    for(let i = 0; i<4; i++){
        $('body > section')[i].style.display = 'none';
        $('aside button').removeClass('active');
    }
    document.getElementById(section_id).style.display = 'block';
    btn.className += ' active';
}

// Перезагрузка старницы с анимацией логотипа
function reload(logo){
    logo.style.animation = 'you_spin_me_right_round 1s';
    setTimeout("location.reload()", 800);
}

// Закрытие формы
function close_form(bg){
    bg.parentElement.style.display = 'none';
}

// Открытие формы по нажатию на урок
$("#diary .item").click(function(){
    $('#diary .form')[0].style.display = 'block';
});