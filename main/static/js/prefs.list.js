/*******************************************************************************
 Prefs List 
*******************************************************************************/

$("#prefs-list-next").click(function() {
    prefsList.nextPage();
});

$("#prefs-list-prev").click(function() {
    prefsList.prevPage();
});

$("#clear-my-prefs").click(function() {
    if (confirm("Are your sure you want to clear all your preferences?")) {
        clearPrefsList();
        alignMoviesListWithUserPrefs();
    }
});


$(document).on("click", ".pref-item-remove", function() {
    var movieId = $(this).parent().data("movie-id");

    $(".movie-item").filter(function() {
        return $(this).data("movie-id") == movieId
    }).find("input").prop("checked", false);
    prefsList.remove(movieId);
});

prefsList.on("onUpdate", function() {
    reloadPrefsList(prefsList.getCurrentPage());
});

prefsList.on("onRemove", function(movieId) {
    var items = prefsList.getCurrentPage();
    // if removal of item leads to empty page than skip to previous page
    if (items.length == 0) {
        prefsList.prevPage(noCallback = true);
        items = prefsList.getCurrentPage();
    } 
    reloadPrefsList(items);
});

prefsList.on("onNextPage", function(page) {
    var items = prefsList.getCurrentPage();
    if (items.length > 0 ) {
        reloadPrefsList(items);
    } else {
        prefsList.prevPage(noCallback = true);
    }
});

prefsList.on("onPrevPage", function(page) {
    var items = prefsList.getCurrentPage();
    reloadPrefsList(items);
});

function addMovieToPrefsList(movieId, movieTitle, movieRating) {
    var $prefList = $("#pref-list");
    var $prefItem = $("<div class='pref-movie'></div>")
       .data("movie-id", movieId);
    $prefItem.append($("<span class='pref-movie-title'></span>")
        .html(movieTitle));
    var $prefUI = $("<div></div>");
    var $ratingForm = $("<div class='pref-movie-rating'></div>");
    for(var i = 1; i <= 5; i++) {
        $ratingForm.append($("<div class='movie-rating-star " +
            (i <= movieRating ? "selected" : "") +
            " '><span></span></div>"));

    }
    $prefUI.append($ratingForm);
    $prefUI.append($("<button class='pref-movie-remove' " +
        "type='button'>Remove</button>"));
    $prefItem.append($prefUI);
    $prefList.append($prefItem);        
}


function removeMovieFromPrefsList(movieId) {
    var $prefList = $("#pref-list");
    $prefList.children("div").filter(function() {
        return $(this).data("movie-id") == movieId; 
    }).remove();       
}

function reloadPrefsList(items) {
    $("#pref-list").children().remove();
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
    $("#pref-list").children("div").remove(); 
    alignMoviesListWithUserPrefs();
}

/******************************************************************************/