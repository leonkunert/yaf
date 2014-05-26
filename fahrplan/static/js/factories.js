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
        }
    }
})

.factory('haltestellenFactory', function($http) {
    return {
        'autocomplete': function (string) {
            return $http.post('/autocomplete', {haltestelle: string});
        }
    };
});