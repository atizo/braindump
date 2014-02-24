'use strict';

angular.module('bdFilters', [])
  .filter('bdToArray', function () {
    /* Workaround for the object ordering problem:
       https://github.com/angular/angular.js/issues/1286
     */
    return function (obj) {
      var prop;

      if (!(obj instanceof Object)) {
        return obj;
      }

      return Object.keys(obj).map(function (key) {
        prop = Object.create(null);
        prop.value = key;
        return Object.defineProperty(obj[key], '$key', prop);
      });
    };
  });