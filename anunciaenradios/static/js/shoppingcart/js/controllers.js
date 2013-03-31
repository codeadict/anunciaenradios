'use strict';

/* Controllers */

function PaquetePublicidadListController($scope, $http) {
	$http.get('http://localhost:8080/radios/api/v1/paquetepublicidad/?estacion_id=9&format=json').success(function(data) {
		$scope.paquetes = data.objects;
	});
}
PaquetePublicidadListController.$inject = ['$scope', '$http'];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
