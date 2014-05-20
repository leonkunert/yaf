'use strict';
angular.module('yaf.factories', [])

.factory('fahrplanFactory', function(){
    return {
        'get_farhplan': function (i) {
            return 'Hallo '+i;
        }
    };
})

.factory('haltestellenFactory', function($http) {
    return {
        'autocomplete': function (string) {
            $http.post('/autocomplete', {haltestelle: string});
        }
    };
});