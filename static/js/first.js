$(function ($) {
    $("#login").on("click",function () {
        $("body").append("<div class='hiding'></div>");
        $(".hiding").fadeIn("slow");
        $("#loginer").fadeIn("slow");
    });
});