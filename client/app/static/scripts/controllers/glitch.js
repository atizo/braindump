'use strict';

angular.module('braind')
  .controller('GlitchCtrl', ['$scope', 'errorMsg',
    function ($scope, errorMsg) {
      $scope.errorMsg = errorMsg;
    }]);
