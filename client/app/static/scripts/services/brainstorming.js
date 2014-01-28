'use strict';

angular.module('braind')
  .factory('brainstormingService', ['Restangular', '$q', 'initialBrainstorming', 'initialIdeas',
    function (Restangular, $q, initialBrainstorming, initialIdeas) {
      var service = {},
        brainstormingRoute = 'api/brainstormings',
        ideas = null,
        currentBrainstorming = null;

      function initIdeas() {
        currentBrainstorming.getList('ideas').then(function (obj) {
          ideas = obj;
        });
      }

      if (initialBrainstorming) {
        currentBrainstorming = Restangular.restangularizeElement(null,
          initialBrainstorming, brainstormingRoute);
        if (initialIdeas) {
          ideas = Restangular.restangularizeCollection(currentBrainstorming,
            initialIdeas, 'ideas');
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
        return $q.when(ideas);
      };

      service.createIdea = function (data) {
        return ideas.post(data).then(function (obj) {
          ideas.push(obj);
          return obj;
        });
      };

      return service;
    }
  ]);
