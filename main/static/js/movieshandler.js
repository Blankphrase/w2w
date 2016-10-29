/*******************************************************************************
 Movies Handler
*******************************************************************************/

var MoviesHandler = {
    mode: undefined,
    onLoad: undefined,
    onLoaded: undefined,
    setMode: function(mode) {
        this.mode = mode;
        this.mode.on("onLoad", this.onLoad);
        this.mode.on("onLoaded", this.onLoaded);
    },
    getMovies: function(page, callback) {
        return (this.mode.getMovies(page, callback));
    },
    getNextPageMovies: function(callback) {
        return (this.mode.getNextPageMovies(callback));
    },
    getPrevPageMovies: function(callback) {
        return (this.mode.getPrevPageMovies(callback));
    }
};

/******************************************************************************/