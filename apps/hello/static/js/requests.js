
var onLoadRequestsDB = 0; // get requests count in DB after window.onload
var ajaxRequestsDB = 0;   // get requests count in DB after current AJAX
var firstAJAX = false;    // init first ajax after loading request.html
var checkReqTmr;          // timer for checking request's logs
var sortingURL = '';
var sortingMode = false;

var $initTitle = $('title').text();
var $pSlider, $btnSetPriority, $btnBackPriority, $lastLink;


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
        $('a').attr('disabled', 'disabled');
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
            'id="priority_' + data.reqlogs[i-1].id + 
            '" data-request-id="' + data.reqlogs[i-1].id + '">' + 
            data.reqlogs[i-1].priority + '</a>  ' +
            '<select style="display: none;" ' +
            'data-request-id="' + data.reqlogs[i-1].id + '">' +
            '</select></td></tr>';

		    $('#requests-content').html(newContent);
        $('a').removeAttr('disabled');
    },

    error: function(xhr, status, error){
        $('a').removeAttr('disabled');
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


$(document).ready(function(){
  $('#content-column').attr('style', 'background: #FBEFF2');
 
  localStorage.setItem('synchronizePages', true);
  firstAJAX = true;
  sortingURL = location.href;
  sortingMode = false;
  JsonRequests();

  $('#slider').slider({
        'id': 'pSlider',
        'min': -65536,
        'max': 65536,
        'step': 1,
        'value': 1
    });

  $pSlider = $('#pSlider');
  $btnSetPriority = $('#btnSetPriority');
  $btnBackPriority = $('#btnBackPriority');
  $pSlider.hide();
  $lastLink = $pSlider;


  $btnBackPriority.click(function() {
    $('#pSlider, #btnSetPriority, #btnBackPriority').hide();
    $lastLink.show();
  });


  $btnSetPriority.click(function() {
    $('#pSlider, #btnSetPriority, #btnBackPriority').hide();
    $('#content-column').prepend($pSlider, $btnSetPriority, $btnBackPriority);
    $lastLink.show();
    
		$.ajax({
			'url': location.href,
			'type': 'POST',
			'dataType': 'json',
			'data': {
				'pk': $lastLink.data('request-id'),
				'priority': $('#slider').slider().data('slider').getValue(),
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

});


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

  $('#pSlider, #btnSetPriority, #btnBackPriority').hide();
  $('#content-column').prepend($pSlider, $btnSetPriority, $btnBackPriority);
};


$(document).on('click', 'a.priority', function() {
  $(this).hide();
  $(this).after($btnBackPriority, $pSlider, $btnSetPriority);
  $('#slider').slider().data('slider').setValue($(this).text());
  $('#btnBackPriority, #pSlider, #btnSetPriority').show();

  if (!$(this).is($lastLink)) {
    $lastLink.show();
  }

  $lastLink = $(this);
  return false;
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


