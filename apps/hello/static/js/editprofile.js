
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

// Change image when user select another file

$("#id_photo").change(function() {
  var input = this;

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $(".picture").attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]);
  }
});

// Change image to default when user clear image in edit.html

$('input[name="photo-clear"]').click(function() {
  $('input[name="photo"]').parent('div').hide();
  $('label[for="id_photo"]').after('<div><br><br></div>');
  $(".picture").attr('src', '/static/img/user_default.png');
}); 


function customizePhotoDiv() {
  $photoDiv = $('input[name="photo"]').parent('div');
  $photoDiv.find('a').hide(); // hide imagelink

  $photoDiv.contents().filter(function() {
    return this.nodeType===3; // remove text from div
  }).remove();
}


$(document).ready(function() {
  customizePhotoDiv();

  /*  Set configuration to validate form before submit 
      http://www.formvalidator.net */

  var config = {         
    form : 'form',
    validate : {
      '#id_first_name, #id_last_name' : {
        validation : 'length',
        length : 'min3'
      },
      '#id_email, #id_jabber' : {
        validation : 'email'
      },
      '#id_birthday' : {
        validation : 'birthdate',
        'error-msg' : 'Date should be younger than today and not older than 120 years'
      }
    },
    onElementValidate : function(valid, $el, $form, errorMess) {
       $rowDiv = $el.parents().eq(3);
       if(valid) {
         $rowDiv.removeClass('errorspacing');
       } else {
         $rowDiv.addClass('errorspacing');
       }
    }
  };

  $.validate({
     modules : 'jsconf, date',
     onModulesLoaded : function() {
       $.setupValidation(config);
     }
  }); 

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
          var message = '';
          var errors = JSON.parse(msg.responseText);

          if (errors['Image']) {
            console.log(errors['Image']);
          } else {
            message = "<div id='failmessage' class='col-xs-12'>" +
                      "<b>Check errors, please!</b><br><br>";

            var fields = ['first_name', 'last_name',  'birthday',
                          'email', 'jabber', 'skype'];

            $.each(fields, function( index, field ) {
              if(errors[field]) {
                message += field+ ': ' +errors[field]+ '<br>'
              }
            });

            message += '</div>';
            $('.loader').before(message);
            $('#failmessage').after("<p id='after_fail_empty_string'>&nbsp</p>");
          }
        }
  };

  $('#ajaxform').ajaxForm(options);    
  
});


