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