/*******************************************************************************
 Movies List (owl.carousel)
*******************************************************************************/

MoviesHandler.onLoad = function(response) {
    var owl = $(".owl-carousel");
    var movie_html = 
        "<div class='movie movie-loading' data-movie-id=''>" + // relative
            '<div id="floatingCirclesG">'+
                '<div class="f_circleG" id="frotateG_01"></div>'+
                '<div class="f_circleG" id="frotateG_02"></div>'+
                '<div class="f_circleG" id="frotateG_03"></div>'+
                '<div class="f_circleG" id="frotateG_04"></div>'+
                '<div class="f_circleG" id="frotateG_05"></div>'+
                '<div class="f_circleG" id="frotateG_06"></div>'+
                '<div class="f_circleG" id="frotateG_07"></div>'+
                '<div class="f_circleG" id="frotateG_08"></div>'+
            '</div>'+
            "<span class='movie-title'>Loading ...</span>" + // relative
        "<div>";
    owl.owlCarousel("add", movie_html);
}

MoviesHandler.onLoaded = function(response) {
    movies = response.movies;
    $(".movie-loading").remove();
    if (movies.length > 0) {
        var owl = $(".owl-carousel");
        for (var i = 0; i < movies.length; i++) {
            var img_src = "https://image.tmdb.org/t/p/w154" + movies[i].poster_path;
            var movie_html = 
                "<div class='movie' data-movie-id='" + movies[i].id + "'>" + // relative
                    "<img src='" + img_src + "'>" + // relative
                    "<div class='movie-rating'>" +  // absolute
                        "<div class='movie-rating-star' data-value='1'><span></span></div>" +
                        "<div class='movie-rating-star' data-value='2'><span></span></div>" +
                        "<div class='movie-rating-star' data-value='3'><span></span></div>" +
                        "<div class='movie-rating-star' data-value='4'><span></span></div>" +
                        "<div class='movie-rating-star' data-value='5'><span></span></div>" +
                    "</div>" +
                    "<div class='movie-ui'>" +
                        "<div class='movie-info'>" + 
                            "<a href='#movieInfo' data-toggle='modal' data-movie-id='" + 
                                movies[i].id + "'>INFO</a>" + 
                        "</div>" +
                        // "<div class='movie-watchlist'>" + 
                        //     "<a href='#'>+WATCHLIST</a>" + 
                        // "</div>" +
                    "</div>" +
                    "<div class='check-off'>" + 
                        "<div class='check-off-text'><a href=''>CHECK OFF</a></div>" + 
                    "</div>" +
                    "<span class='movie-title'>" + movies[i].title + "</span>" + // relative
                "<div>";

            owl.owlCarousel("add", movie_html);
        }
        owl.owlCarousel("refresh"); 
        alignMoviesListWithUserPrefs();  
    } else {
        MoviesHandler.setEndOfMovies();
        var owl = $(".owl-carousel");
        var movie_html = 
            "<div class='movie movie-loading' data-movie-id=''>" + // relative
                "<img src='" + MoviesHandler.noMoreMoviesImg + "'>" +
                "<span class='movie-title'></span>" + // relative
            "<div>";
        owl.owlCarousel("add", movie_html);
    }
};

function changeBrowseCallback(url) {
    return function(event) {
        clearMoviesList();
        MoviesHandler.setMode(new BrowseQuery(url));
        MoviesHandler.getMovies(page = 1);
        $(".dropdown-toggle").dropdown("toggle");
        e.preventDefault();
        return (false);
    };
}

$("#popular-browse-mode").click(
    changeBrowseCallback("/movies/popular")
);
$("#toprated-browse-mode").click(
    changeBrowseCallback("/movies/toprated")
);
$("#upcoming-browse-mode").click(
    changeBrowseCallback("/movies/upcoming")
);
$("#nowplaying-browse-mode").click(
    changeBrowseCallback("/movies/nowplaying")
);

$(document).on("mouseover", ".movie-rating-star", function() {
    $(this).addClass("hovered");
    $(this).prevAll().addClass("hovered");
});

$(document).on("mouseout", ".movie-rating-star", function() {
    $(this).removeClass("hovered");
    $(this).prevAll().removeClass("hovered");
});

$(document).on("click", ".movie-rating-star", function() {
    // Rating 1-5
    var rating = $(this).data("value");
    var movieId = $(this).parent().parent().data("movie-id");
    var title = $(this).parent().siblings(".movie-title").html();

    PrefsList.update(
        movieId = movieId,
        movieTitle = title,
        movieRating = rating   
    );   

    $(this).nextAll().removeClass("selected");
    $(this).addClass("selected");
    $(this).prevAll().addClass("selected");
    $(this).parent().siblings(".check-off").show();
});

$(document).on("click", ".movie-watchlist > a", function(event) {
    alert("TIME FOR WATCHLIST");

    event.preventDefault();
});

$(document).on("click", ".check-off a", function(event) {
    var movieId = $(this).parent().parent().parent().data("movie-id");
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

    event.preventDefault();
});

// Search Movies

$("#movie-search-button").click(function() {
    var query = $("#movie-search-input").val();
    showMoviesListInfo("Searching movies...");
    MoviesHandler.setMode(new SearchQuery(query));
    MoviesHandler.getMovies(page = 1, function(response) {
        if (response.movies.length > 0) {
            // Remove all movies from carousel from previous browsing
            var owl = $(".owl-carousel");
            while ($(".owl-item").length > response.movies.length) {
                owl.trigger("remove.owl.carousel", 0);
            } 
            owl.trigger("to.owl.carousel", [0]);
            alignMoviesListWithUserPrefs();
            hideMoviesListInfo(); 
        } else {
            showMoviesListInfo("No movies found matching your query.");
        }
    });
});


