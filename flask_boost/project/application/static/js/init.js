(function () {
    "use strict";

    // Find out params in routing rules
    var pattern = new RegExp("<[^:]*:?([^>]+)>", "g");
    var result = null;

    $.each(g.rules, function (endpoint, rules) {
        $.each(rules, function (index, rule) {
            rule.params = [];
            while ((result = pattern.exec(rule.rule)) !== null) {
                rule.params.push(result[1]);
            }
        });
    });

    /**
     * Generate url for the endpoint.
     * urlFor(endpoint [, parameters] [, external])
     * @param endpoint
     * @param parameters
     * @param external
     * @returns url for the endpoint.
     */
    function urlFor(endpoint, parameters, external) {
        var url = null,
            params = [],
            maxMatchDegree = 0.0,
            keys;

        if ($.type(parameters) === "boolean") {
            external = parameters
        }

        parameters = ($.type(parameters) !== 'undefined') ? parameters : {};
        external = ($.type(external) !== 'undefined') ? external : false;

        if (g.rules[endpoint] === undefined) {
            throw new Error("Uncorrect endpoint in urlFor(\"" + endpoint + "\", " +
                JSON.stringify(parameters) + ")");
        }

        keys = $.map(parameters, function (value, key) {
            return key;
        });

        // Find the first matched rule among rules in this endpoint.
        $.each(g.rules[endpoint], function (index, rule) {
            var match = true,
                currentMatchDegree = 0.0;

            $.each(rule.params, function (index, param) {
                if ($.inArray(param, keys) === -1) {
                    match = false;
                    return false;
                }
            });

            if (match) {
                currentMatchDegree = parseFloat(rule.params.length) / keys.length;
                if (currentMatchDegree > maxMatchDegree || url === null) {
                    maxMatchDegree = currentMatchDegree;
                    url = rule.rule;
                    params = rule.params;
                }
            }
        });

        if (url) {
            $.each(keys, function (index, key) {
                // Build in params
                if ($.inArray(key, params) > -1) {
                    url = url.replace(new RegExp("<[^:]*:?" + key + ">"), parameters[key]);
                } else {
                    // Query string params
                    if (url.indexOf("?") === -1) {
                        url += "?";
                    }
                    if (!endsWith(url, '?')) {
                        url += "&";
                    }
                    url += key + "=" + parameters[key];
                }
            });
        } else {
            throw new Error("Uncorrect parameters in urlFor(\"" + endpoint + "\", " +
                JSON.stringify(parameters) + ")");
        }

        if (external) {
            url = g.domain + url
        }

        return url;
    }

    /**
     * Check whether str ends with suffix.
     * @param str
     * @param suffix
     * @returns {boolean}
     */
    function endsWith(str, suffix) {
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    }

    /**
     * Register context into global variable g.
     * @param context
     */
    function registerContext(context) {
        if (typeof g === 'undefined') {
            throw new Error("Global variable g is not defined.");
        }

        $.each(context, function (key, value) {
            if (g.hasOwnProperty(key)) {
                throw new Error("The key '" + key + "' already exists in the global variable g.");
            }
            g[key] = value;
        });
    }

    /**
     * Find elements in #main
     * @param selector
     * @returns {*|jQuery}
     */
    function $page(selector) {
        return $('#main').find(selector);
    }

    window.$page = $page;
    window.urlFor = urlFor;
    window.registerContext = registerContext;
})();
