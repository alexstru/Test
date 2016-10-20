
var onLoadRequestsDB = 0; // get requests count in DB after window.onload
var ajaxRequestsDB = 0;   // get requests count in DB after current AJAX
var firstAJAX = false;    // init first ajax after loading request.html
var checkReqTmr;          // timer for checking request's logs

var $initTitle = $('title').text();


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
	$.ajax({
    type: 'GET',
    url: location.href,
	  cache: false,
    dataType: 'json',

	  success: function(data, status, xhr){
		    var newContent;
		    ajaxRequestsDB = data.dbcount;
		   
		    if (firstAJAX) {
		       onLoadRequestsDB = ajaxRequestsDB;
		       firstAJAX = false;
		    }

		    var unreadRequests = ajaxRequestsDB - onLoadRequestsDB;

		    if (!unreadRequests) {
		      $('title').text($initTitle);
		    } else {
		      $('title').text("(" + unreadRequests + ") unread");
		    }

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

		    for (var i = 1; i <= data.reqlogs.length; i++) 
		      newContent += '<tr><td>' + i + '</td>' +
		        '<td>' + data.reqlogs[i-1].method + '</td>' +
		        '<td>' + data.reqlogs[i-1].path + '</td>' +
		        '<td>' + data.reqlogs[i-1].status_code + '</td>' +
		        '<td>' + toDate(data.reqlogs[i-1].date) + '</td></tr>';

		    $('#requests-content').html(newContent);
    },

    error: function(xhr, status, error){
		    console.log(error);
    }
  });
}


window.onload = function() {
  firstAJAX = true;
  JsonRequests();
};


window.onfocus = function() {
  clearTimeout(checkReqTmr);
  $('title').text($initTitle);
  onLoadRequestsDB = ajaxRequestsDB;
};

window.onblur = function() {
  checkReqTmr = setInterval(JsonRequests, 1500);
};
