/*******************************************************************************
    EVENTS HANDLERS
*******************************************************************************/

$(document).on("change", ".movie-item-checkbox", function() {
    if ($(this).is(':checked')) {
        addToPrefList($(this).val(), $(this).next().html());
        addMovieToList($(this).val(), $(this).next().html(), 10);
    } else {
        removeFromPrefList($(this).val());
        removeMovieFromList($(this).val());
    }
});

var loadInProgress = false;
$("#movies-list-next").click(function() {
    if (!loadInProgress) loadMoviesFromServer("/movies/next");
});

$("#movies-list-prev").click(function() {
    if (!loadInProgress) loadMoviesFromServer("/movies/prev");
});

$("#clear-my-prefs").click(function() {
    var moviesList = getMoviesList();
    var movieId;

    for (var i = 0; i < moviesList.length; i++) {
        movieId = moviesList[i].id;
        $(".movie-item").filter(function() {
            return $(this).data("movie-id") == movieId
        }).find("input").prop("checked", false);
        removeFromPrefList(movieId);
        removeMovieFromList(movieId);        
    }
});

$(document).on("change", ".pref-item-rating", function() {
    var movieId = $(this).parent().parent().data("movie-id");
    var rating = $(this).val();
    updateMovieRating(movieId, rating);
});

$(document).on("click", ".pref-item-remove", function() {
    var movieId = $(this).parent().data("movie-id");

    $(".movie-item").filter(function() {
        return $(this).data("movie-id") == movieId
    }).find("input").prop("checked", false);
    removeFromPrefList(movieId);
    removeMovieFromList(movieId);   
});

$("#movie-search-button").click(function() {
    var query = $("#movie-search-input").val();
    $.ajax({
        type: "POST",
        url: "/movies/search",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify({query: query}),
        success: function(movies) {
            refreshMoviesList(movies);    
        }
    });
});

/******************************************************************************/

/*******************************************************************************
    FUNCTIONS
*******************************************************************************/

function addToPrefList(movieId, movieTitle, movieRating) {
    if (movieRating === undefined) movieRating = 10

    var $prefList = $("#pref-list");
    var $prefItem = $("<li class='list-group-item col-xs-4'></li>").data("movie-id", movieId);
    $prefItem.append($("<span class='pref-item-title'></span>")
        .html(movieTitle));
    var $ratingForm = $("<form></form>");
    for(var i = 1; i <= 10; i++) {
        $ratingForm.append("<input type='radio' name='movie_" + movieId + "' " +
            "value='" + i + "' " + (i == movieRating ? "checked": "") + " " +
            "class='pref-item-rating'>" + i + "");
    }
    $prefItem.append($ratingForm);
    $prefItem.append($("<button class='pref-item-remove' type='button'>Remove</button>"));
    $prefList.append($prefItem);
}

function removeFromPrefList(movieId) {
    var $prefList = $("#pref-list");
    $prefList.children("li").filter(function() {
        return $(this).data("movie-id") == movieId; 
    }).remove();
}

function loadMoviesFromServer(url, data) {
    loadInProgress = true;
    $("#state-msg").show();
    $("#state-msg").html("(Loading ...)");
    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            movies = response.movies;
            if (movies.length > 0) {
                refreshMoviesList(movies);
                $("#state-msg").hide();
            } else {
                $("#state-msg").show();
                $("#state-msg").html("(No more movies)");               
            }
            loadInProgress = false;
        },
        failure: function(errMsg) {
            alert(errMsg);
            loadInProgress = false;
        }
    });   
}

function refreshMoviesList(movies) {
    var $moviesList = $("#movies-list");
    $moviesList.empty();
    for (var i = 0; i < movies.length; i++) {
        var $movieItem = $("<li class='movie-item list-group-item col-xs-4'></li>").data("movie-id", 
            movies[i].id);
        $movieItem.append("<input class='movie-item-checkbox' " + 
            "type='checkbox' name='movie' value='" + 
            movies[i].id + "' " + 
            (findInMoviesList(movies[i].id) >= 0 ? "checked" : "") +
            ">");
        $movieItem.append("<span class='movie-item-title'>" +
            movies[i].title + "</span>");
        $moviesList.append($movieItem);
    }   
}

function findInMoviesList(id) {
    var moviesArray = getMoviesList();
    id = id.toString();
    for (var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].id == id) {
            return i;
        }
    }
    return -1;
}

function updateMovieRating(id, rating) {
    var moviesArray = getMoviesList();
    var id = id.toString();
    for (var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].id == id) {
                moviesArray[i].rating = rating;
                localStorage.setItem("moviesArray", JSON.stringify(moviesArray));
                return true;                
        }
    }    
    return false;
}

function addMovieToList(id, title, rating) {
    if (rating === undefined) rating = 10

    var moviesArray = getMoviesList();
    id = id.toString();
    for (var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].id == id) {
                return false;                
        }
    }
    moviesArray.push({"id": id, "title": title, "rating": rating});
    localStorage.setItem("moviesArray", JSON.stringify(moviesArray));
    return true;
}

function removeMovieFromList(id) {
    var moviesArray = getMoviesList();
    var id = id.toString();
    for(var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].id == id) {
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