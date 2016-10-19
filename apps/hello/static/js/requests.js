
var $initTitle = $('title').text();
var checkReqTmr; // timer for checking request's logs
var unread = 0;

var content = '';
for(var num = 1; num <= 10; num++) {
  content += '<tr><td>' + num + '</td>' + 
             '<td>GET</td>' +
             '<td>/request/</td>' + 
             '<td>200</td>' +
						 '<td>October 19, 2016, 09:30 a.m.</td></tr>';
}

function FakeRequests() {
	$.ajax({
	url: $(this).attr("href"),
	cache: false,
	success: function(data){
           $('#requests-content').html(content);
           unread++;
           $(document).attr("title", "(" + unread + ") unread");
					 }
	});
}

window.onfocus = function() {
  clearTimeout(checkReqTmr);
  $('title').text($initTitle);
  unread = 0;
};

window.onblur = function() {
	checkReqTmr = setInterval(FakeRequests, 1500);
}

