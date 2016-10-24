
var onLoadRequestsDB = 0; // get requests count in DB after window.onload
var ajaxRequestsDB = 0;   // get requests count in DB after current AJAX
var firstAJAX = false;    // init first ajax after loading request.html
var checkReqTmr;          // timer for checking request's logs
var sortingURL = '';
var sortingMode = false;

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
    url: sortingURL,
	  cache: false,
    dataType: 'json',

    beforeSend: function(xhr, settings){
        if (sortingURL == location.href) {
          $('a.sort span').hide();
          $('span#defaultDate').show();
          $('span#defaultPriority').show();
        } else {
          sortingMode = true;
        }
        console.log('sortingURL: ' + sortingURL);
    },

	  success: function(data, status, xhr){

        console.log('info from json: ' + data.info);

        if (!sortingMode) {
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
        } else {
          sortingMode = false;
        }

        /* AJAX get data in JSON like that:

        {"dbcount": 701, 
         "reqlogs": [
                    {"date": "2016-09-16 09:20:19.098777+00:00", 
                     "path": "http://localhost:8000/request/", 
                     "status_code": 200, 
                     "priority": 0, 
                     "id": 701, 
                     "method": "GET"}, 
                    .....
                    {"date": "2016-09-16 09:20:12.355412+00:00", 
                     "path": "http://localhost:8000/admin/", 
                     "status_code": 200, 
                     "priority": 1,
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
		        '<td>' + toDate(data.reqlogs[i-1].date) + '</td>' +
            '<td style="text-align: center;">' +
            '<a class="priority" href="" ' + 
            'id="priority_' + data.reqlogs[i-1].id + '">' + 
            data.reqlogs[i-1].priority + '</a>  ' +
            '<select style="display: none;" ' +
            'data-request-id="' + data.reqlogs[i-1].id + '">' +
            '<option value="0">0</option><option value="1">1</option>' +
            '<option value="2">2</option><option value="3">3</option>' +
            '<option value="4">4</option><option value="5">5</option>' +
            '<option value="6">6</option><option value="7">7</option>' +
            '<option value="8">8</option><option value="9">9</option>' +
            '</select></td></tr>';

		    $('#requests-content').html(newContent);
    },

    error: function(xhr, status, error){
		    console.log(error);
    }
  });
}


window.addEventListener("storage", function() {
  if (localStorage.synchronizePages == 'true') {
      firstAJAX = true;
      JsonRequests();
    } else if (localStorage.synchronizeInitTitle == 'true') {
      clearTimeout(checkReqTmr);
      $('title').text($initTitle);
      onLoadRequestsDB = ajaxRequestsDB;
    } else if ((localStorage.synchronizePages == 'false') && 
               (localStorage.synchronizeInitTitle == 'false')) {
      checkReqTmr = setInterval(JsonRequests, 1500);
  }
}, false);


window.onload = function() {
  localStorage.setItem('synchronizePages', true);
  firstAJAX = true;
  sortingURL = location.href;
  sortingMode = false;
  JsonRequests();
};


window.onfocus = function() {
  localStorage.setItem('synchronizeInitTitle', true);
  clearTimeout(checkReqTmr);
  $('title').text($initTitle);
  onLoadRequestsDB = ajaxRequestsDB;
};


window.onblur = function() {
  localStorage.setItem('synchronizePages', false);
  localStorage.setItem('synchronizeInitTitle', false);
  checkReqTmr = setInterval(JsonRequests, 1500);
};


$(document).on('click', 'a.priority', function() {
  $prioritySelector = $(this).parent().find('select').val($(this).text());
  $prioritySelector.attr('size', 10).show();
  return false;
});


$(document).on('change', 'select', function() {
  $(this).hide();

		$.ajax({
			'url': location.href,
			'type': 'POST',
			'dataType': 'json',
			'data': {
				'pk': $(this).data('request-id'),
				'priority': $(this).val(),
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			'error': function(xhr, status, error){
				alert(error);
			},
			'success': function(data, status, xhr){
				$(data.link_id).text(data.priority);
			}
		});
});


$('a.sort').click(function() {
/* AJAX sorting requests by priority or date  */

  $('a.sort span').hide();

  if ($(this).is('#dateColumn')) {

    $('span#defaultPriority').show();

    if (sortingURL.contains("?date=0")) {
      sortingURL = location.href + '?date=1';
      $('span#oldestDate').show();
    } else if(sortingURL.contains("?date=1")) {
      sortingURL = location.href + '?date=0';
      $('span#newestDate').show();
    } else {
      sortingURL = location.href + '?date=0';
      $('span#newestDate').show();
    }
  } 

  if ($(this).is('#priorityColumn')) {

    $('span#defaultDate').show();

    if (sortingURL.contains("?priority=0")) {
      sortingURL = location.href + '?priority=1';
      $('span#highPriority').show();
    } else if(sortingURL.contains("?priority=1")) {
      sortingURL = location.href + '?priority=0';
      $('span#lowPriority').show();
    } else {
      sortingURL = location.href + '?priority=1';
      $('span#highPriority').show();
    }
  }

  JsonRequests();
  return false;
});

