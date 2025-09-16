$bw.gameServices = new (function() {
    var that = this,
            _uid = 1,
            _moduleId = 'gameservices';

    function signInFailed(data) {
        $bw.debug.log('sign in failed', data);
        $bw.debug.log('failed auto-signin');
    }

    function signInSucceeded(data) {
        $bw.debug.log('sign in succeeded', data);		
        alert('succeeded signin');
        // todo: paas alle scores van te halen leaderboards
        // todo: paas unlocked achievements
    }

    function connect() {
        $bw.doAction(_moduleId + '.connect');
        return that;
    }

    function signIn() {
        $bw.debug.log('$bw.gameServices.signIn')
        $bw.doAction(_moduleId + '.signin');
        return that;
    }

    function showLeaderboard(id) {
        $bw.doAction(_moduleId + '.showLeaderboard', {
            leaderboard: id // constants.LEAD_STARS
        });
        return that;
    }

    function showAllLeaderboards() {
        $bw.doAction(_moduleId + '.showAllLeaderboards');
        return that;
    }

    function showAchievements() {
        $bw.doAction(_moduleId + '.showAchievements');
        return that;
    }

    function unlockAchievement(id) {
        $bw.doAction(_moduleId + '.unlockAchievement', {
            achievement: id
        });
        return that;
    }

    function revealAchievement() {
        $bw.doAction(_moduleId + '.revealAchievement', {
            achievement: id
        });
        return that;
    }

    function getState(handler) {
        var callbackHandlerName = _moduleId + 'Callback' + _uid++;
        window[callbackHandlerName] = function(data) {
            $bw.debug.log('$bw.gameServices.getState callback ', callbackHandlerName, 'fired with data', data);
            //data = JSON.parse(data);
            //handler(data);
            delete window.callbackHandlerName;
        }
        $bw.doAction(_moduleId + '.getState');
        return that;
    }

    function setScore(id, score) {
        $bw.doAction(_moduleId + '.setScore', {
            leaderboard: id,
            score: score
        });
        return that;
    }

    this.signInFailed = signInFailed;
    this.signInSucceeded = signInSucceeded;
    this.signIn = signIn;
    this.connect = connect;
    this.showLeaderboard = showLeaderboard;
    this.showAllLeaderboards = showAllLeaderboards;
    this.showAchievements = showAchievements;
    this.unlockAchievement = unlockAchievement;
    this.revealAchievement = revealAchievement;
    this.getState = getState;
    this.setScore = setScore;

})();

window.bubbleWrappGameServicesSignInFailed = function(data) {
    $bw.gameServices.signInFailed(data);
}
window.bubbleWrappGameServicesSignInSucceeded = function(data) {
    $bw.gameServices.signInSucceeded(data);
}
