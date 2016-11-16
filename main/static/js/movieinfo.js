$("#movieInfo").on("show.bs.modal", function(event) {
    var modal = $(this);
    modal.find("#minfo-body").hide();
    modal.find("#minfo-add-watchlist").hide();
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
                if (data.poster_path !== null) {
                    modal.find("#minfo-poster").attr(
                        "src", "https://image.tmdb.org/t/p/w154" + data.poster_path
                    );
                } else {
                    modal.find("#minfo-poster").hide().attr("src", "#");
                }
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
                if (modal.data("active") == "1") {
                    var $watchlist = modal.find("#minfo-add-watchlist");
                    $watchlist.show();
                    $watchlist.find("a").show();
                    $watchlist.children("span").remove();
                    $watchlist.data("movie-id", movieId);
                }
            }
        }
    );
});

$("#minfo-poster").on("load", function() { 
    $(this).show();
}).on("error", function() { 
    $(this).hide();
});

$(document).on("click", "#minfo-add-watchlist > a", function(event) {
    var $self = $(this).parent();
    $self.find("a").hide();
    $self.children("span").remove();
    $self.append("<span>Adding to watchlist ...</span>");
    $.post(
        "/accounts/watchlist/add",
        {id: $self.data("movie-id")},
        success = function(response) {
            $self.children("span").remove();
            if (response.status.toUpperCase() === "ERROR") {
                console.log(response.msg);
                $self.append("<span>Unexpected error when adding to watchlist.</span>");
            } else {
                $self.append("<span>Movie added to your watchlist.</span>");
                setTimeout(function() {
                    $self.hide();
                }, 2000);
            }
        }
    );

    event.preventDefault();
    return (false);
});