/*******************************************************************************
    prefsList 
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
    movies-list Manager
*******************************************************************************/

moviesList = {

    loadInProgress: false,
    callbacks: {
        onLoad: undefined,
        onLoaded: undefined,
        onFail: undefined
    },
    page: undefined,
    totalPages: undefined,
    currentMovies: undefined, 

    on: function(event, callback) {
        this.callbacks[event] = callback;
    },

    next: function(callback) {
        var this_ = this;
        this.load(
            url = "/movies/next",
            data = undefined,
            extra = callback
        );
    },

    prev: function(callback) {
        var this_ = this;
        this.load(
            url = "/movies/prev",
            data = undefined,
            extra = callback
        );
    },

    popular: function(page, callback) {   
        this.load(
            url = "/movies/popular",
            data = {page: page},
            extra = callback
        );
    },

    search: function(query, callback) {
        this.load(
            url = "/movies/search",
            data = {query: query},
            extra = callback
        );
    },

    load: function(url, data, extra) {
        var this_ = this;
        this.loadInProgres = true;
        if (this_.callbacks.onLoad !== undefined) {
            this_.callbacks.onLoad(); 
        }
        $.post(url, data).done(
            function(response) {
                this_.loadInProgres = false;
                this_.page = response.page;
                this_.totalPages = response.total_pages;
                this_.currentMovies = response.movies;

                if (this_.callbacks.onLoaded !== undefined) {
                    this_.callbacks.onLoaded(response); 
                }

                if (extra !== undefined) {
                    extra(response);
                }
            }
        ).fail(
            function(error) {
                this_.loadInProgres = false;
                if (this_.callbacks.onFail !== undefined) {
                    this_.callbacks.onFail(response); 
                }               
            }
        );           
    },

    current: function() {
        return (currentMovies);    
    }

};

/******************************************************************************/