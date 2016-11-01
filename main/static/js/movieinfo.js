$("#movieInfo").on("show.bs.modal", function(event) {
    var modal = $(this);
    modal.find("#minfo-body").hide();
    modal.find("#minfo-loading").show();
    modal.find("#minfo-title").html("Loading data ...");
    modal.find("#minfo-genres").html("");
});

$('#movieInfo').on('shown.bs.modal', function (event) {
    var movieId = $(event.relatedTarget).data("movie-id");
    var modal = $(this);

    $.post(
        "/movies/" + movieId + "/info"
    ).done(function(data) {
            modal.find("#minfo-loading").hide();           
            modal.find("#minfo-body").show();
            modal.find("#minfo-poster").attr(
                "src", "https://image.tmdb.org/t/p/w154" + data.poster_path
            );
            modal.find("#minfo-title").html(
                data.title + " (" + 
                (new Date(data.release_date)).getFullYear() + ")"
            );
            modal.find("#minfo-overview").html(data.overview);
            modal.find("#minfo-genres").html(
                data.genres.map(function(item) { return item.name }).join(", ")
            );
            modal.find("#minfo-runtime").html(data.runtime);
            modal.find("#minfo-vote").html(
                data.vote_average + " (" + data.vote_count + " votes)"
            );
            modal.find("#minfo-imdb").attr(
                "href",
                "http://www.imdb.com/title/" + data.imdb_id + "/"
            );
            modal.find("#minfo-tmdb").attr(
                "href",
                "https://www.themoviedb.org/movie/" + data.id
            );
        }
    );
})