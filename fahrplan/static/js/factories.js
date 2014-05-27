'use strict';
angular.module('yaf.factories', [])

.factory('fahrplanFactory', function() {
    return {
        'get_farhplan': function (i) {
            return 'Hallo '+i;
        }
    };
})

.factory('userFactory', function($http) {
    return {
        'login': function (user) {
            return $http({
                url: "/login",
                method: "POST",
                params: {
                    user:user.username,
                    pass:user.password
                }
            });
        },
        'logout': function () {
            return $http.post("/logout");
        },
        'status': function () {
            return $http.get("/userStatus");
        }
    }
})

.factory('haltestellenFactory', function($http) {
    return {
        'get_haltestellen': function () {
            return $http.post('/haltestellen');
        }
    };
});