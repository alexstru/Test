
var $initTitle = $('title').text();


window.onfocus = function() {
  $('title').text($initTitle);
};


