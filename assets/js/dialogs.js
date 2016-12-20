/*global $, _ */
$(function() {
    "use strict";

    var textarea = $('div#chat'), // place for messages
        input = $('input#input'), // input here new message
        btn_send = $('button[id=btn_send]'), // button to send message
        currentThread = $('#currentDialog'), // from the left-handed panel
        in_unload = false, // stop functions during page unloading
        //stopThread = false, // stop current thread
        recipient;

    //var now = moment();    // used for date_to_string function

    // Сurrent interlocutor for communication
    var currentPartner = input.data('sender');

    // Set to true when send message into another (not current) thread
    var changeDialog = false; 

    // value can be 'changeDialog' or 'currentDialog'
    var mode = 'currentDialog'; 

    // After chat loading create initial dictionaries 
    var initLMID = {}; // Last Message ID (LMID) for each thread
    var stopThread = {}; // stop status for each thread
   
    $('a.thread-link').each(function() {
        initLMID[$(this).data('partner')] = $(this).data('lastid');
        stopThread[$(this).data('partner')] = false;
    });

    // The dict currentLMID contains updated LMID during long polling
    var currentLMID = initLMID;

    /* Contains the current number of failed requests (for get_new_messages) in a row. */
    var failed_requests_in_a_row = 0;

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
            stopThread[currentPartner] = true;
        }
        console.log('mode: ' + mode);

        $.post('/send/', {

            'text': input.val(),
            'sender_id': input.data('senderid'),
            'recipient': recipient,
            'mode': mode

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

        textarea.html('');

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
            stopThread[recipient] = false;
            console.log('new thread created!');
        }

        currentPartner = recipient;
        changeDialog = false;

        // Start long polling with new thread
        setTimeout(get_new_messages, 500);
        input.focus();
    };


    /* Gets new messages from the server by initiating an AJAX POST-request.
     * If any new message(s) was found, some JSON in returned.
     * If no new message(s) was found, "OK" is returned.
     *
     * After 3 failed requests in a row, the loop is stopped.
     */
    var get_new_messages = function() {
        
        // Remember the receiver until the function is executed 
        var receiver = currentPartner;

        if (failed_requests_in_a_row >= 3) {
            add_error("Reached the max number of failed requests in a row.<br />" +
                      "Click <a href=\"javascript:$.retry_get_new_messages();\">Here</a> to try again!");
            return;
        }
        $.post('/get_new/', {
            'thread_id': currentThread.data('thread'),
            'last_id': currentLMID[currentPartner],
            'username': input.data('sender'),
            'receiver': receiver
 
        }, function(result) { 
 
           if (stopThread[receiver]) return;

           failed_requests_in_a_row = 0;

            if (result === 'OK') {
                // 'OK' is caused by long polling timeout.
                remove_spinner();
                return;
            }

            if (result === 'STOP') {
                // 'STOP' is caused when the user changes a thread.
                stopThread = true;
                remove_spinner();
                return;
            }

            // if the dialog has no new messages
            if (result.messages === []) {
                remove_spinner();
                currentLMID[currentPartner] = result.lastid;
                //add_senders(result.senders);
                return;
            }

            // if the dialog has new messages
            var messages = result.messages;          

            /* Convert ISO timestamps to javascript Date objects. */
            _.each(messages, function(message) {
                message.timestamp = moment(message.timestamp);
            });

            /* Try to parse and interpret the resulting json. */
            try {
                currentLMID[currentPartner] = result.lastid;
                //add_senders(result.senders);
                add_messages(result.messages);
                remove_spinner();
            } catch (e) {
                add_error(e);
            }

        }).fail(function(data) {

            if (stopThread[receiver]) return;

            /* A fail has happened, increment the counter. */
            failed_requests_in_a_row += 1;

            /* Format the error string into something readable, instead of [Object object]. */
            var failed_string = data.status + ": " + data.statusText;
            add_error(failed_string);

            /* Seems to happen on hibernate, the request will restart. */
            if (data.status === 0) return;

        }).always(function() {

            /* Get new messages even when the previous request failed. */
            if (stopThread[receiver]) stopThread[receiver] = false;
            else setTimeout(get_new_messages, 500);
        });
    };


    // convert timestamp to date in JavaScript
    var date_to_string = function(date) {
        var now = moment(); // moment.min.js
        if (now.year() === date.year()) {
            if (now.month() === date.month() && now.date() === date.date()) {
                return date.format('HH:mm');
            } else {
                return date.format('MM-DD HH:mm');
            }
        } else {
            return date.format('YYYY-MM-DD HH:mm');
        }
    };


    // Renders JSON messages to HTML and appends to the existing messages.
    var add_messages = function(messages) {
        if (in_unload)
            return;
        // Convert date objects to string repressentations.
        _.each(messages, function(message) {
            message.formatted_timestamp = date_to_string(message.timestamp);
        });
        // Render the template using underscore.
        var rendered_messages = _.template(
            '<% _.each(messages, function(message) { %>' +
                '<span class="time">[<%= message.formatted_timestamp %>] </span>' +
                '<span class="username"><%= message.username %>:</span> ' +
                '<span class="message"><%= message.message %></span><br />' +
                '<% }); %>')({
            messages: messages
        });
        textarea.append(rendered_messages);
        textarea.scrollTop(textarea[0].scrollHeight);
    };


    /* Called by the user, if he/she wants to try and get new messages again
     * after the limit (failed_requests_in_a_row) has been exceeded.
     */
    $.retry_get_new_messages = function() {
        failed_requests_in_a_row = 0;
        setTimeout(get_new_messages, 500);
    };


});
