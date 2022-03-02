let marks = {}

$(".menu__button").on("click", function(){
    $(this).parent().find(".menu__button").removeClass("active");
    $(this).toggleClass("active", "inactive");
});

addMark = (student, mark) => marks[student] = mark;
