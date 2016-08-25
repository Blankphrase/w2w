/*******************************************************************************
    LOAD MOVIES
*******************************************************************************/

loadMovies("movies/browse/page/1");

var moviesList = getMoviesList();
var $prefList = $("#pref-list");
for (var i = 0; i < moviesList.length; i++) {
    $prefItem = $("<li></li>").data("movie-id", moviesList[i].tmdb_id).html(
        moviesList[i].title
    );
    $prefList.append($prefItem);
}

/******************************************************************************/

/*******************************************************************************
    EVENTS HANDLERS
*******************************************************************************/

$(document).on("change", ".movie-item-checkbox", function() {
    var $prefList = $("#pref-list");
    var $prefItem = undefined;

    if ($(this).is(':checked')) {
        $prefItem = $("<li></li>").data("movie-id", $(this).val()).html(
            $(this).next().html()
        );
        $prefList.append($prefItem);
        addMovieToList($(this).val(), $(this).next().html(), 10);
    } else {
        var movieId = $(this).val();
        $prefList.children("li").filter(function() {
            return $(this).data("movie-id") == movieId; 
        }).remove();
        removeMovieFromList($(this).val());
    }
});

$("#movies-list-next").click(function() {
    loadMovies("/movies/browse/next");
});

$("#movies-list-prev").click(function() {
    loadMovies("/movies/browse/prev");
});

/******************************************************************************/

/*******************************************************************************
    FUNCTIONS
*******************************************************************************/

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
            movies[i].tmdb_id + "' " + 
            (findInMovieList(movies[i].tmdb_id) >= 0 ? "checked" : "") +
            ">");
        $movieItem.append("<span class='movie-item-title'>" +
            movies[i].title + "</span>");
        $moviesList.append($movieItem);
    }   
}

function findInMovieList(tmdb_id) {
    var moviesArray = getMoviesList();
    tmdb_id = tmdb_id.toString();
    for (var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].tmdb_id == tmdb_id) {
            return i;
        }
    }
    return -1;
}

function addMovieToList(tmdb_id, title, favour) {
    if (favour === undefined) favour = 10

    var moviesArray = getMoviesList();
    tmdb_id = tmdb_id.toString();
    for (var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].tmdb_id == tmdb_id) 
            return false;
    }
    moviesArray.push({"tmdb_id": tmdb_id, "title": title, "favor": favour});
    localStorage.setItem("moviesArray", JSON.stringify(moviesArray));
    return true;
}

function removeMovieFromList(tmdb_id) {
    var moviesArray = getMoviesList();
    tmdb_id = tmdb_id.toString();
    for(var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].tmdb_id == tmdb_id) {
            moviesArray.splice(i, 1);
            localStorage.setItem("moviesArray", JSON.stringify(moviesArray));
            return true;
        }
    }
    return false;
}

function getMoviesList() {
    var moviesArray = localStorage.getItem("moviesArray");
    if (!moviesArray) {
        moviesArray = [];
        localStorage.setItem("moviesArray", JSON.stringify(moviesArray));
    } else {
        moviesArray = JSON.parse(moviesArray);
    }
    return moviesArray;
}

/******************************************************************************/