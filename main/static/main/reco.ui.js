// User clicks checkbox.

$(document).on("change", ".movie-item-checkbox", function() {
    var $prefList = $("#pref-list");
    var $prefItem = undefined;

    if ($(this).is(':checked')) {
        $prefItem = $("<li></li>").data("movie-id", $(this).val()).html(
            $(this).next().html()
        );
        $prefList.append($prefItem);
    } else {
        var movieId = $(this).val();
        $prefList.children("li").filter(function() {
            return $(this).data("movie-id") == movieId; 
        }).remove();
    }
});

$("#movies-list-next").click(function() {
    loadMovies("/movies/browse/next");
});

$("#movies-list-prev").click(function() {
    loadMovies("/movies/browse/prev");
});


function loadMovies(url, data) {
    $("#state-msg").show();
    $("#state-msg").html("Loading ...");
    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(movies) {
            if (movies.length > 0) {
                updateMoviesList(movies);
                $("#state-msg").hide();
            } else {
                $("#state-msg").show();
                $("#state-msg").html("No more movies.");               
            }
        },
        failure: function(errMsg) {
            alert(errMsg);
        }
    });   
}


function updateMoviesList(movies) {
    var $moviesList = $("#movies-list");
    $moviesList.empty();
    for (var i = 0; i < movies.length; i++) {
        var $movieItem = $("<li class='movie-item'></li>");
        $movieItem.append("<input class='movie-item-checkbox' " + 
            "type='checkbox' name='movie' value='" + 
            movies[i].tmdb_id + "'>");
        $movieItem.append("<span class='movie-item-title'>" +
            movies[i].title + "</span>");
        $moviesList.append($movieItem);
    }   
}