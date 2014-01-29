'use strict';

angular.module('braind')
  .factory('bdDate', ['$window',
    function ($window) {
      var service = {};

      service.formatFromNow = function (value) {
        var m, howOld,
          secondsUntilUpdate = null,
          fromNow = null,
          now = new Date();

        // parse to date if not already is
        if (!angular.isDate(value)) {
          value = new Date(value);
        }

        m = $window.moment(value);
        howOld = Math.abs($window.moment().diff(m, 'minute'));

        if (howOld < 22 * 60) {
          if (howOld < 1) {
            secondsUntilUpdate = 1;
          } else if (howOld < 50) {
            secondsUntilUpdate = 30;
          } else if (howOld < 22 * 60) {
            secondsUntilUpdate = 300;
          }
          fromNow = m.fromNow();
        } else {
          if (m.year() === now.getFullYear()) {
            fromNow = m.format('D. MMM HH:mm');
          } else {
            fromNow = m.format('D. MMM YYYY HH:mm');
          }
        }

        return {
          'fromNow': fromNow,
          'secondsUntilUpdate': secondsUntilUpdate
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
