'use strict';

// Declare app level module which depends on filters, and services
angular.module('shoppingCartApp', ['shoppingCartApp.filters', 'shoppingCartApp.services', 'shoppingCartApp.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/paquete', {templateUrl: '/static/js/shoppingcart/partials/paquete_publicidad.html', controller: PaquetePublicidadListController});
    $routeProvider.when('/view2', {templateUrl: '/static/js/shoppingcart/partials/partial2.html', controller: MyCtrl2});
    $routeProvider.otherwise({redirectTo: '/paquete'});
  }]);
