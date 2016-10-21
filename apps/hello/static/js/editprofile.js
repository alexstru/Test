
function blockPage() {
    if( $('#failmessage').length ) {
      $('#failmessage').remove();
      $('#after_fail_empty_string').remove();
      $('div .form-group').removeClass('has-error');
      $('span').remove();
    } 
		$('textarea').attr('disabled', 'disabled');
		$('input').attr('disabled', 'disabled');
		$('button').attr('disabled', 'disabled');
		$('a').attr('disabled', 'disabled');
		$('.loader').css('display', 'block');
}


function unblockPage() {
		$('textarea').removeAttr('disabled');
		$('input').removeAttr('disabled');
		$('button').removeAttr('disabled');
		$('a').removeAttr('disabled');
		$('.loader').css('display', 'none');
}


$( function() {
    $("#id_birthday").datepicker();
    $( "#id_birthday" ).datepicker("option", "dateFormat", "yy-mm-dd");
    $("#id_birthday").datepicker("setDate" , "2016-01-01");
});


$(document).ready(function() {

	// Set options for ajaxForm
	var options = {
        beforeSubmit: function(){
          blockPage();
        },

        success: function(msg){

          unblockPage();
          var message = "<div id='goodmessage' class='col-xs-12" +
                        " bg-success prof_updated'>" +
                        "Changes have been save!</div><br><br>";
          $('.loader').before(message);
          setTimeout(function() {
            $('#goodmessage').remove();
            $('#content-column br').eq(0).remove();
            $('#content-column br').eq(0).remove();
            }, 2000);
        },

        error: function(msg) {

          unblockPage();
          var message = "<div id='failmessage' class='col-xs-12'>" +
                        "<b>Check errors, please!</b></div>";
          $('.loader').before(message);
          $('#failmessage').after("<p id='after_fail_empty_string'>&nbsp</p>");

          var errors = JSON.parse(msg.responseText);

          var fields = ['first_name', 'last_name',  'birthday',
                        'email', 'jabber', 'skype'];

          var $idElement, $labelElement;

          $.each(fields, function( index, field ) {
            $idElement = $('#id_' + field);
            $labelElement = $("label[for='"+$idElement.attr('id')+"']");
            $idElement.parent('div').prepend('<span>&nbsp</span>');

            if(errors[field]) {
              $idElement.parent('div').prepend('<span>'+errors[field]+'</span>');
              $labelElement.prepend('<span>*</span>');
              $labelElement.parent('div').addClass('has-error');
            }
          });
        }
  };

  $('#ajaxform').ajaxForm(options);
});


