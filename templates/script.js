$(document).ready(function() {
    $("#start-button").click(function() {
        $.post('/start_game', function(data) {
            $('#word-display').text(data.word);
            $('#submit-button').prop('disabled', false);
        });
    });

    $("#submit-button").click(function() {
        var userTypedWord = $('#user-input').val().toLowerCase();
        $.post('/check_word', {'user_typed_word': userTypedWord}, function(data) {
            if (data.correct) {
                alert('Correct! Well done.');
            } else {
                alert('Incorrect. The correct word is: ' + data.correct_word);
            }
            $('#start-button').prop('disabled', false);
            $('#submit-button').prop('disabled', true);
        });
    });
});
