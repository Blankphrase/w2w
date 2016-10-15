/*******************************************************************************
    Reco - list
*******************************************************************************/

recoList.on("onNewPage", function(movies) {
    updateRecoList(movies);
});


$("#reco-list-next").click(function() {
    if (recoList.getPage() < recoList.getPagesCount()) {
        recoList.nextPage();
    }
});


$("#reco-list-prev").click(function() {
    recoList.prevPage();
});

$(document).on("click", ".watchlist-add-btn", function(event) {
    event.preventDefault();
    
    var $movie = $(this).parent();
    $.post(
        "/accounts/watchlist/add",
        {id: $movie.data("movie-id")},
        success = function(response) {
            if (response.status.toUpperCase() === "ERROR") {
                alert(response.msg);
            }
        }
    );

    return (false);
});

var recoInProgress = false;
$("#reco-btn").click(function() {
    // General recommendation procedure does not required to receive
    // preferences, because it used all user's preferences already
    // stored in internal databases.

    if (recoInProgress) {
        alert("The recommendation is already being perpered for you. Please wait.");
    } else {
        var prefList = null;
        if (recoType == "standalone") {
            prefList = prefsList.getData();
        }

        if (recoType == "standalone" && prefList.length == 0) {
            alert("Please specifiy your preferences");
        } else {
            $("#reco-status").show();
            $("#reco-status-msg").html("Recommendation in progres ...");
            recoInProgress = true;
            $.post(
                "/make_reco",
                JSON.stringify({
                    type: recoType,
                    prefs: prefList
                }),
                function(response) {
                    recoInProgress = false;
                    handleRecoResponse(response);                    
                }
            );
        }
    }
});


function handleRecoResponse(response) {
    if (response.status == "OK") {
        var movies = response.movies;
        
        if (movies.length === 0) {
            $("#reco-status").show();
            $("#reco-status-msg").html("Unable to make recommendation on the " +
                "base of your preferneces");
        } else {
            $("#reco-container").show();
            $("#reco-status").show();
            $("#reco-status-msg").html("Recommendation complete.");
            $("#reco-output").show();
            recoList.init(movies, 5);
        }
    } else {
        alert("ERROR: DO STH WITH IT");
    }
}


function updateRecoList(movies) {
    $("#reco-page").html("Page " + (recoList.getPage() + 1) + " of " +
            (recoList.getPagesCount() + 1)
    );
    var $recoList = $("#reco-list");
    $recoList.children("li").remove();
    for (var i = 0; i < movies.length; i++) {
        $recoList.append($("<li class='reco-item' data-movie-id='" + 
            movies[i].id + "'>" + movies[i].title + 
            " (<a href='#' class='watchlist-add-btn'>+Watchlist</a>)</li>")); 
    }
}

/******************************************************************************/