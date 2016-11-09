/*******************************************************************************
    RecoList
*******************************************************************************/

var RecoList = {

    callbacks: {
        onNewPage: undefined
    },
    page: 0,
    data: undefined,
    pageSize: 10,
    type: undefined,

    setType: function(type) {
        this.type = type;
    },

    getType: function(type) {
        return this.type;
    },

    initFromData: function(data, pageSize) {
        if (pageSize !== undefined) this.pageSize = pageSize;
        this.data = data;
        if (this.callbacks.onNewPage !== undefined) {
            this.callbacks.onNewPage(this.getData(this.page));
        }
    },

    saveInStorage: function(type) {
        if (this.type !== undefined) {
            try {
                sessionStorage.setItem("reco-" + this.type, 
                                     JSON.stringify(this.data));
                return true;
            } catch(e) {
                return false;
            }
        } else {
            return false;
        }
    },

    initFromStorage: function(pageSize) {
        if (pageSize !== undefined) this.pageSize = pageSize;
        if (this.type !== undefined) {
            try {
                var data = JSON.parse(sessionStorage.getItem("reco-" + this.type));
                if (data !== undefined) {
                    this.data = data;
                    if (this.callbacks.onNewPage !== undefined) {
                        this.callbacks.onNewPage(this.getData(this.page));
                    }
                    return true;
                } else {
                    return false;
                }
            } catch(e) {
                return false;
            }
        } else {
            return false;
        }
    },

    on: function(event, callback) {
        this.callbacks[event] = callback;
    },

    nextPage: function() {
        this.page += 1;
        if (this.callbacks.onNewPage !== undefined) {
            this.callbacks.onNewPage(this.getData(this.page));
        }
    },

    setPage: function(page) {
        if (this.page != page) {
            this.page = page;
            if (this.callbacks.onNewPage !== undefined) {
                this.callbacks.onNewPage(this.getData(this.page));
            }
        }
    },

    prevPage: function() {
        if (this.page > 0) {
            this.page -= 1;
            if (this.callbacks.onNewPage !== undefined) {
                this.callbacks.onNewPage(this.getData(this.page));
            }
        }
    },  

    getData: function(page) {
        if (page === undefined) {
            return (this.data);
        } else {
            return (this.data.slice(
                page * this.pageSize,
                (page+1)*this.pageSize
            ));
        }
    },

    getPagesCount: function() {
        return (Math.floor(this.data.length / this.pageSize));
    },

    getPage: function() {
        return (this.page);
    }
};

/******************************************************************************/


/*******************************************************************************
    PrefsList 
*******************************************************************************/

var PrefsList = {

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
    type: undefined,

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
            function(response) {
                if (!noCallback && this_.callbacks.onRemove !== undefined) {
                    this_.callbacks.onRemove(response);
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
    },

    size: function() {
        return (this.source.size());
    }
};

/******************************************************************************/