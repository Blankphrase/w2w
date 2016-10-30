$("#movieInfo").on("show.bs.modal", function(event) {
    var modal = $(this);

    var $poster = modal.find("#minfo-poster");
    var $title = modal.find("#minfo-title");
    var $overview = modal.find("#minfo-overview");   

    $poster.attr("src", "");
    $title.html("Loading data ...");
    $overview.html("Wait a second.");
});

$('#movieInfo').on('shown.bs.modal', function (event) {
    var movieId = $(event.relatedTarget).data("movie-id");
    var modal = $(this);

    $.post(
        "movies/" + movieId + "/info"
    ).done(function(data) {
            var $poster = modal.find("#minfo-poster");
            var $title = modal.find("#minfo-title");
            var $overview = modal.find("#minfo-overview");

            $poster.attr("src", "https://image.tmdb.org/t/p/w154" + 
                data.poster_path);
            $title.html(data.title);
            $overview.html(data.overview);
        }
    );
})