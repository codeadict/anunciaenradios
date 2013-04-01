'use strict';

/* Controllers */

function PaquetePublicidadListController($scope, $http) {
	var estacion_id = $('#angular-app').attr('data-estacion-id');
	$http.get('/radios/api/v1/paquetepublicidad/?estacion='+estacion_id+'&format=json').success(function(data) {
		$scope.paquetes = data.objects;
		$scope.reset();
	});
	$scope.resetRequest = function(index) {
		$scope.paquetes[index].cantidad = 0;
    },

	$scope.emptyRequest = function(index) {
		return $scope.paquetes[index].cantidad == 0;
    },

    $scope.total = function() {
        var total = 0;
        angular.forEach($scope.paquetes, function(paquete) {
            total += paquete.cantidad * paquete.precio;
        })

        return total;
    }
    $scope.reset = function(){
		angular.forEach($scope.paquetes, function(paquete) {
            paquete.cantidad = 0;
        })    	
    }
    $scope.archiveOrder = function(){
    	//TODO
    }
}
PaquetePublicidadListController.$inject = ['$scope', '$http'];

function HorarioRotativoListController($scope, $http) {
	var estacion_id = $('#angular-app').attr('data-estacion-id');
	$http.get('/radios/api/v1/horariorotativo/?estacion='+estacion_id+'&format=json').success(function(data) {
		$scope.horarios_rotativos = data.objects;
		$scope.reset();
	});
	$scope.resetRequest = function(index) {
		$scope.horarios_rotativos[index].cantidad = 0;
    },

	$scope.emptyRequest = function(index) {
		return $scope.horarios_rotativos[index].cantidad == 0;
    },

    $scope.total = function() {
        var total_regional = 0;
        var total_nacional = 0;
        angular.forEach($scope.horarios_rotativos, function(horario_rotativo) {
            total_regional += horario_rotativo.cantidad * horario_rotativo.precio_regional;
            total_nacional += horario_rotativo.cantidad * horario_rotativo.precio_nacional;
        })

        return [total_regional, total_nacional];
    }
    $scope.reset = function(){
		angular.forEach($scope.horarios_rotativos, function(horario_rotativo) {
            horario_rotativo.cantidad = 0;
        })    	
    }

    $scope.archiveOrder = function(){
    	//TODO
    }
}
HorarioRotativoListController.$inject = ['$scope', '$http'];