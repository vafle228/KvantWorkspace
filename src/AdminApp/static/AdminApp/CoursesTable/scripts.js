function scheduleScanner(){
	lesson_shedule = {}
	$('#createGroup').find('input[type=time]').toArray().forEach((input)  => {
		lesson_shedule[$(input).prev().text()] = $(input).val()
	});
	return lesson_shedule
}

$('#teacherSelect .userSelect__user').click( function() {
    if ($(this).parent().attr('id') == 'teacherSelect') {
        $('#selectedTeachers').append($(this));
        $('#teacherSearch').val('').focus();
        $('.userSelect').hide();
        $('#teacherSearch').hide();
    } else {
        $('#teacherSelect').append($(this));
        $('#teacherSearch').show();
    }
});

$('#studentSelect .userSelect__user').click( function() {
    if ($(this).parent().attr('id') == 'studentSelect') {
        $('#selectedStudents').append($(this));
        $('#studentSearch').val('').focus();
        $('.userSelect').hide();
    } else {
        $('#studentSelect').append($(this));
    }
});
