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
                    "<div class='movie-ui'>" +
                        "<div class='movie-info'>" + 
                            "<a href='#movieInfo' data-toggle='modal' data-movie-id='" + 
                                movies[i].id + "'>INFO</a>" + 
                        "</div>" +
                        // "<div class='movie-watchlist'>" + 
                        //     "<a href='#'>+WATCHLIST</a>" + 
                        // "</div>" +
                    "</div>" +
                    "<span class='movie-title'>" + movies[i].title + "</span>" + // relative
                "<div>";

            owl.owlCarousel("add", movie_html);
        }
        owl.trigger("refresh.owl.carousel");
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

function changeBrowseCallback(url, title) {
    return function(event) {
        clearMoviesList();
        MoviesHandler.setMode(new BrowseQuery(url));
        MoviesHandler.getMovies(page = 1);
        if (title !== undefined) {
            $("#browse-mode-name").html(title);
        }
        // $(".dropdown-toggle").dropdown("toggle");
        event.preventDefault();
        return (false);
    };
}

$("#popular-browse-mode").click(
    changeBrowseCallback("/movies/popular", "Popular Movies")
);
$("#toprated-browse-mode").click(
    changeBrowseCallback("/movies/toprated", "Top Rated Movies")
);
$("#upcoming-browse-mode").click(
    changeBrowseCallback("/movies/upcoming", "Upcoming Movies")
);

$("#nowplaying-browse-mode").click(
    changeBrowseCallback("/movies/nowplaying", "Now Playing Movies")
);

$(document).on("click", ".movie-watchlist > a", function(event) {
    alert("TIME FOR WATCHLIST");
    event.preventDefault();
});

function clearMoviesList() {
    var owl = $(".owl-carousel");
    while ($(".owl-item").length) {
        owl.trigger("remove.owl.carousel", 0);
    } 
}

/******************************************************************************/