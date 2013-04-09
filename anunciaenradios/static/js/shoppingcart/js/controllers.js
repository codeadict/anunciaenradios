'use strict';

/* Controllers */
function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
             .toString(16)
             .substring(1);
};

$.urlParam = function(name){
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}

function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         s4() + '-' + s4() + s4() + s4();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var success = $.urlParam('success').trim();
if(success == 1){
    alert("Orden realizada satisfactoriamente");
    var url = window.location;
    window.location.replace(url.toString().replace("&success=1", ""));    

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
        var producto_object_cantidad_arr = ""
        var success_url = window.location;
        angular.forEach($scope.paquetes, function(paquete) {
            if(paquete.cantidad > 0){
                producto_object_cantidad_arr += $('#angular-app').attr('data-product-paquetes') + ":" + paquete.id + ":" + paquete.cantidad + "|";
            }
        });
        var url = '/ordenes/paquetes/agregar/?pdc=' + producto_object_cantidad_arr + '&success_url='+ success_url;
        window.location = url;
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
        var producto_object_cantidad_arr = ""
        var success_url = window.location;
        angular.forEach($scope.horarios_rotativos, function(horario_rotativo) {
            if(horario_rotativo.cantidad > 0){
                producto_object_cantidad_arr += $('#angular-app').attr('data-product-horarios') + ":" + horario_rotativo.id + ":" + horario_rotativo.cantidad + "|";
            }
        });
        var url = '/ordenes/paquetes/agregar/?pdc=' + producto_object_cantidad_arr + '&success_url='+ success_url;
        window.location = url;        
    }
}
HorarioRotativoListController.$inject = ['$scope', '$http'];