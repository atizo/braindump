'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', '$rootScope', '$location', 'Restangular', 'brainstormingService',
    function ($scope, $rootScope, $location, Restangular, brainstormingService) {

    $scope.create = function () {
      $rootScope.user = {
        email: $scope.formData.creatorEmail
      };
      brainstormingService.create($scope.formData).then(function (brainstorming) {
        $location.path('/' + brainstorming.id + '/invite');
      });
    };

    $scope.reset = function () {
      $scope.formData = {
        question: '',
        creatorEmail: '',
        details: ''
      };
    };

    $scope.reset();
  }]);
