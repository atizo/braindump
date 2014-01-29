'use strict';

angular.module('braind')
  .directive('bdHeader', ['$timeout', 'bdDate', function ($timeout, bdDate) {

    return {
      restrict: 'E',
      templateUrl: '/static/scripts/directives/templates/bdheader.html',
      transclude: true,
      link: function (scope, element, attr) {

      }
    };
  }]);