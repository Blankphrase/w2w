/******************************************************************************
    UserBasedPrefsManager
 ******************************************************************************/

function UserBasedPrefsManager() { 
    this.data = [];
}

UserBasedPrefsManager.prototype.update = function(
    id, title, rating, callback
) {
    var this_ = this; // required for post's callback which overrides this
    $.post(
        "/accounts/user/prefs/update",
        JSON.stringify({id: id, rating: rating}),
        success = function(response) {
            if (response.status.toUpperCase() === "OK") {
                var movie = this_.get(id);
                if (movie === null) {
                    movie = {
                        id: id, title: title, rating: rating
                    };
                }
                this_.data.push(movie);
            }
            if (callback !== undefined) {
                callback(response);
            }
        }
    );
}

UserBasedPrefsManager.prototype.get = function(id) {
    for (var i = 0; i < this.data.length; i++) {
        if (this.data[i].id == id) {
            return (this.data[i]);
        }
    }
    return null;
}

UserBasedPrefsManager.prototype.remove = function(id, callback) {
    var this_ = this; // required for post's callback which overrides this
    $.post(
        "/accounts/user/prefs/remove",
        JSON.stringify({id: id}),
        success = function(response) {
            if (response.status.toUpperCase() === "OK") {
                var index = this_.indexOf(id);
                if (index >= 0) {
                    this_.data.splice(index, 1);
                }
            }
            if (callback !== undefined) {
                callback(response);
            }
        }
    );
}

UserBasedPrefsManager.prototype.loadData = function(callback) {
    var this_ = this; // required for post's callback which overrides this
    $.post(
        "/accounts/user/prefs/load",
        success = function(response) {
            if (response.status.toUpperCase() === "OK") {
                this_.data = [];
                var movies = response.movies;
                for (var i = 0; i < movies.length; i++) {
                    this_.data.push({
                        id: movies[i].id,
                        title: movies[i].title,
                        rating: movies[i].rating
                    });
                }
            }
            if (callback !== undefined) {
                callback(response);
            }
        }
    );   
}

UserBasedPrefsManager.prototype.indexOf = function(id) {
    for (var i = 0; i < this.data.length; i++) {
        if (this.data[i].id == id) {
            return (i);
        }
    }
    return -1;
}

UserBasedPrefsManager.prototype.count = function() {
    return (this.data.length);
}

UserBasedPrefsManager.prototype.pagination = function(page, pageSize) {
    if (pageSize === undefined) pageSize = 10;

    var start = page*pageSize;
    var end = (page+1)*pageSize;
    return (this.data.slice(start, end));
}

/******************************************************************************
    SessionBasedPrefsManager
 ******************************************************************************/

function SessionBasedPrefsManager(storage) {
    this.storage = storage;
}

SessionBasedPrefsManager.prototype.update = function(
    id, title, rating, callback
) {
    var data = this.getStorageData();
    var index = this.indexOf(id);
    var movie = null;

    if (index >= 0) {
        data[index].id = id;
        data[index].title = title;
        data[index].rating = rating;
    } else {
        data.push({
            id: id, title: title, rating: rating
        });
    }
    this.saveStorageData(data);
}

SessionBasedPrefsManager.prototype.get = function(id) {
    var data = this.getStorageData();
    for (var i = 0; i < data.length; i++) {
        if (data[i].id == id) {
            return (data[i]);
        }
    }
    return null;
}

SessionBasedPrefsManager.prototype.remove = function(id, callback) {
    var index = this.indexOf(id);
    if (index >= 0) {
        var data = this.getStorageData();
        data.splice(index, 1);
        this.saveStorageData(data);
    }
}


SessionBasedPrefsManager.prototype.loadData = function(callback) {
    // Do nothing. Required for ensuring similar interface for
    // all preferences managers.
}

SessionBasedPrefsManager.prototype.indexOf = function(id) {
    var data = this.getStorageData();
    for (var i = 0; i < data.length; i++) {
        if (data[i].id == id) {
            return (i);
        }
    }
    return -1;
}

SessionBasedPrefsManager.prototype.count = function() {
    var data = this.getStorageData();
    return (data.length);
}

SessionBasedPrefsManager.prototype.pagination = function(page, pageSize) {
    if (pageSize === undefined) pageSize = 10;
    
    var data = this.getStorageData();
    var start = page*pageSize;
    var end = (page+1)*pageSize;
    return (data.slice(start, end));
}

// Extra functions, specific for storage based preferences managers.

SessionBasedPrefsManager.prototype.getStorageData = function() {
    var moviesArray = this.storage.getItem("reco-pref");
    if (!moviesArray) {
        moviesArray = [];
        this.storage.setItem("reco-pref", JSON.stringify(moviesArray));
    } else {
        moviesArray = JSON.parse(moviesArray);
    }
    return moviesArray;
}

SessionBasedPrefsManager.prototype.saveStorageData = function(items) {
    this.storage.setItem("reco-pref", JSON.stringify(items));
}