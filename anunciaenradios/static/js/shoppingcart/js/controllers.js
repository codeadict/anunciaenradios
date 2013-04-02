'use strict';

/* Controllers */
function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
             .toString(16)
             .substring(1);
};

function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         s4() + '-' + s4() + s4() + s4();
}

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
        var error = false;
        angular.forEach($scope.paquetes, function(paquete) {
            if(paquete.cantidad > 0){
                $http({
                    method: 'POST',
                    url: "/ordenes/api/v1/orden/",
                    data: {"cantidad": paquete.cantidad,
                         "content_type": "/ordenes/api/v1/contenttype/"+$('#angular-app').attr('data-product-paquetes')+"/",
                         "estado": "Pendiente",
                         "numero": guid(),
                         "object_id": paquete.id.toString(),
                         "total_incl_iva": (paquete.cantidad * paquete.precio).toString(),
                         "user": "/ordenes/api/v1/user/"+$('#angular-app').attr('current-user')+"/"},
                    headers: {'Content-Type': 'application/json'}
                }).success(function(data, status, headers, config) {
                        //
                    }).
                    error(function(data, status, headers, config) {
                        error = true;
                    });
            }
        })
        if(error){
            alert('Ocurrió un error procesando su orden, por favor intente de nuevo');
        }else{
            $scope.reset();
            alert('Se ha registrado su orden satisfactoriamente');  
        }
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
        var error = false;
    	angular.forEach($scope.horarios_rotativos, function(horario_rotativo) {
            if(horario_rotativo.cantidad > 0){
                $http({
                    method: 'POST',
                    url: "/ordenes/api/v1/orden/",
                    data: {"cantidad": horario_rotativo.cantidad,
                         "content_type": "/ordenes/api/v1/contenttype/"+$('#angular-app').attr('data-product-horarios')+"/",
                         "estado": "Pendiente",
                         "numero": guid(),
                         "object_id": horario_rotativo.id.toString(),
                         "total_incl_iva": (horario_rotativo.cantidad * horario_rotativo.precio_nacional).toString(),
                         "user": "/ordenes/api/v1/user/"+$('#angular-app').attr('current-user')+"/"},
                    headers: {'Content-Type': 'application/json'}
                }).success(function(data, status, headers, config) {
                        //
                    }).
                    error(function(data, status, headers, config) {
                        error = true;
                    });
            }
        })
        if(error){
            alert('Ocurrió un error procesando su orden, por favor intente de nuevo');
        }else{
            $scope.reset();
            alert('Se ha registrado su orden satisfactoriamente');  
        }
    }
}
HorarioRotativoListController.$inject = ['$scope', '$http'];