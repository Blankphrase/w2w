/*******************************************************************************
    prefsList 
*******************************************************************************/

var prefsList = {

    callbacks: {
        onInitialized: undefined,
        onNextPage: undefined,
        onPrevPage: undefined,
        onUpdate: undefined,
        onRemove: undefined
    },
    source: undefined,
    page: 0,
    pageSize: 10,

    init: function(source, pageSize) {
        this.source = source; 
        if (pageSize !== undefined) {
            this.pageSize = pageSize;
        }
        this.source.loadData(this.callbacks.onInitialized);
    },

    on: function(event, callback) {
        this.callbacks[event] = callback;
    },

    update: function(movieId, movieTitle, movieRating) {
        if (movieRating === undefined) movieRating = 10;
        this.source.update(
            movieId, movieTitle, movieRating,
            this.callbacks.onUpdate
        );
    },

    remove: function(movieId, noCallback) {
        if (noCallback === undefined) noCallback = false;
        var this_ = this;
        this.source.remove(
            movieId,
            function() {
                if (!noCallback && this_.callbacks.onRemove !== undefined) {
                    this_.callbacks.onRemove(movieId);
                }
            }
        );   
    },

    nextPage: function(noCallback) {
        if (noCallback === undefined) noCallback = false;
        this.page += 1;
        if (!noCallback && this.callbacks.onNextPage !== undefined) {
            this.callbacks.onNextPage(this.page);
        }
    },

    setPage: function(page) {
        this.page = page;
    },

    prevPage: function(noCallback) {
        if (noCallback === undefined) noCallback = false;
        if (this.page > 0) {
            this.page -= 1;
            if (!noCallback && this.callbacks.onPrevPage !== undefined) {
                this.callbacks.onPrevPage(this.page);
            }
        }
    },

    contains: function(movieId) {
        return (this.source.indexOf(movieId) >= 0);
    },

    getMovie: function(movieId) {
        return (this.source.get(movieId));
    },

    getData: function(all) {
        if (all === undefined || all === false) {
            var items = this.source.pagination(this.page, this.pageSize);
            return (items); 
        } else {      
            return (this.source.getData());
        }
    },

    getCurrentPage: function() {
        return (this.getData());
    }
};

/******************************************************************************/
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
        if (this.loadInProgress == false) {
            var this_ = this;
            this.loadInProgress = true;
            if (this_.callbacks.onLoad !== undefined) {
                this_.callbacks.onLoad(); 
            }
            $.post(url, data).done(
                function(response) {
                    this_.loadInProgress = false;
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
                    this_.loadInProgress = false;
                    if (this_.callbacks.onFail !== undefined) {
                        this_.callbacks.onFail(response); 
                    }               
                }
            );      
        }  
    },

    current: function() {
        return (currentMovies);    
    }

};

/******************************************************************************/