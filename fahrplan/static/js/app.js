'use strict';
angular.module('yaf', [
    'yaf.controllers',
    'yaf.factories'
])

.config(function ($locationProvider) {
    $locationProvider.html5Mode(true);
});