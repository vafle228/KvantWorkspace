let page = 1;

// <=== Скрипты работы страницы ===>

// Открытие формы по нажатию на курс
$("#slider .item").click(function(event){
	$('#widgets .item').each(function(i, item){
		if(item == event.delegateTarget || item == event.target){
			$($('#widgets .form')[i]).addClass("active");
			$("body").css("overflow", "hidden");
		}
	})
});
