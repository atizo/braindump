'use strict';

angular.module('braind')
  .directive('bdHeader', [function () {

    return {
      restrict: 'E',
      templateUrl: '/static/scripts/directives/templates/bdheader.html',
      scope:{
        title: '@',
        action: '&',
        href: '@'
      }
    };
  }]);