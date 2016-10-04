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
                    "<div class='check-off-background'>" + 
                        "<div class='check-off'><a href='#'>CHECK OFF</a></div>" + 
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

$(document).on("mouseover", ".poster", function() {

});

$(document).on("click", ".poster", function() {
    prefsList.update(
        movieId = $(this).data("movie-id"), 
        movieTtile = $(this).find("span").html(),
        movieRating = 10 // set be default highest possible rating       
    );
});

// Search Movies

$("#movie-search-button").click(function() {
    var query = $("#movie-search-input").val();
    showMoviesListInfo("Searching movies...");
    moviesList.search(query, function(response) {
        if (response.movies.length > 0) {
            clearMoviesList();   
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
                clearMoviesList();   
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

/******************************************************************************/