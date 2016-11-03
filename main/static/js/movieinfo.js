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
            if (data.w2w_status == "ERROR") {
                $("#movieInfo").modal("hide");
                alert("Error while loading information about the movie. Please try again latter.");
            } else {
                modal.find("#minfo-loading").hide();           
                modal.find("#minfo-body").show();
                modal.find("#minfo-poster").attr(
                    "src", "https://image.tmdb.org/t/p/w154" + data.poster_path
                );
                modal.find("#minfo-title").html(
                    (data.title === null ? "<Title not available>" : data.title) + 
                    (data.release_date === null ? "" : 
                        " (" + (new Date(data.release_date)).getFullYear() + ")")
                );
                modal.find("#minfo-overview").html(
                    data.overview === null ? "<Overview not available>" : data.overview
                );
                if (data.genres !== undefined) {
                    modal.find("#minfo-genres").html(
                        data.genres.map(function(item) { return item.name }).join(", ")
                    );
                } else {
                    modal.find("#minfo-genres").html(""); 
                }

                modal.find("#minfo-runtime").html(
                    data.runtime === null ? "-" : data.runtime   
                );

                modal.find("#minfo-vote").html(
                    (data.vote_average === null ? "-" : data.vote_average) +
                    " (" + (data.vote_count === null ? "-" : data.vote_count) + 
                    " votes)"
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
        }
    );
});

$("#minfo-poster").on("load", function() { 
    $(this).show();
}).on("error", function() { 
    $(this).hide();
});