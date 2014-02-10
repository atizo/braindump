'use strict';

angular.module('braind')
  .controller('EditCtrl', ['$scope', '$rootScope', '$location', '$routeParams', 'brainstormingService',
    function ($scope, $rootScope, $location, $routeParams, brainstormingService) {
      var brainstorming = brainstormingService.get($routeParams.brainstorming);

      $scope.nuser = {email: ''};

      brainstorming.then(function (bs) {
        $scope.bs = bs;

        if (bs.canEdit) {
          $scope.formData = {
            question: bs.question,
            details: bs.details
          };
          $scope.update = function () {
            brainstormingService.update(bs.id, $scope.formData).then(function () {
              $location.path('/' + bs.id);
            });
          };
        } else {
          $scope.submit = function () {
            bs.post('edit', $scope.nuser).then(function (r) {
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
