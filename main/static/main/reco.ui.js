
// User clicks checkbox.
$(".movie-item-checkbox").change(function() {
    var $prefList = $("#pref-list");
    var $prefItem = undefined;

    if ($(this).is(':checked')) {
        $prefItem = $("<li></li>").data("movie-id", $(this).val()).html(
            $(this).next().html()
        );
        $prefList.append($prefItem);
    } else {
        var movieId = $(this).val();
        $prefList.children("li").filter(function() {
            return $(this).data("movie-id") == movieId; 
        }).remove();
    }
});

// User clicks movies-list-next button
$("#movies-list-next").click(function() {
    alert("Do you want new list of movies?");
});

// User clicks movies-list-prev button
$("#movies-list-prev").click(function() {
    alert("Do you want previous list of movies?");
});