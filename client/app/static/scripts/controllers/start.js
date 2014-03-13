'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', '$rootScope', '$location', 'brainstormingService',
    function ($scope, $rootScope, $location, brainstormingService) {

      $rootScope.showDeco = false;

      $scope.create = function () {
        $scope.user.email = $scope.formData.creatorEmail;
        $scope.loading = true;
        brainstormingService.post($scope.formData).then(function (brainstorming) {
          $location.path('/' + brainstorming.id + '/invite');
        })['finally'](function () {
          $scope.loading = false;
        });
      };

      $scope.reset = function () {
        $scope.formData = {
          question: '',
          creatorEmail: $scope.user.email,
          details: ''
        };
      };

      $scope.showDeco = true;

      brainstormingService.getRecent().then(function (recentBS) {
        $scope.rb = recentBS;
        $rootScope.showDeco = !recentBS.length;
      });

      $scope.reset();


    }]);
