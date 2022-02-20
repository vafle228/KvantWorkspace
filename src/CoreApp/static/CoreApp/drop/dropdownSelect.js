for (const option of document.querySelectorAll(".dropdownSelect__option")) {
    option.addEventListener('click', function() {
        if (!$(this).hasClass('selected')) {
            if($(this).parent().find('.dropdownSelect__option.selected')){
                $(this).parent().find('.dropdownSelect__option.selected').removeClass('selected');
            }
            $(this).addClass('selected');
            this.closest('.dropdownSelect').querySelector('.dropdownSelect__trigger span').textContent = this.textContent;
            this.closest('.dropdownSelect').querySelector('.dropdownSelect__trigger').classList.add('active');
            $(this).parents(".filtering").next().removeClass("disable");
        }
    })
}

for (const dropdown of document.querySelectorAll(".filtering")) {
    dropdown.addEventListener('click', function() {
        if (!$(this).hasClass('disable')){
            this.querySelector('.dropdownSelect').classList.toggle('open');
        }
    })
}

window.addEventListener('click', function(e) {
    for (const select of document.querySelectorAll('.dropdownSelect')) {
        if (!select.contains(e.target)) {
            select.classList.remove('open');
        }
    }
});