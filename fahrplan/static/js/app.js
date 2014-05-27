'use strict';
angular.module('yaf', [
    'yaf.controllers',
    'yaf.factories',
    'ngRoute',
    'ngAutocomplete'
])

.config(function ($locationProvider) {
    $locationProvider.html5Mode(true);
});