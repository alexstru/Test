
var $initTitle = $('title').text();
var checkReqTmr; // timer for checking request's logs
var unread = 0;


window.onfocus = function() {
  clearTimeout(checkReqTmr);
  $('title').text($initTitle);
  unread = 0;
};

window.onblur = function() {
	checkReqTmr = setInterval(function() {
      unread++;
      $(document).attr("title", "(" + unread + ") unread");
    }, 1500);
}

