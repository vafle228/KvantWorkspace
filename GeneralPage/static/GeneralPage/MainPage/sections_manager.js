let page = 0;

// Открытие формы по нажатию на курс
$("#widgets .item").click(function(){
    $('#widgets .form')[0].style.display = 'block';
	$("body").css("position", "fixed");
});
// Перезагрузка старницы с анимацией логотипа
function reload(logo){
    logo.style.animation = 'you_spin_me_right_round 1s';
    setTimeout("location.reload()", 800);
}

function close_form(bg){
    bg.parentElement.style.display = 'none';
	$("body").css("position", "relative");
}

function getNewNews(){
	$.ajax({
		type: "POST",
		url: "/general/" + String(id) + "/send/news",
		data: {
			page: page,
			csrfmiddlewaretoken: csrf_token
		},
		cache: false,
		success: function(response){
			for(let i in response['news'])
				buildNewNews(response['news'][i])
		}
	});
	page += 1;
}


function buildNewNews(news){
	let div_item = document.createElement("div");
	div_item.className = "item";
	div_item.onclick = function() { 
		location.href = location.origin + '/general/' + String(id) + '/news/detail/' + String(news['id'])
	}

	let news_image = document.createElement("img");
	news_image.src = news['image'];
	news_image.alt = "Превью";

	let news_title = document.createElement("h2")
	news_title.innerHTML = news['title'];

	let news_content = document.createElement("p");
	news_content.innerHTML = news['content'];

	div_item.appendChild(news_image);
	div_item.appendChild(news_title);
	div_item.appendChild(news_content);

	$("#news-container")[0].appendChild(div_item);
}
