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
        currentBrainstorming = Restangular.restangularizeElement(null,
          initialBrainstorming, brainstormingRoute + initialBrainstorming.slug);
        if (initialIdeas) {
          $q.when(Restangular.restangularizeCollection(currentBrainstorming,
            initialIdeas, 'ideas'));
        } else {
          initIdeas();
        }
      }

      service.create = function (data) {
        return Restangular.all(brainstormingRoute).post(data)
          .then(function (obj) {
            currentBrainstorming = obj;
            initIdeas();
            return obj;
          });
      };

      service.getBrainstorming = function () {
        return $q.when(currentBrainstorming);
      };

      service.getIdeas = function () {
        return ideas;
      };

      service.createIdea = function (data) {
        var newIdea = ideas.post(data);
        console.log(ideas, newIdea);
        return newIdea;
      };

      return service;
    }
  ]);
