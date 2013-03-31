'use strict';

/* Controllers */

function PaquetePublicidadListController($scope, $http) {
	var estacion_id = $('#angular-app').attr('data-estacion-id');
	$http.get('/radios/api/v1/paquetepublicidad/?estacion='+estacion_id+'&format=json').success(function(data) {
		$scope.paquetes = data.objects;
	});
}
PaquetePublicidadListController.$inject = ['$scope', '$http'];

function HorarioRotativoListController($scope, $http) {
	var estacion_id = $('#angular-app').attr('data-estacion-id');
	$http.get('/radios/api/v1/rorariorotativo/?estacion='+estacion_id+'&format=json').success(function(data) {
		$scope.paquetes = data.objects;
	});
}
HorarioRotativoListController.$inject = ['$scope', '$http'];


function MyCtrl2() {
}
MyCtrl2.$inject = [];
