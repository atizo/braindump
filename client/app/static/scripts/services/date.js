'use strict';

angular.module('braind')
  .factory('bdDate', ['$window', '$timeout', '$exceptionHandler',
    function ($window, $timeout, $exceptionHandler) {
      var service = {},
        registry = {};

      var isOld = function (value) {
        return Math.abs($window.moment().diff($window.moment(value), 'minute')) >= 22 * 60;
      };

      var getFormatted = function (value) {
        var m,
          fromNow,
          now = new Date();

        m = $window.moment(value);

        if (!isOld(value)) {
          fromNow = m.fromNow();
        } else {
          if (m.year() === now.getFullYear()) {
            fromNow = m.format('D. MMM HH:mm');
          } else {
            fromNow = m.format('D. MMM YYYY HH:mm');
          }
        }
        return fromNow;
      };

      var update = function () {
        _.forOwn(registry, function (listeners, value) {
          var i, length;
          for (i = 0, length = listeners.length; i < length; i++) {

            // if listeners were deregistered, defragment the array
            if (!listeners[i]) {
              listeners.splice(i, 1);
              i--;
              length--;
              continue;
            }
            try {
              listeners[i].apply(null, [getFormatted(value)]);
            } catch (e) {
              $exceptionHandler(e);
            }
          }
        });

        $timeout(update, 30 * 1000);
      };

      $timeout(update, 1000);

      service.formatFromNow = function (value, cb) {
        if (!angular.isDate(value)) {
          value = new Date(value);
        }

        cb.apply(null, [getFormatted(value)]);

        if (isOld(value)) {
          return angular.noop;
        }

        var valueListeners = registry[value];
        if (!valueListeners) {
          registry[value] = valueListeners = [];
        }
        valueListeners.push(cb);

        return function () {
          valueListeners[indexOf(valueListeners, cb)] = null;
        };
      };

      service.format = function (value, format) {
        // parse to date if not already is
        if (!angular.isDate(value)) {
          value = new Date(value);
        }

        // define default format
        if (!angular.isDefined(format)) {
          format = 'D. MMM YYYY HH:mm';
        }

        var moment = $window.moment(value);
        if (angular.isDefined(format)) {
          return moment.format(format);
        }

        return moment.toString();
      };

      return service;
    }
  ]);
