/******************************************************************************/
// Movies List
/******************************************************************************/

$(document).on("change", ".movie-item-checkbox", function() {
    if ($(this).is(':checked')) {
        prefsList.update(
            movieId = $(this).val(), 
            movieTtile = $(this).next().html(),
            movieRating = 10 // set be default highest possible rating       
        );
    } else {
        prefsList.remove(movieId = $(this).val());
    }
});

$("#movies-list-next").click(function() {
    moviesList.next();
});

$("#movies-list-prev").click(function() {
    moviesList.prev();
});

moviesList.on("onLoad", function() {
    $("#state-msg").show();
    $("#state-msg").html("(Loading ...)");    
});

moviesList.on("onLoaded", function(response) {
    movies = response.movies;
    if (movies.length > 0) {
        createMoviesList(movies);
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
// Prefs List
/******************************************************************************/

$("#prefs-list-next").click(function() {
    prefsList.nextPage();
});

$("#prefs-list-prev").click(function() {
    prefsList.prevPage();
});

$("#clear-my-prefs").click(function() {
    if (confirm("Are your sure you want to clear all your preferences?")) {
        clearPrefsList();
    }
});

$(document).on("change", ".pref-item-rating", function() {
    var movieId = $(this).parent().parent().data("movie-id");
    var rating = $(this).val();
    var title = $(this).parent().parent().find(".pref-item-title").html();
    prefsList.update(movieId, title, rating);
});


$(document).on("click", ".pref-item-remove", function() {
    var movieId = $(this).parent().data("movie-id");

    $(".movie-item").filter(function() {
        return $(this).data("movie-id") == movieId
    }).find("input").prop("checked", false);
    prefsList.remove(movieId);
});

prefsList.on("onUpdate", function() {
    refreshPrefsList(prefsList.getCurrentPage());
});

prefsList.on("onRemove", function(movieId) {
    var items = prefsList.getCurrentPage();
    // if removal of item leads to empty page than skip to previous page
    if (items.length == 0) {
        prefsList.prevPage(noCallback = true);
        items = prefsList.getCurrentPage();
    } 
    refreshPrefsList(items);
});

prefsList.on("onNextPage", function(page) {
    var items = prefsList.getCurrentPage();
    if (items.length > 0 ) {
        refreshPrefsList(items);
    } else {
        prefsList.prevPage(noCallback = true);
    }
});

prefsList.on("onPrevPage", function(page) {
    var items = prefsList.getCurrentPage();
    refreshPrefsList(items);
});

function addMovieToPrefsList(movieId, movieTitle, movieRating) {
    var $prefList = $("#pref-list");
    var $prefItem = $("<li class='list-group-item col-xs-4'></li>")
       .data("movie-id", movieId);
    $prefItem.append($("<span class='pref-item-title'></span>")
        .html(movieTitle));
    var $ratingForm = $("<form></form>");
    for(var i = 1; i <= 10; i++) {
        $ratingForm.append("<input type='radio' name='movie_" + 
            movieId + "' " + "value='" + i + "' " + 
            (i == movieRating ? "checked": "")  + " " + 
            "class='pref-item-rating'>" + i + "");
    }
    $prefItem.append($ratingForm);
    $prefItem.append($("<button class='pref-item-remove' " +
        "type='button'>Remove</button>"));
    $prefList.append($prefItem);        
}

function removeMovieFromPrefsList(movieId) {
    var $prefList = $("#pref-list");
    $prefList.children("li").filter(function() {
        return $(this).data("movie-id") == movieId; 
    }).remove();       
}

function refreshPrefsList(items) {
    $("#pref-list").children("li").remove(); 
    if (items.length > 0) {
        for (var i = 0; i < items.length; i++) {
            addMovieToPrefsList(items[i].id, items[i].title, items[i].rating);
        }
    }
    return (items.length);
}

function clearPrefsList() {
    var movies = prefsList.getData(all = true);
    for(var i = 0; i < movies.length; i++) {
        prefsList.remove(movies[i].id, noCallback = true);
    }
    prefsList.setPage(0);
    $("#pref-list").children("li").remove(); 
    $("#movies-list > li > input").prop("checked", false); 
}

/******************************************************************************/


/*******************************************************************************
    Reco - list
*******************************************************************************/

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
    if (recoType == "standalone") {
        prefList = prefsList.getArray();
    }

    if (recoType == "standalone" && prefList.length == 0) {
        alert("Please specifiy your preferences");
    } else {
        $("#reco-status").show();
        $("#reco-status").html("Recommendation in progres ...");
        $.post(
            "/make_reco",
            JSON.stringify({
                type: recoType,
                prefs: prefList
            }),
            handleRecoResponse
        );
    }
});

function handleRecoResponse(response) {
    if (response.status == "OK") {
        var movies = response.movies;
        if (movies.length === 0) {
            $("#reco-status").show();
            $("#reco-status").html("Unable to make recommendation on the " +
                "base of your preferneces");
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