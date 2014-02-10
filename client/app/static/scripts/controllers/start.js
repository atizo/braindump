'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', '$location', 'brainstormingService',
    function ($scope, $location, brainstormingService) {

      $scope.create = function () {
        $scope.user.email = $scope.formData.creatorEmail;
        brainstormingService.post($scope.formData).then(function (brainstorming) {
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

      brainstormingService.getRecent().then(function (recentBS) {
        $scope.rb = recentBS;
      });

      $scope.reset();
    }]);
