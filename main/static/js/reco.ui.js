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
    loadMoviesFromServer("/movies/search", {query: query});
});


$("#movie-search-input").keyup(function (e) {
    if (e.keyCode == 13) {
        loadMoviesFromServer("/movies/search", {query: $(this).val()});
    }
});


$("#make-reco-btn").click(function() {

    var recoType = sessionStorage.getItem("reco-type");

    // General recommendation procedure does not required to receive
    // preferences, because it used all user's preferences already
    // stored in internal databases.
    var prefList = null;
    if (recoType == RECO.STANDALONE) {
        prefList = JSON.parse(sessionStorage.getItem("reco-pref"));
    }

    if (recoType == RECO.STANDALONE && prefList.length == 0) {
        alert(RECO.NOMOVIES_MSG);
    } else {
        $("#reco-status").show();
        $("#reco-status").html("Recommendation in progres ...");
        $.post(
            RECO.URL,
            JSON.stringify({
                type: recoType,
                prefs: prefList
            }),
            handleRecoResponse
        );
    }
});

/******************************************************************************/

/*******************************************************************************
    GLOBAL VARIABLES

*******************************************************************************/

var RECO = {
    EMPTY_MSG: "Unable to make recommendation on the base of your preferneces",
    NOMOVIES_MSG: "Please specifiy your preferences",
    STANDALONE: "standalone",
    GENERAL: "general",
    URL: "/make_reco"
};

/******************************************************************************/

/*******************************************************************************
    FUNCTIONS
*******************************************************************************/

function handleRecoResponse(response) {
    if (response.status == "OK") {
        var movies = response.movies;
        if (movies.length === 0) {
            $("#reco-status").show();
            $("#reco-status").html(RECO.EMPTY_MSG);
        } else {
            updateRecoList(movies);
            $("#reco-container").show();
            $("#reco-status").show();
            $("#reco-status").html("Recommendation complete.");
        }
    } else {
        alert("ERROR: DO STH WITH IT");
    }
}

function updateRecoList(movies) {
    var $recoList = $("#reco-list");
    $recoList.children("li").remove();
    for (var i = 0; i < movies.length; i++) {
        $recoList.append($("<li class='list-group-item'>" + 
            movies[i].title + "</li>")); 
    }
}

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
    if (data === undefined) data = {};

    loadInProgress = true;
    $("#state-msg").show();
    $("#state-msg").html("(Loading ...)");

    $.post(url, data)
    .done(function(response) {
        movies = response.movies;
        refreshMoviesList(movies);
        if (movies.length > 0) {
            $("#state-msg").hide();
        } else {
            $("#state-msg").show();
            $("#state-msg").html("(Empty list)");               
        }
        loadInProgress = false;

        if (response.page == 1) {
            $("#movies-list-prev").prop("disabled", true);
        } else {
            $("#movies-list-prev").prop("disabled", false);
        }

        if (response.page == response.total_pages) {
            $("#movies-list-next").prop("disabled", true);   
        } else {
            $("#movies-list-next").prop("disabled", false);
        }

    })
    .fail(function(errMsg) {
            alert(errMsg);
            loadInProgress = false;
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

function clearMoviesList() {
    $("#movies-list").empty();
    sessionStorage.setItem("reco-pref", JSON.stringify([]));
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
                sessionStorage.setItem("reco-pref", JSON.stringify(moviesArray));
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
    sessionStorage.setItem("reco-pref", JSON.stringify(moviesArray));
    return true;
}

function removeMovieFromList(id) {
    var moviesArray = getMoviesList();
    var id = id.toString();
    for(var i = 0; i < moviesArray.length; i++) {
        if (moviesArray[i].id == id) {
            moviesArray.splice(i, 1);
            sessionStorage.setItem("reco-pref", JSON.stringify(moviesArray));
            return true;
        }
    }
    return false;
}

function getMoviesList() {
    var moviesArray = sessionStorage.getItem("reco-pref");
    if (!moviesArray) {
        moviesArray = [];
        sessionStorage.setItem("reco-pref", JSON.stringify(moviesArray));
    } else {
        moviesArray = JSON.parse(moviesArray);
    }
    return moviesArray;
}

/******************************************************************************/