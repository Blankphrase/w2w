/*******************************************************************************
 Prefs List 
*******************************************************************************/

$("#prefs-list-next").click(function() {
    PrefsList.nextPage();
});


$("#prefs-list-prev").click(function() {
    PrefsList.prevPage();
});


$("#clear-my-prefs").click(function() {
    if (confirm("Are your sure you want to clear all your preferences?")) {
        clearPrefsList();
        alignMoviesListWithUserPrefs();
    }
});


$(document).on("click", ".pref-movie-remove", function() {
    var movieId = $(this).parent().parent().data("movie-id");
    PrefsList.remove(movieId);
    $(".movie-item").filter(function() {
        return $(this).data("movie-id") == movieId
    }).find("input").prop("checked", false); 

    // alignMoviesListWithUserPrefs();
    var $movie = $(".movie").filter(function() { 
        return $(this).data("movie-id") == movieId
    });
    $movie.children(".movie-rating").children().removeClass("selected");
    $movie.children(".check-off").hide();
});


$(document).on("mouseover", ".pref-rating-star", function() {
    $(this).addClass("hovered");
    $(this).prevAll().addClass("hovered");
});

$(document).on("mouseout", ".pref-rating-star", function() {
    $(this).removeClass("hovered");
    $(this).prevAll().removeClass("hovered");
});

$(document).on("click", ".pref-rating-star", function() {
    // Adjust rating from 1-5 to 1-10
    var rating = $(this).data("value");

    var movieId = $(this).parent().parent().parent().data("movie-id");
    var title = $(this).parent().parent().siblings(".pref-movie-title").html();

    PrefsList.update(
        movieId = movieId,
        movieTitle = title,
        movieRating = rating   
    );   

    // alignMoviesListWithUserPrefs();
    var $movie = $(".movie").filter(function() { 
        return $(this).data("movie-id") == movieId
    });
    $movie.children(".movie-rating").children().removeClass("selected");

    var $movieStar =  $movie.children(".movie-rating").
        find("[data-value='" + rating + "']");
    $movieStar.addClass("selected");
    $movieStar.prevAll().addClass("selected");
});


PrefsList.on("onUpdate", function() {
    reloadPrefsList(PrefsList.getCurrentPage());
});


PrefsList.on("onRemove", function(movieId) {
    var items = PrefsList.getCurrentPage();
    // if removal of item leads to empty page than skip to previous page
    if (items.length == 0) {
        PrefsList.prevPage(noCallback = true);
        items = PrefsList.getCurrentPage();
    } 
    reloadPrefsList(items);
});


PrefsList.on("onNextPage", function(page) {
    var items = PrefsList.getCurrentPage();
    if (items.length > 0 ) {
        reloadPrefsList(items);
    } else {
        PrefsList.prevPage(noCallback = true);
    }
});


PrefsList.on("onPrevPage", function(page) {
    var items = PrefsList.getCurrentPage();
    reloadPrefsList(items);
});


function addMovieToPrefsList(movieId, movieTitle, movieRating) {
    var $prefList = $("#pref-list");
    var $prefItem = $("<div class='pref-movie'></div>")
       .data("movie-id", movieId);
    $prefItem.append($("<span class='pref-movie-title'></span>")
        .html(movieTitle));
    var $prefUI = $("<div class ='pref-movie-ui'></div>");
    var $ratingForm = $("<div class='pref-movie-rating'></div>");
    for(var i = 1; i <= 5; i++) {
        $ratingForm.append($("<div class='pref-rating-star " +
            (i <= movieRating ? "selected" : "") +
            "' data-value='" + i + "'><span></span></div>"));

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
    var movies = PrefsList.getData(all = true);
    for(var i = 0; i < movies.length; i++) {
        PrefsList.remove(movies[i].id, noCallback = true);
    }
    PrefsList.setPage(0);
    $("#pref-list").children("div").remove(); 
    alignMoviesListWithUserPrefs();
}

/******************************************************************************/