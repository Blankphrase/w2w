function MoviesQuery(url, page) {
    if (url === undefined) {
        throw("MoviesQuery: url parameter is required");
    }
    this.url = url;
    this.page = page;
    this.total_pages = undefined;
    this.total_results = undefined;
}

MoviesQuery.prototype.getMovies = function(page, callback) {
    // Make sure the page is in valid format.
    if (page === undefined) page = 1;
    if (isNaN(page)) page = 1;
    page = parseInt(page, 10);
    if (page < 1) page = 1;

    var this_ = this;
    $.post(
        this.url,
        JSON.stringify({page: page}),
        function(response) {
            if (response.status == "OK") {
                this_.page = response.page;
                this_.total_pages = response.total_pages;
                this_.total_results = response.total_results;
            }
            if (callback !== undefined) callback(response);
        }
    );
};

MoviesQuery.prototype.isNextPage = function() {
    if (this.page === undefined || this.total_pages === undefined) {
        return (undefined);
    } else if (this.total_pages > this.page) {
        return (true);
    }
    return (false);
};

MoviesQuery.prototype.isPrevPage = function() {
    if (this.page === undefined || this.total_pages === undefined) {
        return (undefined);
    } else if (this.page > 1 && this.page - 1 <= this.total_pages) {
        return (true);
    }
    return (false);
};

MoviesQuery.prototype.getNextPageMovies = function(callback) {
    if (this.page === undefined) {
        throw("getNextPageMovies: undefined page");
    }
    this.getMovies(page = this.page + 1, callback);
};

MoviesQuery.prototype.getPrevPageMovies = function(callback) {
    if (this.page === undefined) {
        throw("getPrevPageMovies: undefined page");
    }
    this.getMovies(page = this.page - 1, callback);
};

MoviesQuery.prototype.getLastPage = function() {
    return (this.page);
};

MoviesQuery.prototype.setPage = function(page) {
    this.page = page;
};