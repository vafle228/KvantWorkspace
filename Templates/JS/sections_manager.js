function switch_to(section_id, btn) {
    for(let i = 0; i<4; i++){
        $('body > section')[i].style.display = 'none';
        $('aside button').removeClass('active');
    }
    document.getElementById(section_id).style.display = 'block';
    btn.className += ' active';
}