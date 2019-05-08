$("#id_search").click(function () {
    var username = $(this).val();

    $.ajax({
        url: '{% url "search_user_ajax" %}',
        data: {
            'username': username
        },
        dataType: 'json',
        success: function (data) {
            if (data.username) {
                $('#result_search').html('<img src=' + data.avatar_url + ' width=50> <p>' + data.username + '</p>')
            }
            else {
                $('#result_search').html('<p>...</p>')
            }
        },
        error: function (request, status, error) {
            alert(request.responseText);
        }
    });
});