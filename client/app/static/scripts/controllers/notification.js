'use strict';

angular.module('braind')
  .controller('NotificationCtrl', ['$scope', '$rootScope', '$location', '$routeParams', 'brainstormingService', 'messageService',
    function ($scope, $rootScope, $location, $routeParams, brainstormingService, messageService) {
      var brainstorming = brainstormingService.get($routeParams.brainstorming),
        msg = messageService.getMsg();

      $scope.nuser = {email: ''};

      brainstorming.then(function (bs) {
        $scope.bs = bs;

        if (msg.length > 0) {
          $scope.infoMsg = msg;
        } else {
          $scope.submit = function () {
            bs.post('notification', $scope.nuser).then(function (r) {
              $scope.status = {
                email: $scope.nuser.email,
                action: r.status
              };
            });
          };
        }
      }, function () {
        $location.path('/').replace();
      });
    }]);
