'use strict';

angular.module('braind')
  .factory('brainstormingService', ['Restangular', '$q', 'initialBrainstorming', 'initialIdeas',
    function (Restangular, $q, initialBrainstorming, initialIdeas) {
      var service = {},
        brainstormingRoute = 'api/brainstormings/',
        ideas = null,
        currentBrainstorming = null;

      function initIdeas() {
        ideas = currentBrainstorming.getList('ideas');
      }

      if (initialBrainstorming) {
        currentBrainstorming = $q.when(Restangular.restangularizeElement(null,
          initialBrainstorming, brainstormingRoute + initialBrainstorming.slug));

        if (initialIdeas) {
          $q.when(Restangular.restangularizeCollection(currentBrainstorming,
            initialIdeas, 'ideas'));
        } else {
          initIdeas();
        }
      }

      service.create = function (data) {
        currentBrainstorming = Restangular.all(brainstormingRoute).post(data);
        initIdeas();
        return currentBrainstorming;
      };

      service.getBrainstorming = function () {
        return currentBrainstorming;
      };

      service.getIdeas = function () {
        return ideas;
      };

      service.createIdea = function (data) {
        return ideas.post(data);
      };

      return service;
    }
  ]);
