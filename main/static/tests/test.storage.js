// mock for some storage
var testStorage = {
    storage: [],
    setItem: function(key, data) {
        var index = this.indexOf(key);
        if (index < 0) {
            this.storage.push({key: key, data: data});
        } else {
            this.storage[index].data = data;
        }
    },
    getItem: function(key) {
        var index = this.indexOf(key);
        if (index >= 0) {
            return this.storage[index].data;
        }
        return null;
    },
    indexOf: function(key) {
        for (var i = 0; i < this.storage.length; i++) {
            if (this.storage[i].key === key) {
                return i;
            }
        }
        return -1;
    }
};