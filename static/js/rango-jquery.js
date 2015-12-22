$(document).ready(function(){
  //JQuery code to be added in here.
  $("#about-btn").click(function(event){
  	alert("You clicked the button using JQuery!");
  });
  $("#about-btn").addClass('btn btn-primary')
  $("p").hover( function() {
            $(this).css('color', 'red');
    },
    function() {
            $(this).css('color', 'blue');
    });
  $("#about-btn").click(function  (event) {
  	// body...
  	msgstr = $('h1').html()
  		msgstr = msgstr + ' me'
  		$('h1').html(msgstr)
  });

  // $("p").css('color','pink');
});