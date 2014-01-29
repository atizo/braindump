'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', '$location', 'Restangular', 'brainstormingService',
    function ($scope, $location, Restangular, brainstormingService) {

    $scope.create = function () {
      $scope.user.email = $scope.formData.creatorEmail;
      brainstormingService.create($scope.formData).then(function (brainstorming) {
        $location.path('/' + brainstorming.id + '/invite');
      });
    };

    $scope.reset = function () {
      $scope.formData = {
        question: '',
        creatorEmail: $scope.user.email,
        details: ''
      };
    };

    $scope.reset();
  }]);
