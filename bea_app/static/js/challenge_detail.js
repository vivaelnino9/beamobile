function changeColor(dropdownList){if (dropdownList.value){dropdownList.style.color = '#555'};}
$(".complete").click(function(){
  var form = $("#location_form");
  form.validate()
  if (form.valid()){
    $("#challengeDetail").css("display","none")
    $("#completeChallenge").css("display","inline")
    $("#completeChallenge")[0].scrollIntoView({
        behavior: "smooth", // or "auto" or "instant"
        block: "start" // or "end"
    });
  }
  else
    $('label.error').css("color","red")
});
$(".feeling").click(function(){
  $("#feelingChoice").val($(this).text());
  $("#location_form").submit();
})
