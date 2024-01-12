$(document).ready(function(){
    $(".searchinput").keyup(function(){
        $(this).siblings(".searchclear").toggle(Boolean($(this).val()));
    });
    $(".searchclear").toggle(Boolean($(".searchinput").val()));
    $(".searchclear").click(function(){
        $(".searchinput").val('').focus();
        $(this).hide();
    });
});