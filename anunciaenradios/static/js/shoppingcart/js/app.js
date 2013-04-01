'use strict';

// Declare app level module which depends on filters, and services
angular.module('shoppingCartApp', ['shoppingCartApp.filters', 'shoppingCartApp.services', 'shoppingCartApp.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/cart', {templateUrl: '/static/js/shoppingcart/partials/cart.html'});
    $routeProvider.otherwise({redirectTo: '/cart'});
  }]);
