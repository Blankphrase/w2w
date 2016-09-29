/*******************************************************************************
    EVENTS HANDLERS
*******************************************************************************/

$(document).on("change", ".movie-item-checkbox", function() {
    if ($(this).is(':checked')) {
        prefsList.add(
            movieId = $(this).val(), 
            movieTtile = $(this).next().html(),
            movieRating = 10, // set be default highest possible rating
            callback = function() {
                prefsList.refresh();
            }
        );
    } else {
        prefsList.remove(
            movieId = $(this).val(),
            callback = function() {
                prefsList.refresh();
            }
        );
    }
});

var loadInProgress = false;
$("#movies-list-next").click(function() {
    // if (!loadInProgress) loadMoviesFromServer("/movies/next");
    moviesList.next();
});

$("#movies-list-prev").click(function() {
    // if (!loadInProgress) loadMoviesFromServer("/movies/prev");
    moviesList.prev();
});

$("#prefs-list-next").click(function() {
    prefsList.nextPage();
    var items = prefsList.refresh();
    if (items == 0) {
        prefsList.prevPage();
    }
});

$("#prefs-list-prev").click(function() {
    prefsList.prevPage();
    var items = prefsList.refresh();
});

$("#clear-my-prefs").click(function() {
    if (confirm("Are your sure you want to clear all your preferences?")) {
        prefsList.clear();
    }
});

$(document).on("change", ".pref-item-rating", function() {
    var movieId = $(this).parent().parent().data("movie-id");
    var rating = $(this).val();
    var title = $(this).parent().parent().find(".pref-item-title").html();
    prefsList.update(movieId, title, rating, function() {
        prefsList.refresh();
    });
});

$(document).on("click", ".pref-item-remove", function() {
    var movieId = $(this).parent().data("movie-id");

    $(".movie-item").filter(function() {
        return $(this).data("movie-id") == movieId
    }).find("input").prop("checked", false);
    prefsList.remove(movieId, function() {
        prefsList.refresh();
    });
});

$("#movie-search-button").click(function() {
    var query = $("#movie-search-input").val();
    moviesList.search(query);
});


$("#movie-search-input").keyup(function (e) {
    if (e.keyCode == 13) {
        // loadMoviesFromServer("/movies/search", {query: $(this).val()});
        moviesList.search($(this).val());
    }
});

$("#make-reco-btn").click(function() {
    // General recommendation procedure does not required to receive
    // preferences, because it used all user's preferences already
    // stored in internal databases.
    var prefList = null;
    if (recoType == RECO.STANDALONE) {
        prefList = prefsList.getArray();
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
// Movies List
/******************************************************************************/

moviesList.on("onLoad", function() {
    $("#state-msg").show();
    $("#state-msg").html("(Loading ...)");    
});

moviesList.on("onLoaded", function(response) {
    movies = response.movies;
    createMoviesList(movies);
    if (movies.length > 0) {
        $("#state-msg").hide();
    } else {
        $("#state-msg").show();
        $("#state-msg").html("(Empty list)");               
    }

    $("#movies-list-prev").prop("disabled", false);
    $("#movies-list-next").prop("disabled", false);
    if (response.page == 1) {
        $("#movies-list-prev").prop("disabled", true);
    }
    if (response.page == response.total_pages) {
        $("#movies-list-next").prop("disabled", true);  
    }

});

function createMoviesList(movies) {
    var $moviesList = $("#movies-list");
    $moviesList.empty();
    for (var i = 0; i < movies.length; i++) {
        var $movieItem = $("<li class='movie-item list-group-item col-xs-4'></li>")
            .data("movie-id", movies[i].id);
        $movieItem.append("<input class='movie-item-checkbox' " + 
            "type='checkbox' name='movie' value='" + movies[i].id + "'>");
        $movieItem.append("<span class='movie-item-title'>" +
            movies[i].title + "</span>");
        $moviesList.append($movieItem);
    }   
}

function alignMoviesListWithUserPrefs() {
    var $movies = $("#movies-list > li input");
    for(var i = 0; i < $movies.length; i++) {
        var movieId = $($movies[i]).val();
        if (prefsList.contains(movieId)) {
            $($movies[i]).prop("checked", true);
        } else {
            $($movies[i]).prop("checked", false);
        }
    }
}

/******************************************************************************/

/*******************************************************************************
    settings
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
    reco-list
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

/******************************************************************************/