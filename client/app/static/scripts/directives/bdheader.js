'use strict';

angular.module('braind')
  .directive('bdHeader', [function () {

    return {
      restrict: 'E',
      templateUrl: '/static/views/directives/bdheader.html',
      scope:{
        title: '@',
        action: '&',
        href: '@'
      }
    };
  }]);