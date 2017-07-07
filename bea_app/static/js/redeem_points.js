$(document).ready(function(){
  function convert_points(points){
    // converts points to cash with ration 1 point = 1 cent
    return parseFloat(Math.round(points * 100) / 10000).toFixed(2);
  }
  // initiate cash value based on user points
  var points = $('#user_points').text()
  var cash_points = convert_points(points);
  $('#cash_points').text(cash_points)

  // convert points when user inputs points
  $('#inputPoints').on('input', function() {
     if (isNaN($(this).val()))
       $('#cash_points').text('')
     else
       $('#cash_points').text(convert_points($(this).val()))
  });
});
