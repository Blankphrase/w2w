/*******************************************************************************
 Movies List (owl.carousel)
*******************************************************************************/

moviesList.on("onLoad", function() {
    // $("#state-msg").show();
    // $("#state-msg").html("(Loading ...)");    
});

moviesList.on("onLoaded", function(response) {
    movies = response.movies;
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
                    "<div class='check-off'>" + 
                        "<div class='check-off-text'><a href='#'>CHECK OFF</a></div>" + 
                    "</div>" +
	    			"<span class='movie-title'>" + movies[i].title + "</span>" + // relative
	    		"<div>"

	    	owl.owlCarousel("add", movie_html);
	    }
	 	owl.owlCarousel("refresh");  
	} else {
		// alert("NO MORE MOVIES");
	}
});


$(document).on("mouseover", ".movie-rating-star", function() {
	$(this).addClass("hovered");
	$(this).prevAll().addClass("hovered");
});

$(document).on("mouseout", ".movie-rating-star", function() {
	$(this).removeClass("hovered");
	$(this).prevAll().removeClass("hovered");
});

$(document).on("click", ".movie-rating-star", function() {
    // Adjust rating from 1-5 to 1-10
    var rating = $(this).data("value")*2 - 1;
    rating = rating == 9 ? 10 : rating;

    var movieId = $(this).parent().parent().data("movie-id");
    var title = $(this).parent().siblings(".movie-title").html();

    prefsList.update(
        movieId = movieId,
        movieTitle = title,
        movieRating = rating   
    );   

    $(this).nextAll().removeClass("selected");
    $(this).addClass("selected");
    $(this).prevAll().addClass("selected");
    $(this).parent().siblings(".check-off").show();
});

// Search Movies

$("#movie-search-button").click(function() {
    var query = $("#movie-search-input").val();
    showMoviesListInfo("Searching movies...");
    moviesList.search(query, function(response) {
        if (response.movies.length > 0) {
            // Remove all movies from carousel from previous browsing
            var owl = $(".owl-carousel");
            while ($(".owl-item").length > response.movies.length) {
                owl.trigger("remove.owl.carousel", 0);
            } 
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
        moviesList.search($(this).val(), function(response) {
            if (response.movies.length > 0) {
                // Remove all movies from carousel from previous browsing
                var owl = $(".owl-carousel");
                while ($(".owl-item").length > response.movies.length) {
                    owl.trigger("remove.owl.carousel", 0);
                }    
                alignMoviesListWithUserPrefs(); 
                hideMoviesListInfo(); 
            } else {
                showMoviesListInfo("No movies found matching your query.");
            }
        });
    }
});

function clearMoviesList() {
    var owl = $(".owl-carousel");
    while ($(".owl-item").length > 0) {
        owl.trigger("remove.owl.carousel", 0);
    }     
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
        if (prefsList.contains(movieId)) {
            var $starRef = $(this).children(".movie-rating").find("[data-value='" + 
                prefsList.getMovie(movieId).rating + "']")

            $starRef.nextAll().removeClass("selected");
            $starRef.addClass("selected");
            $starRef.prevAll().addClass("selected");
            $starRef.parent().siblings(".check-off").show();
        }
    });
}

/******************************************************************************/