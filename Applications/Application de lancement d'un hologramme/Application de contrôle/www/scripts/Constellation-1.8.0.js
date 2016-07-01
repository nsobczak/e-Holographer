/*
 *	 Constellation Platform 1.8
 *	 Web site: http://www.myConstellation.io
 *	 Copyright (C) 2014-2016 - Sebastien Warin <http://sebastien.warin.fr>	   	
 *	 All Rights Reserved.  
 *	
 *	 NOTICE:  All information contained herein is, and remains the property of Sebastien Warin.
 *	 The intellectual and technical concepts contained herein are proprietary to Sébastien Warin.
 *	 Dissemination of this information or reproduction of this material is strictly forbidden
 *   unless prior written permission is obtained from Sébastien Warin.	 
*/

/// <reference path="jquery-2.1.3.js" />
/// <reference path="jquery.signalR-2.2.0.js" />
(function ($, window, undefined) {
    /// <param name="$" type="jQuery" />
    "use strict";

    if (typeof ($.signalR) !== "function") {
        throw new Error("SignalR: SignalR is not loaded. Please ensure jquery.signalR-x.js is referenced before ~/signalr/js.");
    }

    var signalR = $.signalR;
    var groups = {};

    function makeProxyCallback(hub, callback) {
        return function () {
            // Call the client hub method
            callback.apply(hub, $.makeArray(arguments));
        };
    }

    function registerHubProxies(instance, shouldSubscribe) {
        var key, hub, memberKey, memberValue, subscriptionMethod;

        for (key in instance) {
            if (instance.hasOwnProperty(key)) {
                hub = instance[key];

                if (!(hub.hubName)) {
                    // Not a client hub
                    continue;
                }

                if (shouldSubscribe) {
                    // We want to subscribe to the hub events
                    subscriptionMethod = hub.on;
                } else {
                    // We want to unsubscribe from the hub events
                    subscriptionMethod = hub.off;
                }

                // Loop through all members on the hub and find client hub functions to subscribe/unsubscribe
                for (memberKey in hub.client) {
                    if (hub.client.hasOwnProperty(memberKey)) {
                        memberValue = hub.client[memberKey];

                        if (!$.isFunction(memberValue)) {
                            // Not a client hub function
                            continue;
                        }

                        subscriptionMethod.call(hub, memberKey, makeProxyCallback(hub, memberValue));
                    }
                }
            }
        }
    }

    $.hubConnection.prototype.createHubProxies = function (hub) {
        var proxies = {};
        var sagaCallbacks = {};

        this.starting(function () {
            // Register the hub proxies as subscribed
            // (instance, shouldSubscribe)
            registerHubProxies(proxies, true);

            this._registerSubscribedHubs();
        }).disconnected(function () {
            // Unsubscribe all hub proxies when we "disconnect".  This is to ensure that we do not re-add functional call backs.
            // (instance, shouldSubscribe)
            registerHubProxies(proxies, false);
        });

        if (hub == 'consumerHub') {
            proxies['Consumer'] = this.createHubProxy('consumerHub');
            proxies['Consumer'].client = {
                onReceiveMessage: function (callback) {
                    return proxies['Consumer'].on("ReceiveMessage", function (msg) {
                        var sagaCallback = sagaCallbacks[msg.Scope.SagaId];
                        if (sagaCallback != undefined) {
                            sagaCallback(msg);
                        }
                        delete sagaCallbacks[msg.Scope.SagaId];
                        if (callback != undefined) {
                            callback(msg);
                        }
                    });
                },
                onUpdateStateObject: function (callback) {
                    return proxies['Consumer'].on("UpdateStateObject", callback);
                }
            };
            proxies['Consumer'].server = {
                requestStateObjects: function (sentinelName, packageName, name, type) {
                    return proxies['Consumer'].invoke.apply(proxies['Consumer'], $.merge(["RequestStateObjects"], $.makeArray(arguments)));
                },

                sendMessage: function (scope, key, data) {
                    return proxies['Consumer'].invoke.apply(proxies['Consumer'], $.merge(["SendMessage"], $.makeArray(arguments)));
                },

                sendMessageWithSaga: function (scope, key, data, callback) {
                    scope.SagaId = new Date().getTime();
                    sagaCallbacks[scope.SagaId] = callback;
                    return proxies['Consumer'].server.sendMessage(scope, key, data);
                },

                subscribeMessages: function (group) {
                    return proxies['Consumer'].invoke.apply(proxies['Consumer'], $.merge(["SubscribeMessages"], $.makeArray(arguments)));
                },

                subscribeStateObjects: function (sentinelName, packageName, name, type) {
                    return proxies['Consumer'].invoke.apply(proxies['Consumer'], $.merge(["SubscribeStateObjects"], $.makeArray(arguments)));
                },

                unSubscribeMessages: function (group) {
                    return proxies['Consumer'].invoke.apply(proxies['Consumer'], $.merge(["UnSubscribeMessages"], $.makeArray(arguments)));
                },

                unSubscribeStateObjects: function (sentinelName, packageName, name, type) {
                    return proxies['Consumer'].invoke.apply(proxies['Consumer'], $.merge(["UnSubscribeStateObjects"], $.makeArray(arguments)));
                },

                requestSubscribeStateObjects: function (sentinelName, packageName, name, type) {
                    proxies['Consumer'].server.requestStateObjects(sentinelName, packageName, name, type);
                    return proxies['Consumer'].server.subscribeStateObjects(sentinelName, packageName, name, type);
                }
            };
        }
        else if (hub == 'controlHub') {
            proxies['Controller'] = this.createHubProxy('controlHub');
            proxies['Controller'].client = {
                onReceiveLogMessage: function (callback) {
                    groups.PackagesLog = true;
                    return proxies['Controller'].on("ReceiveLog", callback);
                },
                onUpdateSentinel: function (callback) {
                    groups.Sentinels = true;
                    return proxies['Controller'].on("UpdateSentinel", callback);
                },
                onUpdateSentinelsList: function (callback) {
                    return proxies['Controller'].on("UpdateSentinelsList", callback);
                },
                onReportPackageState: function (callback) {
                    groups.PackagesState = true;
                    return proxies['Controller'].on("ReportPackageState", callback);
                },
                onReportPackageUsage: function (callback) {
                    groups.PackagesUsage = true;
                    return proxies['Controller'].on("ReportPackageUsage", callback);
                },
                onUpdatePackageList: function (callback) {
                    return proxies['Controller'].on("UpdatePackageList", callback);
                },
                onUpdatePackageDescriptor: function (callback) {
                    return proxies['Controller'].on("UpdatePackageDescriptor", callback);
                }
            };
            proxies['Controller'].server = {
                addToControlGroup: function (group) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["AddToControlGroup"], $.makeArray(arguments)));
                },

                purgeStateObjects: function (sentinelName, packageName, name, type) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["PurgeStateObjects"], $.makeArray(arguments)));
                },

                reloadServerConfiguration: function (deployConfiguration) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["ReloadServerConfiguration"], $.makeArray(arguments)));
                },

                reload: function (sentinelName, packageName) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["Reload"], $.makeArray(arguments)));
                },

                removeToControlGroup: function (group) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["RemoveToControlGroup"], $.makeArray(arguments)));
                },

                requestPackageDescriptor: function (packageName) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["RequestPackageDescriptor"], $.makeArray(arguments)));
                },

                requestPackagesList: function (sentinelName) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["RequestPackagesList"], $.makeArray(arguments)));
                },

                requestSentinelsList: function () {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["RequestSentinelsList"], $.makeArray(arguments)));
                },

                requestSentinelUpdates: function () {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["RequestSentinelUpdates"], $.makeArray(arguments)));
                },

                restart: function (sentinelName, packageName) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["Restart"], $.makeArray(arguments)));
                },

                start: function (sentinelName, packageName) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["Start"], $.makeArray(arguments)));
                },

                stop: function (sentinelName, packageName) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["Stop"], $.makeArray(arguments)));
                },

                updatePackageSettings: function (sentinelName, packageName) {
                    return proxies['Controller'].invoke.apply(proxies['Controller'], $.merge(["UpdatePackageSettings"], $.makeArray(arguments)));
                }
            };
        }
        return proxies;
    };

    signalR.createConstellationConsumer = function (serverUri, accessKey, friendlyName) {
        signalR.consumerHub = $.hubConnection(serverUri, {
            useDefaultPath: true,
            qs: {
                "SentinelName": "Consumer",
                "PackageName": friendlyName,
                "AccessKey": accessKey
            }
        });
        $.extend(signalR, signalR.consumerHub.createHubProxies('consumerHub'));
        signalR.Consumer.client.onReceiveMessage();
        return signalR.Consumer;
    };

    signalR.createConstellationController = function (serverUri, accessKey, friendlyName) {
        signalR.controlHub = $.hubConnection(serverUri, {
            useDefaultPath: true,
            qs: {
                "SentinelName": "Controller",
                "PackageName": friendlyName,
                "AccessKey": accessKey
            }
        });
        signalR.controlHub.stateChanged(function (change) {
            if (change.newState === $.signalR.connectionState.connected) {
                for (var group in groups) {
                    if (groups[group] == true) {
                        signalR.Controller.server.addToControlGroup(group);
                    }
                }
            }
        });
        $.extend(signalR, signalR.controlHub.createHubProxies('controlHub'));
        return signalR.Controller;
    };

}(window.jQuery, window));