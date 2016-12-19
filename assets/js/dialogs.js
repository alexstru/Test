/*global $, _ */
$(function() {
    "use strict";

    var textarea = $('div#chat'), // place for messages
        input = $('input#input'), // input here new message
        btn_send = $('button[id=btn_send]'), // button to send message
        currentThread = $('#currentDialog'), // from the left-handed panel
        in_unload = false, // stop functions during page unloading
        recipient;

    //var now = moment();    // used for date_to_string function

    // Сurrent interlocutor for communication
    var currentPartner = input.data('sender');

    // Set to true when send message into another (not current) thread
    var changeDialog = false; 

    // value can be 'changeDialog' or 'currentDialog'
    var mode = 'currentDialog'; 

    /* After chat loading create initial dictionary 
     * with Last Message ID (LMID) for each thread
     */
    var initLMID = {};
    $('a.thread-link').each(function() {
        initLMID[$(this).data('partner')] = $(this).data('lastid');
        //console.log(initLMID[$(this).data('partner')]);
    });

    // The dict currentLMID contains updated LMID during long polling
    var currentLMID = initLMID;

    // make sure AJAX-requests send the CSRF cookie, or the requests will be rejected.
    var csrftoken = $('input[type=hidden][name=csrfmiddlewaretoken]').val();

    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    });


    // stop functions during page unloading
    $(window).bind('beforeunload', function() {
        in_unload = true;
    });

    // hide loader image
    var remove_spinner = function() {
        if (textarea.hasClass('spinner'))
            textarea.removeClass('spinner');
    };

    remove_spinner();
    input.focus();


    // Click handler for Send button.
    btn_send.click(function(event) {

        event.preventDefault();
        btn_send.addClass('disabled');

        recipient = $('#recipient-select').val();
       
        if (recipient !== currentPartner) {
            changeDialog = true;
            mode = 'changeDialog';
        }
        console.log('mode: ' + mode);

        $.post('/send/', {

            'text': input.val(),
            'sender_id': input.data('senderid'),
            'recipient': recipient,
            'mode': mode,
            'prev_thread_id': currentThread.data('thread')

        }, function(data, status, xhr) {

            if (xhr.getResponseHeader('content-type') === 'application/json')
                if (changeDialog) switch_to_another_chat(data);
                else add_error("Invalid message: " + data.text[0]);

            input.val('');
            input.focus();

        }).fail(function(data) {

            // Show the response text as plaintext.
            var status = data.status;
            var statusText = data.statusText;

            // If we've hit a 400 (Bad Request), show the responseText.
            if (status === 400) statusText += ": " + data.responseText;
            add_error(status + " " + statusText);

        }).always(function() {

            btn_send.removeClass('disabled');
            mode = 'currentDialog';
        });
        return false;
    });


    // handle enter in the input field to click the "Send" button.
    input.keypress(function(event) {
        if (event.which === 13) {
            event.preventDefault();
            btn_send.click();
            return false;
        }
        return true;
    });


    // Display error after bad request
    var add_error = function(data) {
        if (in_unload)
            return;
        var line = '<span class="error"><span class="bold">Error</span>:<br /><pre>' +
            data + '</pre></span>';
        textarea.append(line);
        textarea.scrollTop(textarea[0].scrollHeight);
    };


    // Correct HTML after dialog changing
    var switch_to_another_chat = function(data) {
        if (in_unload)
            return;

        // This happens when the user sends an incorrect message after page loading
        if(data.hasOwnProperty('text')) {
            add_error("Invalid message: " + data.text[0]);
            return;
        }

        var rendered_threads = _.template(
            '<% _.each(threads, function(thread) { %>' +
                '<a class="thread-link" ' +
                'data-thread="<%= thread.thread %>" ' +
                'data-partner="<%= thread.partner %>" ' + 
                'data-lastid="<%= thread.lastid %>"> ' + 
                '<%= thread.partner %> (<%= thread.lastid %>)</a><br><% }); %>')({
            threads: data.threads
        });

        //console.log(rendered_threads);
        $('div#threads').html(rendered_threads);

        var copy = $('a.thread-link[data-partner=' +recipient+ ']');
        copy.addClass('bold');

        currentThread.text(recipient);
        currentThread.data('thread', copy.data('thread'));
        currentThread.data('partner', copy.data('partner'));
        currentThread.data('lastid', copy.data('lastid'));

        if (data.new_thread == 'new') {
            initLMID[recipient] = copy.data('lastid');
            currentLMID[recipient] = copy.data('lastid');
            console.log('new thread created!');
        }

        currentPartner = recipient;
        changeDialog = false;

        // Start long polling with new thread
        //setTimeout(get_new_messages, 1000);
        input.focus();
    };


});
