
function StartMeeting(){
    const domain = 'meet.jit.si';
    const options = {
        roomName: 'JitsiMeetAPIExample123',
        width: '100%',
        height: '100%',
        parentNode: document.querySelector('#jitsi-meet-conf-container'),
        configOverwrite: {
            disableDeepLinking: true,
        },
        interfaceConfigOverwrite: {
            SHOW_CHROME_EXTENSION_BANNER: false,
        },
    };
    api = new JitsiMeetExternalAPI(domain, options);

    return api;
}

function ScreenShot(){
    apiObj.captureLargeVideoScreenshot().then(data => {
        console.log(data.dataURL);   
        var a = document.createElement("a"); //Create <a>
        a.href = data.dataURL; //Image Base64 Goes here
        a.download = "Image.png"; //File name Here
        a.click(); //Downloaded file

    });
}