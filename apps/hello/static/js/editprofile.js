
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


function fakeGoodSaving() {
  blockPage();
  setTimeout(hardcodedUpdate, 2000);
}


function fakeFailSaving() {
  blockPage();
  setTimeout(showErrors, 2000);
}


function hardcodedUpdate() {
var profile = {
    pk: 2, 
    model: "hello.aboutme",
    fields: [{
        first_name: "Kim", 
        last_name: "Shao",  
        birthday: "1981-03-25", 
        email: "kim@box.com",
        jabber: "ks_jab", 
        skype: "ks_skype", 
        bio: "Senior Django developer", 
        contacts: "facebook.com/kim"
    }]
};

	$.ajax({
	url: $(this).attr("href"),
	cache: false,

	success: function(){
      for(field in profile.fields[0]) 
        $('#id_' + field).val(profile.fields[0][field]);

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

  error: function(error){
      unblockPage();
		  console.log(error);
      }
	});
}


function showErrors() {
  var errors = {
        first_name: "This field is required",  
        last_name:  "This field is required",
        birthday:   "Enter a valid date", 
        email:      "Enter a valid email address",
        jabber:     "This field is required",
        skype:      "This field is required"
      };

	$.ajax({
	url: $(this).attr("href"),
	cache: false,

	success: function(){
      unblockPage();
      var message = "<div id='failmessage' class='col-xs-12'>" +
                    "<b>Check errors, please!</b></div>";
      $('.loader').before(message);
      $('#failmessage').after("<p id='after_fail_empty_string'>&nbsp</p>");

			var $idElement, $labelElement;

			for(field in errors) {
				$idElement = $('#id_' + field);
				$idElement.parent('div').prepend('<span>&nbsp'+errors[field]+'</span>');
        if(errors[field]) {
				  $labelElement = $("label[for='"+$idElement.attr('id')+"']").prepend('<span>*</span>');
				  $labelElement.parent('div').addClass('has-error')
          }
			  }
		  },

  error: function(error){
      unblockPage();
		  console.log(error);
      }
	});
}


$( function() {
    $("#id_birthday").datepicker();
    $( "#id_birthday" ).datepicker("option", "dateFormat", "yy-mm-dd");
    $("#id_birthday").datepicker("setDate" , "2016-01-01");
});
