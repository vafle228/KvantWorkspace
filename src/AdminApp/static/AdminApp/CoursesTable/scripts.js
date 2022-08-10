function scheduleScanner(){
	lesson_shedule = {}
	$('#createGroup').find('input[type=time]').toArray().forEach((input)  => {
		lesson_shedule[$(input).prev().text()] = $(input).val()
	});
	return lesson_shedule
}