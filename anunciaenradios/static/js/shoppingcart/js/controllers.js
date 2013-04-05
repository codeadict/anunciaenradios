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

function PaquetePublicidadListController($scope, $http) {
	var estacion_id = $('#angular-app').attr('data-estacion-id');
	$http.get('/radios/api/v1/paquetepublicidad/?estacion='+estacion_id+'&format=json').success(function(data) {
		$scope.paquetes = data.objects;
		$scope.reset();
        angular.forEach($scope.paquetes, function(paquete) {            
            var any = false;
            $http.get("/ordenes/api/v1/paquetepublicidad/?duenno="+$('#angular-app').attr('current-user')+"&format=json").success(function(data){
                paquete.paquetes_usuario = data.objects                
                any = true;
            }); 
            if(any){
                paquete.paquetes_usuario[0].selecc = "selected='selected'";
            }
        });

	});
	$scope.resetRequest = function(index) {
		$scope.paquetes[index].cantidad = 0;
    },

	$scope.emptyRequest = function(index) {
		return $scope.paquetes[index].cantidad == 0;
    },

    $scope.shouldDisplay = function() {
        if($scope.paquetes){
            if($scope.paquetes[0].paquetes_usuario){
                if($scope.paquetes[0].paquetes_usuario.length > 0){
                    return true;    
                }                
            }
        }
        return false;
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
        var requestDone = false;
        angular.forEach($scope.paquetes, function(paquete) {
            if(paquete.cantidad > 0){
                requestDone = true;
                $http({
                    method: 'POST',
                    url: "/ordenes/api/v1/orden/",
                    data: {"cantidad": paquete.cantidad,
                         "content_type": "/ordenes/api/v1/contenttype/"+$('#angular-app').attr('data-product-paquetes')+"/",
                         "estado": "Pendiente",
                         "numero": guid(),
                         "object_id": paquete.id.toString(),
                         "total_incl_iva": (paquete.cantidad * paquete.precio).toString(),
                         "user": "/ordenes/api/v1/user/"+$('#angular-app').attr('current-user')+"/",
                         "paquete_publicidad": "/ordenes/api/v1/paquetepublicidad/"+$('#pkg_'+paquete.id).val()+"/",
                     },
                    headers: {'Content-Type': 'application/json'}
                }).error(function(data, status, headers, config) {
                        error = true;
                    });
            }
        })
        if(error){
            alert('Ocurrió un error procesando su orden, por favor intente de nuevo');
        }else{
            if(requestDone){
                $scope.reset();
                alert('Se ha registrado su orden satisfactoriamente');  
            }
        }
    }
}
PaquetePublicidadListController.$inject = ['$scope', '$http'];

function HorarioRotativoListController($scope, $http) {
	var estacion_id = $('#angular-app').attr('data-estacion-id');
	$http.get('/radios/api/v1/horariorotativo/?estacion='+estacion_id+'&format=json').success(function(data) {
		$scope.horarios_rotativos = data.objects;
		$scope.reset();
        angular.forEach($scope.horarios_rotativos, function(horario_rotativo) {            
            var any = false;
            $http.get("/ordenes/api/v1/paquetepublicidad/?duenno="+$('#angular-app').attr('current-user')+"&format=json").success(function(data){
                horario_rotativo.paquetes_usuario = data.objects                
                any = true;
            }); 
            if(any){
                horario_rotativo.paquetes_usuario[0].selecc = "selected='selected'";
            }
        });
	});
	$scope.resetRequest = function(index) {
		$scope.horarios_rotativos[index].cantidad = 0;
    },

	$scope.emptyRequest = function(index) {
		return $scope.horarios_rotativos[index].cantidad == 0;
    },
    
    $scope.shouldDisplay = function() {
        if($scope.horarios_rotativos){
            if($scope.horarios_rotativos[0].paquetes_usuario){
                if($scope.horarios_rotativos[0].paquetes_usuario.length > 0){
                    return true;    
                }                
            }
        }
        return false;
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
        var requestDone = false;
    	angular.forEach($scope.horarios_rotativos, function(horario_rotativo) {
            if(horario_rotativo.cantidad > 0){
                requestDone = true;
                $http({
                    method: 'POST',
                    url: "/ordenes/api/v1/orden/",
                    data: {"cantidad": horario_rotativo.cantidad,
                         "content_type": "/ordenes/api/v1/contenttype/"+$('#angular-app').attr('data-product-horarios')+"/",
                         "estado": "Pendiente",
                         "numero": guid(),
                         "object_id": horario_rotativo.id.toString(),
                         "total_incl_iva": (horario_rotativo.cantidad * horario_rotativo.precio_nacional).toString(),
                         "user": "/ordenes/api/v1/user/"+$('#angular-app').attr('current-user')+"/",
                         "paquete_publicidad": "/ordenes/api/v1/paquetepublicidad/"+$('#pkg2_'+horario_rotativo.id).val()+"/",
                     },
                    headers: {'Content-Type': 'application/json'}
                }).error(function(data, status, headers, config) {
                        error = true;
                    });
            }
        })
        if(error){
            alert('Ocurrió un error procesando su orden, por favor intente de nuevo');
        }else{
            if(requestDone){
                $scope.reset();
                alert('Se ha registrado su orden satisfactoriamente');  
            }
        }
    }
}
HorarioRotativoListController.$inject = ['$scope', '$http'];