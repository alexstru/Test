
var $initTitle = $('title').text();
var checkReqTmr; // timer for checking request's logs
var unread = 0;
var focused = 0;


function toDate(dateStr) {  
 // convert "yyyy-mm-dd hh:mm:ss" string to date

		var dateOptions = {
			month:  'short',
			day:    'numeric',
			year:   'numeric',
			hour:   '2-digit',
			minute: '2-digit',
			second: '2-digit',
		};

    var yyyymmdd = dateStr.substring(0, 10);
    var time = dateStr.substring(11, 19);
    var dateArray = yyyymmdd.split("-");
    var timeArray = time.split(":");

    result = new Date(
                      dateArray[0], 
                      dateArray[1] - 1, 
                      dateArray[2],
                      timeArray[0],
                      timeArray[1],
                      timeArray[2]
                 );

    var now = new Date();
    result.setHours(result.getHours() - now.getTimezoneOffset()/60);

    return result.toLocaleString("en-US", dateOptions);
}


function JsonRequests() {
  var currentUrl = location.href;

	$.ajax({
    type: 'GET',
    url: currentUrl,
	  cache: false,
    dataType: 'json',

	  success: function(data){

        /* AJAX get data in JSON like that:
        {"dbcount": 701, 
         "reqlogs": [
                    {"date": "2016-09-16 09:20:19.098777+00:00", 
                     "path": "http://localhost:8000/request/", 
                     "status_code": 200, 
                     "id": 701, 
                     "method": "GET"}, 
                    .....
                    {"date": "2016-09-16 09:20:12.355412+00:00", 
                     "path": "http://localhost:8000/admin/", 
                     "status_code": 200, 
                     "id": 700, 
                     "method": "GET"}
                    ]
        }*/

               var newContent;
               for (var i = 1; i <= data.reqlogs.length; i++) 
                 newContent += '<tr><td>' + i + '</td>' +
                               '<td>' + data.reqlogs[i-1].method + '</td>' +
                               '<td>' + data.reqlogs[i-1].path + '</td>' +
                               '<td>' + data.reqlogs[i-1].status_code + '</td>' +
                               '<td>' + toDate(data.reqlogs[i-1].date) + '</td></tr>';

               $('#requests-content').html(newContent);
               if (!focused) {              
                 unread++;
                 $(document).attr("title", "(" + unread + ") unread");
               }
    },

    error: function(xhr, status, error){
		    console.log(error);
    }
  });
}


window.onfocus = function() {
  focused = 1;
  clearTimeout(checkReqTmr);
  $('title').text($initTitle);
  unread = 0;
};


window.onblur = function() {
  focused = 0;
	checkReqTmr = setInterval(JsonRequests, 1500);
}
