/**
 * Alerts Controller
 */

angular
    .module('RDash')
    .controller('DashCtl', ['$scope', '$http', '$modal', DashCtl]);

angular
    .module('RDash')
    .controller('ModalInstanceCtrl', ['$scope', '$modalInstance', '$http', 'selected_server', ModalInstanceCtrl]);

function DashCtl($scope, $http, $modal) {
    $scope.refresh_machines = function (){
      $http({method: 'GET', url: 'http://10.111.4.100:5000/machines/',
           headers: {'Authorization': 'Basic ' + btoa('admin:admin')}})
         .success(function(response) {
                  servers = response._items;
                  servers.sort(function(a,b) { return a.job_id.localeCompare(b.job_id); } );
                  var users = {};
                  var free_machines = [];
                  var pxe_failed = [];
                  var in_use = [];
                  for (i = 0; i < servers.length; i++) {
                      server = servers[i];
                      if (server.state == 'idle'){
                        free_machines.push(server);
                      }else if(server.state == 'in_use'){
                        in_use.push(server);
                      }else if(server.state == 'pxe_failed'){
                        pxe_failed.push(server);
                      }
                  }
                  $scope.servers = servers;
                  $scope.users = users;
                  $scope.pxe_failed = pxe_failed;
                  $scope.in_use = in_use;
                  $scope.free_machines = free_machines;
                });}
      $scope.open = function (selected_server) {
        console.log("Confirming: " + selected_server.job_id);
        $scope.selected_server = selected_server;
        var modalInstance = $modal.open({
          templateUrl: 'templates/modal.html',
          controller: 'ModalInstanceCtrl',
          resolve: {
            selected_server: function () {
              return $scope.selected_server;
            }
          }
        });

        modalInstance.result.then(function (selectedItem) {
          $scope.selected = selectedItem;
        }, function () {
          console.log('Modal dismissed at: ' + new Date());
        });
      };
}



function ModalInstanceCtrl($scope, $modalInstance, $http, selected_server) {

  $scope.selected_server = selected_server;

  $scope.ok = function () {
    console.log("Freeing: " + selected_server.job_id);
    var updated_server = selected_server;
    var jenkins_url = 'http://jenkins.qa1.eucalyptus-systems.com/job/Free%20Reservation/buildWithParameters?token=machine_dashboard';
    $http({
      method: 'POST',
      url: jenkins_url,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: "JOB_ID=" + selected_server.job_id
    }).success(function(response) {
      console.log('Successfully freed: ' + selected_server.job_id);
    });
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
};
