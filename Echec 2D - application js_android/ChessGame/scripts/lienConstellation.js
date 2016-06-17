//________________________________________________________________________________________________________________

var constellation = $.signalR.createConstellationConsumer(
    "http://nicolas:8088", "1a6afb7aef6ed90fbf767e3a19df75267d489660", "TestConnection");



constellation.connection.stateChanged(function (change) {
    if (change.newState === $.signalR.connectionState.connected) {
        $("#state").text("Connecte");

        constellation.server.sendMessage({ Scope: 'Package', Args: ['HolographerPythonPackage'] },
            'InfosConnection', '');

    }
    else {
        $("#state").text("Non connecte");
    }
});



constellation.connection.start();

$("#demoChessGame").click(function () {
    constellation.server.sendMessage({ Scope: 'Package', Args: ['HolographerPythonPackage'] },
        'PlateauDeDepart', '');
});

//________________________________________________________________________________________________________________
