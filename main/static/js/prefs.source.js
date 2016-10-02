/******************************************************************************
    UserBasedPrefsSource
 ******************************************************************************/

function UserBasedPrefsSource() { 
    this.data = [];
}

UserBasedPrefsSource.prototype.update = function(
    id, title, rating, callback
) {
    var this_ = this; // required for post's callback which overrides this
    $.post(
        "/accounts/user/prefs/update",
        {id: id, rating: rating},
        success = function(response) {
            if (response.status.toUpperCase() === "OK") {
                var movie = this_.get(id);
                if (movie === null) {
                    movie = {
                        id: id, title: title, rating: rating
                    };
                    this_.data.push(movie);
                } else {
                    movie.rating = rating;
                    movie.title = title;
                }
            } else {
                alert("WTF");
            }
            if (callback !== undefined) {
                callback(this_);
            }
        }
    );
}

UserBasedPrefsSource.prototype.getData = function() {
    return (this.data.slice());
} 

UserBasedPrefsSource.prototype.get = function(id) {
    for (var i = 0; i < this.data.length; i++) {
        if (this.data[i].id == id) {
            return (this.data[i]);
        }
    }
    return null;
}

UserBasedPrefsSource.prototype.remove = function(id, callback) {
    var this_ = this; // required for post's callback which overrides this
    $.post(
        "/accounts/user/prefs/remove",
        {id: id},
        success = function(response) {
            if (response.status.toUpperCase() === "OK") {
                var index = this_.indexOf(id);
                if (index >= 0) {
                    this_.data.splice(index, 1);
                }
            }
            if (callback !== undefined) {
                callback(this_);
            }
        }
    );
}

UserBasedPrefsSource.prototype.loadData = function(callback) {
    var this_ = this; // required for post's callback which overrides this
    $.post(
        "/accounts/user/prefs/load",
        success = function(response) {
            if (response.status.toUpperCase() === "OK") {
                this_.data = [];
                var movies = response.prefs;
                for (var i = 0; i < movies.length; i++) {
                    this_.data.push({
                        id: movies[i].id,
                        title: movies[i].title,
                        rating: movies[i].rating
                    });
                }
            }
            if (callback !== undefined) {
                callback(this_);
            }
        }
    );   
}

UserBasedPrefsSource.prototype.indexOf = function(id) {
    for (var i = 0; i < this.data.length; i++) {
        if (this.data[i].id == id) {
            return (i);
        }
    }
    return -1;
}

UserBasedPrefsSource.prototype.size = function() {
    return (this.data.length);
}

UserBasedPrefsSource.prototype.pagination = function(page, pageSize) {
    if (pageSize === undefined) pageSize = 10;
    if (page < 0) {
        return (undefined);
    }
    var start = page*pageSize;
    var end = (page-1)*pageSize;
    return (this.data.slice(start, end));
}

/******************************************************************************
    SessionBasedPrefsSource
 ******************************************************************************/

function SessionBasedPrefsSource(storage) {
    this.storage = storage;
}

SessionBasedPrefsSource.prototype.update = function(
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
        // Keep the newest preferences at the beginning
        data.unshift({
            id: id, title: title, rating: rating
        });
    }
    this.saveStorageData(data);
    if (callback !== undefined) {
        callback(this);
    }
}

SessionBasedPrefsSource.prototype.getData = function() {
    var data = this.getStorageData();
    return (data);
} 

SessionBasedPrefsSource.prototype.get = function(id) {
    var data = this.getStorageData();
    for (var i = 0; i < data.length; i++) {
        if (data[i].id == id) {
            return (data[i]);
        }
    }
    return null;
}

SessionBasedPrefsSource.prototype.remove = function(id, callback) {
    var index = this.indexOf(id);
    if (index >= 0) {
        var data = this.getStorageData();
        data.splice(index, 1);
        this.saveStorageData(data);
        if (callback !== undefined) {
            callback(this);
        }
    }
}


SessionBasedPrefsSource.prototype.loadData = function(callback) {
    // Do nothing. Required for ensuring similar interface for
    // all preferences managers.
    if (callback !== undefined) {
        callback(this);
    }
}

SessionBasedPrefsSource.prototype.indexOf = function(id) {
    var data = this.getStorageData();
    for (var i = 0; i < data.length; i++) {
        if (data[i].id == id) {
            return (i);
        }
    }
    return -1;
}

SessionBasedPrefsSource.prototype.size = function() {
    var data = this.getStorageData();
    return (data.length);
}

SessionBasedPrefsSource.prototype.pagination = function(page, pageSize) {
    if (pageSize === undefined) pageSize = 10;
    if (page < 0) {
        return (undefined);
    }

    var data = this.getStorageData();
    var start = page*pageSize;
    var end = (page+1)*pageSize;
    return (data.slice(start, end));
}

// Extra functions, specific for storage based preferences managers.

SessionBasedPrefsSource.prototype.getStorageData = function() {
    var moviesArray = this.storage.getItem("reco-pref");
    if (!moviesArray) {
        moviesArray = [];
        this.storage.setItem("reco-pref", JSON.stringify(moviesArray));
    } else {
        moviesArray = JSON.parse(moviesArray);
    }
    return moviesArray;
}

SessionBasedPrefsSource.prototype.saveStorageData = function(items) {
    this.storage.setItem("reco-pref", JSON.stringify(items));
}