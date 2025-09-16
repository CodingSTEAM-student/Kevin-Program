$bw.web.gameServices = new (function() {
    var that = this;

    function signIn(data) {
        console.log('web signIn', data);
    }

    function showLeaderboard(data) {
        console.log('web showLeaderboard', data);
    }

    function showAllLeaderboards(data) {
        console.log('web showAllLeaderboards', data);
    }

    function showAchievements(data) {
        console.log('web showAchievements', data);
    }

    function unlockAchievement(data) {
        console.log('web unlockAchievement', data);
    }

    function revealAchievement(data) {
        console.log('web revealAchievement', data);
    }

    function getState(data) {
        console.log('web getState', data);
    }

    function setScore(data) {
        console.log('web setScore', data);
    }

    this.signIn = signIn;
    this.showLeaderboard = showLeaderboard;
    this.showAllLeaderboards = showAllLeaderboards;
    this.showAchievements = showAchievements;
    this.unlockAchievement = unlockAchievement;
    this.revealAchievement = revealAchievement;
    this.getState = getState;
    this.setScore = setScore;
})();