
function blockPage() {
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
      $('#id_first_name').val(profile.fields[0].first_name);
      $('#id_last_name').val(profile.fields[0].last_name);
      $('#id_birthday').val(profile.fields[0].birthday);
      $('#id_email').val(profile.fields[0].email);
      $('#id_jabber').val(profile.fields[0].jabber);
      $('#id_skype').val(profile.fields[0].skype);
      $('#id_contacts').val(profile.fields[0].contacts);
      $('#id_bio').val(profile.fields[0].bio);

      unblockPage();
      var message = "<div id='goodmessage' class='col-xs-12" +
                    " bg-success prof_updated'>" +
                    "Changes have been save!</div><br><br>";
      $('.loader').before(message);
      setTimeout(function() {
        $('#goodmessage').remove();
        $('#content-column br').eq(0).remove();
        $('#content-column br').eq(0).remove();
        }, 3000);
		  },

  error: function(error){
      unblockPage();
		  console.log(error);
      }
	});
}

function fakeLoader() {
  blockPage();
  setTimeout(hardcodedUpdate, 2000);
}

