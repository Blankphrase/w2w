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
    if (!loadInProgress) loadMoviesFromServer("/movies/next");
});

$("#movies-list-prev").click(function() {
    if (!loadInProgress) loadMoviesFromServer("/movies/prev");
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
    loadMoviesFromServer("/movies/search", {query: query});
});


$("#movie-search-input").keyup(function (e) {
    if (e.keyCode == 13) {
        loadMoviesFromServer("/movies/search", {query: $(this).val()});
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
    prefsList Manager
*******************************************************************************/

var prefsList = {

    source: undefined,
    pageSize: 10,
    page: 0,

    init: function(source, callback) {
        this.source = source;
        this.source.loadData(callback);
    },

    getArray: function() {
        return (this.source.getArray());
    },

    add: function(movieId, movieTitle, movieRating, callback) {
        if (movieRating === undefined) movieRating = 10
        this.source.update(movieId, movieTitle, movieRating, callback);
    },

    clear: function() {
        var movies = this.source.getArray();
        var this_ = this;
        for(var i = 0; i < movies.length; i++) {
            this.remove(
                movies[i].id,
                function() {
                    this_.removeItem(movies[i].id);
                }
            )
        }
        $("#movies-list > li > input").prop("checked", false); 
    },

    update: function(movieId, movieTitle, movieRating) {
        this.source.update(movieId, movieTitle, movieRating);
    },

    remove: function(movieId, callback) {
        this.source.remove(movieId,callback);
    },

    nextPage: function() {
        this.page += 1;
    },

    prevPage: function() {
        if (this.page > 0) {
            this.page -= 1;
        }
    },

    contains: function(movieId) {
        return (this.source.indexOf(movieId) >= 0);
    },

    refresh: function() {
        var items = this.source.pagination(this.page, this.pageSize);
        if (items.length > 0) {
            $("#pref-list").children("li").remove(); 
            for (var i = 0; i < items.length; i++) {
                this.addItem(items[i].id, items[i].title, items[i].rating);
            }
        }
        return (items.length);
    },

    addItem: function(movieId, movieTitle, movieRating) {
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
        $prefList.prepend($prefItem);        
    },

    removeItem: function(movieId) {
        var $prefList = $("#pref-list");
        $prefList.children("li").filter(function() {
            return $(this).data("movie-id") == movieId; 
        }).remove();       
    }

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

/*******************************************************************************
    movies-list
*******************************************************************************/

function loadMoviesFromServer(url, data, callback) {
    if (data === undefined) data = {};

    loadInProgress = true;
    $("#state-msg").show();
    $("#state-msg").html("(Loading ...)");

    $.post(url, data)
    .done(function(response) {
        movies = response.movies;
        createMoviesList(movies);
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

        if (callback !== undefined) {
            callback();
        }

    })
    .fail(function(errMsg) {
            alert(errMsg);
            loadInProgress = false;
    }); 
}

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