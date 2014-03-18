'use strict';

angular.module('braind')
  .factory('brainstormingService', ['Restangular', '$q', '$upload', 'brainstormingStore', 'ideaStore', 'recentBrainstormings',
    function (Restangular, $q, $upload, brainstormingStore, ideaStore, recentBrainstormings) {
      var brainstormingRoute = 'api/brainstormings';

      function ideasURL(bsid) {
        return brainstormingRoute + '/' + bsid + '/ideas';
      }

      function addRecentBrainstorming(bsid) {
        recentBrainstormings = _.without(recentBrainstormings, bsid);
        recentBrainstormings.unshift(bsid);
        return recentBrainstormings;
      }

      function addIdeaToStore(bsid, idea) {
        if (!_.has(ideaStore, bsid)) {
          ideaStore[bsid] = {};
        }
        ideaStore[bsid][idea.id] = idea;
        return idea;
      }

      function updateIdeaInStore(bsid, idea) {
        if (!_.has(ideaStore, bsid)) {
          ideaStore[bsid] = {};
        }
        if (!_.has(ideaStore[bsid], idea.id)) {
          ideaStore[bsid][idea.id] = {};
        }
        _.merge(ideaStore[bsid][idea.id], idea);
        return idea;
      }

      function removeIdeaFromStore(bsid, iid) {
        if (!_.has(ideaStore, bsid)) {
          return;
        }
        delete ideaStore[bsid][iid];
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

      bsResource.update = function (bsid, data) {
        return bsResource.get(bsid).then(function (bs) {
          return bs.patch(data).then(function (updatedBS) {
            // add to store
            addRecentBrainstorming(updatedBS.id);
            brainstormingStore[updatedBS.id] = updatedBS;
            return updatedBS;
          });
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
            return addIdeaToStore(bsid, idea);
          });
        }
      };

      bsResource.postIdea = function (bsid, data, file) {
        if (file) {
          return $upload.upload({
            url: ideasURL(bsid),
            data: data,
            file: file,
            fileFormDataName: 'imagefile'
          }).then(function (resp) {
            return addIdeaToStore(bsid, Restangular.restangularizeElement(null,
              resp.data, ideasURL(bsid)));
          });
        }
        return Restangular.all(ideasURL(bsid)).post(data)
          .then(function (idea) {
            return addIdeaToStore(bsid, idea);
          });
      };

      bsResource.updateIdea = function (bsid, iid, data, file) {
        if (file) {
          return $upload.upload({
            url: ideasURL(bsid) + '/' + iid,
            data: data,
            file: file,
            method: 'PUT',
            fileFormDataName: 'imagefile'
          }).then(function (resp) {
            return updateIdeaInStore(bsid, Restangular.restangularizeElement(null,
              resp.data, ideasURL(bsid)));
          });
        }
        return Restangular.one(ideasURL(bsid), iid).patch(data)
          .then(function (idea) {
            return updateIdeaInStore(bsid, idea);
          });
      };

      bsResource.deleteIdea = function (bsid, iid) {
        return Restangular.one(ideasURL(bsid), iid).remove()
          .then(function () {
            return removeIdeaFromStore(bsid, iid);
          });
      };

      bsResource.rateIdea = function (bsid, iid) {
        // optimistically update ratings
        if (_.has(ideaStore, bsid) && _.has(ideaStore[bsid], iid)) {
          if (!ideaStore[bsid][iid].ratings) {
            ideaStore[bsid][iid].ratings = 0;
          }
          if (ideaStore[bsid][iid].rated) {
            ideaStore[bsid][iid].rated = false;
            ideaStore[bsid][iid].ratings = ideaStore[bsid][iid].ratings -= 1;
          } else {
            ideaStore[bsid][iid].rated = true;
            ideaStore[bsid][iid].ratings = ideaStore[bsid][iid].ratings += 1;
          }
        }

        return Restangular.one(ideasURL(bsid), iid).post('rate')
          .then(function (idea) {
            return updateIdeaInStore(bsid, idea);
          });
      };

      return bsResource;
    }
  ]);
