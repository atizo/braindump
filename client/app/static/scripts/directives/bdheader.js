'use strict';

angular.module('braind')
  .directive('bdHeader', [function () {

    return {
      restrict: 'EA',
      templateUrl: '/static/views/directives/bdheader.html',
      scope: {
        title: '@',
        action: '&',
        tools: '=',
        href: '@'
      }
    };
  }]);