$("#movie-search-input").keyup(function (e) {
    if (e.keyCode == 13) {
        showMoviesListInfo("Searching movies...");
        MoviesHandler.setMode(new SearchQuery($(this).val()));
        MoviesHandler.getMovies(page = 1, function(response) {
            if (response.movies.length > 0) {
                // Remove all movies from carousel from previous browsing
                var owl = $(".owl-carousel");
                while ($(".owl-item").length > response.movies.length) {
                    owl.trigger("remove.owl.carousel", 0);
                }    
                alignMoviesListWithUserPrefs();
                owl.trigger("to.owl.carousel", [0]);
                hideMoviesListInfo(); 
            } else {
                showMoviesListInfo("No movies found matching your query.");
            }
        });
    }
});

function clearMoviesList() {
    var owl = $(".owl-carousel");
    while ($(".owl-item").length) {
        owl.trigger("remove.owl.carousel", 0);
    } 
    owl.trigger("to.owl.carousel", [0]);   
}

function showMoviesListInfo(msg) {
    var info = $("#movies-list-info");
    info.find("#movies-list-info-msg").html(msg);
    info.show();
}

function hideMoviesListInfo() {
    $("#movies-list-info").hide();
}

function alignMoviesListWithUserPrefs() {
    var $movies = $(".movie");
    $movies.each(function(index) {
        var movieId = $(this).data("movie-id");
        if (PrefsList.contains(movieId)) {
            var $starRef = $(this).children(".movie-rating").find("[data-value='" + 
                PrefsList.getMovie(movieId).rating + "']");
            $starRef.nextAll().removeClass("selected");
            $starRef.addClass("selected");
            $starRef.prevAll().addClass("selected");
            $starRef.parent().siblings(".check-off").show();
        } else {
            if ($(this).children(".check-off").is(":visible")) {
                $(this).children(".movie-rating").children().removeClass("selected");
                $(this).children(".check-off").hide();
            }
        }
    });
}

/******************************************************************************/

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

    var movieId = $(this).parent().parent().parent().parent().data("movie-id");
    var title = $(this).parent().parent().parent().siblings(".pref-movie-title").html();

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
    // $prefItem.append($("<span class='pref-movie-title'></span>")
        // .html(movieTitle));
    $prefItem.append($("<span class='pref-movie-title'><a href='#movieInfo' " +
        "data-toggle='modal' data-movie-id='" + movieId + "'>" + 
        movieTitle + "</a></span>"));
    var $prefUI = $("<div class ='pref-movie-ui'></div>");

    var $prefSelection = $("<div class = 'pref-selection'></div>");
    $prefSelection.append($("<button class='pref-dropbtn'>" +
        movieRating + "</button>"));

    var $ratingForm = $("<div class='pref-movie-rating'></div>");
    for(var i = 1; i <= 5; i++) {
        $ratingForm.append($("<div class='pref-rating-star " +
            (i <= movieRating ? "selected" : "") +
            "' data-value='" + i + "'><span>" + i + "</span></div>"));

    }
    $prefSelection.append($ratingForm);
    $prefUI.append($prefSelection);
    $prefUI.append($("<button class='btn btn-default btn-md pref-movie-remove' " +
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

/*******************************************************************************
    Reco - list
*******************************************************************************/

RecoList.on("onNewPage", function(movies) {
    updateRecoList(movies);
});


$("#reco-list-next").click(function() {
    if (RecoList.getPage() < RecoList.getPagesCount()-1) {
        RecoList.nextPage();
    }
});


$("#btn-reco-title").click(function() {
    var recoId = $("#reco-id").val();
    var recoTitle = $("#reco-title").val();

    if (recoTitle === "") {
        alert("The given title seems to be empty. Please fill correct title into input box.");
    } else {
        $.post(
            "/accounts/reco/" + recoId + "/title",
            {title: recoTitle},
            success = function(response) {
                if (response.status.toUpperCase() === "ERROR") {
                    alert(response.msg);
                }
            }
        );
    }
});


$("#reco-list-prev").click(function() {
    RecoList.prevPage();
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
            prefList = PrefsList.getData(all = true);
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
            $("#reco-title").val(response.title);
            $("#reco-id").val(response.id);
            RecoList.init(movies, 5);
        }
    } else {
        alert("ERROR: DO STH WITH IT");
    }
}


function updateRecoList(movies) {
    $("#reco-page").html("Page " + (RecoList.getPage() + 1) + " of " +
            RecoList.getPagesCount()
    );
    var $RecoList = $("#reco-list");
    $RecoList.children("li").remove();
    for (var i = 0; i < movies.length; i++) {
        $RecoList.append($("<li class='reco-item' data-movie-id='" + 
            movies[i].id + "'><a href='#movieInfo' " +
            "data-toggle='modal' data-movie-id='" + movies[i].id + "'>" + 
            movies[i].title + "</a>" +
            " (<a href='#' class='watchlist-add-btn'>+Watchlist</a>)</li>")); 
    }
    // $prefItem.append($("<span class='pref-movie-title'><a href='#movieInfo' " +
    //     "data-toggle='modal' data-movie-id='" + movieId + "'>" + 
    //     movieTitle + "</a></span>"));
}

/******************************************************************************/