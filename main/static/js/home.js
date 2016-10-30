/*******************************************************************************
 Movies List (owl.carousel)
*******************************************************************************/

MoviesHandler.onLoaded = function(response) {
    movies = response.movies;
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
        owl.owlCarousel("refresh"); 
    } else {
        // alert("NO MORE MOVIES");
    }
};

$("#popular-browse-mode").click(function(e) {
    clearMoviesList();
    MoviesHandler.setMode(new BrowseQuery("/movies/popular"));
    MoviesHandler.getMovies(page = 1);
    $(".dropdown-toggle").dropdown("toggle");
    e.preventDefault();
    return (false);
});
$("#toprated-browse-mode").click(function(e) {
    clearMoviesList();
    MoviesHandler.setMode(new BrowseQuery("/movies/toprated"));
    MoviesHandler.getMovies(page = 1);
    $(".dropdown-toggle").dropdown("toggle");
    e.preventDefault();
    return (false);
});
$("#upcoming-browse-mode").click(function(e) {
    clearMoviesList();
    MoviesHandler.setMode(new BrowseQuery("/movies/upcoming"));
    MoviesHandler.getMovies(page = 1);
    $(".dropdown-toggle").dropdown("toggle");
    e.preventDefault();
    return (false);
});
$("#nowplaying-browse-mode").click(function(e) {
    clearMoviesList();
    MoviesHandler.setMode(new BrowseQuery("/movies/nowplaying"));
    MoviesHandler.getMovies(page = 1);
    $(".dropdown-toggle").dropdown("toggle");
    e.preventDefault();
    return (false);
});

$(document).on("click", ".movie-watchlist > a", function(event) {
    alert("TIME FOR WATCHLIST");
    event.preventDefault();
});

function clearMoviesList() {
    var owl = $(".owl-carousel");
    while ($(".owl-item").length) {
        owl.trigger("remove.owl.carousel", 0);
    } 
    owl.trigger("to.owl.carousel", [0]);   
}

/******************************************************************************/