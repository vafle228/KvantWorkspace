let lesson = NaN


function openTaskAddForm(lesson_id, form_id){
	lesson = lesson_id
	$(".mainContainer").css("overflow", "hidden");
	$(form_id).addClass("active");
}
