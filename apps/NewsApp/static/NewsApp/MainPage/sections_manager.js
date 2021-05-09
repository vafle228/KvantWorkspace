let page = 0;
let file_array = Array()
let news_preview = undefined

// Открытие формы по нажатию на курс
$("#widgets .item").click(function(event){
	$('#widgets .item').each(function(i, item){
		if(item == event.target.parentElement || item == event.target){
			$('#widgets .form')[i].style.display = 'block';
			$("body").css("position", "fixed");
		}
	})
});

// Добавление файлов по кнопке
$('#file-button').on('click', function(){
	$('#file-input')[0].value = ''
	$('#file-input').click()
})

// Добавление картинки по кнопке
$('#news-preview').on('click', function(){
	$('#preview-input')[0].value = ''
	$('#preview-input').click()
})

$('#news-upload').on('click', function(){
	let news_form = new FormData();

	news_form.append('image', news_preview)
	for(let i = 0; i < file_array.length; i++){
		news_form.append('files', file_array[i])
	}

	news_form.append('title', $('#news-title')[0].value)
	news_form.append('content', $('#news-content')[0].value)
	news_form.append('csrfmiddlewaretoken', csrf_token)

	$.ajax({
		type: 'POST',
		url: send_news_form,
		data: news_form,
		cache: false,
		processData: false,
    	contentType: false,
		enctype: "multipart/form-data",
		success: function(response) { 
			location.href = response 
		}
	})
})

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
		url: get_news,
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
		location.href = location.origin + '/news/' + String(id) + '/detail/' + String(news['id'])
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

function addFileWidget(file){
	let file_div = document.createElement('div')
	file_div.className = 'file'

	let file_info = document.createElement('div')
	file_info.className = 'file-info'

	let file_icon = document.createElement('i')
	splited_name = file.name.split('.')
	file_icon.className = 'file-' + splited_name[splited_name.length - 1]

	let file_name = document.createElement('h4')
	file_name.innerHTML = file.name

	file_info.appendChild(file_icon)
	file_info.appendChild(file_name)

	let file_btns = document.createElement('div')
	file_btns.className = 'file-btns'

	let delete_btn = document.createElement('button')
	delete_btn.className = 'del-file'
	delete_btn.type = 'button'

	file_btns.appendChild(delete_btn)

	file_div.appendChild(file_info)
	file_div.appendChild(file_btns)

	return file_div
}

function addNewFile(event){
	if(event.target.files[0] != undefined){
		let file = event.target.files[0]
		file_array.push(file)
		let file_id = file_array.length - 1

		let container = $('#file-container')[0]
		let file_widget = addFileWidget(file)

		file_widget.childNodes[1].childNodes[0].onclick = function(click) {
			file_array.splice(file_id, 1)
			container.removeChild(file_widget)
		}
		
		container.appendChild(file_widget)
	}
}

function addNewsPreview(event){
	if(event.target.files[0] != undefined){
		$('#news-preview')[0].style.display = 'none'
		news_preview = event.target.files[0]

		let btns_container = $('#news-form-btns')[0]

		let preview_widget = addFileWidget(news_preview)
		preview_widget.childNodes[1].childNodes[0].onclick = function(click) {
			news_preview = undefined
			btns_container.removeChild(preview_widget)
			$('#news-preview')[0].style.display = 'block'
		}

		btns_container.insertBefore(preview_widget, btns_container.firstChild)
	}
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
