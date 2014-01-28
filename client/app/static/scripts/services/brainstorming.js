'use strict';

angular.module('braind')
  .factory('brainstormingService', ['brainstorming', function (brainstorming) {

    var brain = brainstorming;

    return {
      getBrainstorming: function () {
        return brain;
      },
      setBrainstorming: function (brains) {
        brain = brains;
      }
    };
  }]);