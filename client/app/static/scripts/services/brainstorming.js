'use strict';

angular.module('braind')
  .factory('brainstormingService', ['Restangular', '$q', 'brainstormingStore', 'ideaStore', 'recentBrainstormings',
    function (Restangular, $q, brainstormingStore, ideaStore, recentBrainstormings) {
      var brainstormingRoute = 'api/brainstormings';

      function ideasURL(bsid) {
        return brainstormingRoute + '/' + bsid + '/ideas';
      }

      function addRecentBrainstorming(bsid) {
        recentBrainstormings = _.without(recentBrainstormings, bsid);
        recentBrainstormings.unshift(bsid);
        return recentBrainstormings;
      }

      function addIdea(bsid, idea) {
        if (!_.has(ideaStore, bsid)) {
          ideaStore[bsid] = {};
        }
        ideaStore[bsid][idea.id] = idea;
        return idea;
      }

      // restangularize brainstormingStore
      _.forOwn(brainstormingStore, function (bs, bsid) {
          brainstormingStore[bsid] = Restangular.restangularizeElement(null,
            bs, brainstormingRoute);
        }
      );

      // restangularize ideaStore
      _.forOwn(ideaStore, function (ideas, bsid) {
          _.forOwn(ideas, function (idea, iid) {
              ideaStore[bsid][iid] = Restangular.restangularizeElement(null,
                idea, ideasURL(bsid));
            }
          );
        }
      );

      var bsResource = {};

      bsResource.get = function (bsid) {
        if (_.has(brainstormingStore, bsid)) {
          addRecentBrainstorming(bsid);
          return $q.when(brainstormingStore[bsid]);
        } else {
          return Restangular.one(brainstormingRoute, bsid).get().then(function (bs) {
            // add to store
            addRecentBrainstorming(bs.id);
            brainstormingStore[bs.id] = bs;
            return bs;
          });
        }
      };

      bsResource.getRecent = function () {
        var i, max = 10, bs = [];
        _(recentBrainstormings).forEach(function (bsid) {
          if (i > max) {
            return false;
          }
          bs.push(bsResource.get(bsid));
          i += 1;
        });
        return $q.all(bs);
      };

      bsResource.post = function (data) {
        return Restangular.all(brainstormingRoute).post(data)
          .then(function (bs) {
            addRecentBrainstorming(bs.id);
            brainstormingStore[bs.id] = bs;
            return bs;
          });
      };


      bsResource.getIdeas = function (bsid) {
        if (_.has(ideaStore, bsid)) {
          return $q.when(ideaStore[bsid]);
        } else {
          return Restangular.all(ideasURL(bsid)).getList().then(function (ideas) {
            ideaStore[bsid] = {};
            _(ideas).forEach(function (idea) {
                ideaStore[bsid][idea.id] = idea;
              }
            );
            return ideaStore[bsid];
          });
        }
      };

      bsResource.getIdea = function (bsid, iid) {
        if (_.has(ideaStore, bsid) && _.has(ideaStore[bsid], iid)) {
          return $q.when(ideaStore[bsid][iid]);
        } else {
          return Restangular.one(ideasURL(bsid), iid).get().then(function (idea) {
            return addIdea(bsid, idea);
          });
        }
      };

      bsResource.postIdea = function (bsid, data) {
        return Restangular.all(ideasURL(bsid)).post(data)
          .then(function (idea) {
            return addIdea(bsid, idea);
          });
      };

      return bsResource;
    }
  ]);
