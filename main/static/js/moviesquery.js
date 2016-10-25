/*!
 * Movies Queries JavaScript Library 
 * - BrowseQuery
 * - SearchQuery
 */

function BrowseQuery(url, page) {
    if (url === undefined) {
        throw("BrowseQuery: url parameter is required");
    }
    this.url = url;
    this.page = page;
    this.total_pages = undefined;
    this.total_results = undefined;
    this.loadInProgress = false;
}

BrowseQuery.prototype.createRequestParams = function(page) {
    return ({
        page: page
    });
};

BrowseQuery.prototype.getMovies = function(page, callback) {
    // Allow only one request at the same time.
    if (!this.loadInProgress) {
        // Make sure the page is in valid format.
        if (page === undefined) page = 1;
        if (isNaN(page)) page = 1;
        page = parseInt(page, 10);
        if (page < 1) page = 1;

        this.loadInProgress = true;

        var this_ = this;
        $.post(
            this.url,
            JSON.stringify(this.createRequestParams(page)),
            function(response) {
                this_.loadInProgress = false;
                if (response.status == "OK") {
                    this_.page = response.page;
                    this_.total_pages = response.total_pages;
                    this_.total_results = response.total_results;
                }
                if (callback !== undefined) callback(response);
            }
        );
        return (true);
    }
    return (false);
};

BrowseQuery.prototype.isNextPage = function() {
    if (this.page === undefined || this.total_pages === undefined) {
        return (undefined);
    } else if (this.total_pages > this.page) {
        return (true);
    }
    return (false);
};

BrowseQuery.prototype.isPrevPage = function() {
    if (this.page === undefined || this.total_pages === undefined) {
        return (undefined);
    } else if (this.page > 1 && this.page - 1 <= this.total_pages) {
        return (true);
    }
    return (false);
};

BrowseQuery.prototype.getNextPageMovies = function(callback) {
    if (this.page === undefined) {
        throw("getNextPageMovies: undefined page");
    }
    return (this.getMovies(page = this.page + 1, callback));
};

BrowseQuery.prototype.getPrevPageMovies = function(callback) {
    if (this.page === undefined) {
        throw("getPrevPageMovies: undefined page");
    }
    return (this.getMovies(page = this.page - 1, callback));
};

BrowseQuery.prototype.getLastPage = function() {
    return (this.page);
};

BrowseQuery.prototype.setPage = function(page) {
    this.page = page;
};


function SearchQuery(query, page) {
    BrowseQuery.call(this, "/movies/search", page);
    if (query === undefined) {
        throw("SearchQuery: query parameter is required");
    }
    this.query = query;
}
SearchQuery.prototype = Object.create(BrowseQuery.prototype);
SearchQuery.prototype.constructor = SearchQuery;

SearchQuery.prototype.createRequestParams = function(page) {
    var params = BrowseQuery.prototype.createRequestParams.call(this, page);
    params.query = this.query;
    return (params);
};