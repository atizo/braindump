'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', '$routeParams', '$location', '$modal', 'brainstormingService', 'bdDate',
    function ($scope, $routeParams, $location, $modal, brainstormingService, bdDate) {

      var bsid = $routeParams.brainstorming;

      brainstormingService.get(bsid).then(function (obj) {
        obj.createdFormatted = bdDate.format(obj.created);
        $scope.brainstorming = obj;
      }, function () {
        $location.path('/').replace();
      });
      brainstormingService.getIdeas(bsid).then(function (obj) {
        $scope.ideas = obj;
      });

      $scope.create = function () {
        brainstormingService.postIdea(bsid, $scope.formData).then(function () {
          $scope.user.name = $scope.formData.creatorName;
          $scope.reset();
          $scope.fullform = false;
        });
      };

      $scope.openDetail = function (idea) {
        var modalScope = $scope.$new();
        modalScope.idea = idea;
        $modal.open({
          templateUrl: '/static/views/idea-modal.html',
          controller: 'IdeaDetailCtrl',
          scope: modalScope
        });
      };

      $scope.toolBar = [
        {href: '/' + bsid + '/notification', class: 'star'},
        {href: '/' + bsid + '/edit', class: 'edit'}
      ];

      $scope.reset = function () {
        $scope.formData = {
          title: '',
          text: '',
          creatorName: $scope.user.name
        };
      };

      $scope.reset();
    }])
  .controller('IdeaDetailCtrl', ['$scope', '$routeParams', '$modalInstance', '$window', 'brainstormingService',
    function ($scope, $routeParams, $modalInstance, $window, brainstormingService) {
      var bsid = $routeParams.brainstorming;

      $scope.editMode = false;

      $scope.done = function () {
        $modalInstance.close();
      };

      $scope.rate = function () {

      };

      $scope.delete = function (iid) {
        if ($window.confirm('Do you really want to delete this idea?')) {
          brainstormingService.deleteIdea(bsid, iid);
          $modalInstance.close();
        }
      };
    }]);
