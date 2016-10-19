
var $initTitle = $('title').text();
var checkReqTmr; // timer for checking request's logs
var unread = 0;


function JsonRequests() {
  var currentUrl = location.href;

	$.ajax({
    type: 'GET',
    url: currentUrl,
	  cache: false,
	  success: function(data){
               var newContent;
            
               for (var i = 1; i <= data.length; i++) 
                 newContent += '<tr><td>' + i + '</td>' +
                               '<td>' + data[i-1].method + '</td>' +
                               '<td>' + data[i-1].path + '</td>' +
                               '<td>' + data[i-1].status_code + '</td>' +
                               '<td>' + data[i-1].date + '</td></tr>';
               
               $('#requests-content').html(newContent);
               unread++;
               $(document).attr("title", "(" + unread + ") unread");
    },

    error: function(xhr, status, error){
		    console.log(error);
    }
  });
}

window.onfocus = function() {
  clearTimeout(checkReqTmr);
  $('title').text($initTitle);
  unread = 0;
};

window.onblur = function() {
	checkReqTmr = setInterval(JsonRequests, 1500);
}
