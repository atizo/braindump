'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', '$routeParams', 'brainstormingService', 'bdDate',
    function ($scope, $routeParams, brainstormingService, bdDate) {

      var bsid = $routeParams.brainstorming;

      brainstormingService.get(bsid).then(function (obj) {
        obj.createdFormatted = bdDate.format(obj.created);
        $scope.brainstorming = obj;
      });
      brainstormingService.getIdeas(bsid).then(function(obj) {
        $scope.ideas = obj;
      });

      $scope.getIdeaSizeClassName = function (idea) {
        var l = idea.title.length + idea.text.length;
        if (l <= 25) {
          return 'length-25';
        }
        if (l <= 50) {
          return 'length-50';
        }
        if (l <= 150) {
          return 'length-150';
        }
        if (l <= 300) {
          return 'length-300';
        }
        return '';
      };

      $scope.create = function () {
        brainstormingService.postIdea(bsid, $scope.formData).then(function () {
          $scope.user.name = $scope.formData.creatorName;
          $scope.reset();
          $scope.fullform = false;
        });
      };

      $scope.reset = function () {
        $scope.formData = {
          title: '',
          text: '',
          creatorName: $scope.user.name
        };
      };

      $scope.reset();
    }]);
