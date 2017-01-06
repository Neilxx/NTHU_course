
var myRating0;
var myRating1;
var myRating2;
var maxRating= 5;
var callback0 = function(rating) { 
    FB.getLoginStatus(function(response) {
        console.log("click 0");
        if (response.status === 'connected') {
            // getRating(response.authResponse.userID, els);            
            postRating(rating,response.authResponse.userID,0);
        } else if (response.status === 'not_authorized') {      
            console.log("not_authorized = =");
            // window.location = loginUrl;
            FBlogin(0,els);
        } else {
            console.log("?? = =");                    
            FBlogin(0,els);
        }
    });
};
var callback1 = function(rating) { 
    FB.getLoginStatus(function(response) {
        console.log("click 1");
        if (response.status === 'connected') {
            // getRating(response.authResponse.userID, els);
            postRating(rating,response.authResponse.userID,1);
        } else if (response.status === 'not_authorized') {      
            console.log("not_authorized = =");
            // window.location = loginUrl;
            FBlogin(1,els);
        } else {
            console.log("?? = =");                    
            FBlogin(1,els);
        }
    });
};
var callback2 = function(rating) { 
    console.log("click 2");
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            // getRating(response.authResponse.userID, els);
            postRating(rating,response.authResponse.userID,2);
        } else if (response.status === 'not_authorized') {      
            console.log("not_authorized = =");
            // window.location = loginUrl;
            FBlogin(2,els);
        } else {
            console.log("?? = =");                    
            FBlogin(2,els);
        }
    });
};
function postRating(rating, user_id, idx) {
    console.log("post rating");
    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        } 
        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }); 
    var scores = [myRating0.getRating(), myRating1.getRating(), myRating2.getRating()]
    $.ajax({
        type: "POST",
        url: "rating/",
        data: {
             score: scores[idx],
             user_id: user_id,
             idx: idx
        },
        success: function(data) {
            console.log(data);
            console.log('#score'+idx);
            $('#score'+idx).html(data['score'].toFixed(2));
            $('#people'+idx).html(data['people']);
            $('#noRating0').remove();
            $('#noRating1').remove();
            $('#noRating2').remove();
        },                
        error: function(xhr, status, error) {
            console.log("post error!!");
        }
    });    
}
var currentRating = 0;
function getRating(user_id, els){
    console.log("get rating");
    $.ajax({
        type: "GET",
        url: "rating/",
        data: {
             user_id: user_id,
        },
        success: function(data) {
            myRating0 = rating(els[0], data['score0'], maxRating, callback0);
            myRating1 = rating(els[1], data['score1'], maxRating, callback1);
            myRating2 = rating(els[2], data['score2'], maxRating, callback2);
    
            // myRating0.setRating(data['score0']);
            // myRating1.setRating(data['score1']);
            // myRating2.setRating(data['score2']);
            // currentRating = data['rating'];
            console.log("test get "+data['rating']);
        },                
        error: function(xhr, status, error) {
            console.log("get error!!");
        }
    });   
}
// window.fbApp = {
    // id: '1234567891011',
    // scope: 'user_about_me,publish_stream,email,user_likes,friends_photos,read_stream',
    // LoginRedirectUrl: '{放置從Facebook網站授權完後需要回到的頁面網址}',
    // getLoginUrl: function () {  //取得Facebook授權頁面網址
        // var login_url = "https://www.facebook.com/dialog/oauth?";
        // login_url += ("client_id=" + this.id);
        // login_url += ("&redirect_uri=" + this.LoginRedirectUrl);
        // login_url += ("&scope=" + this.scope);
        // return login_url;
    // },
// };
function FBlogin(idx, els){
    FB.login(function(response){
        if (response.status === 'connected') {
            postRating(rating,response.authResponse.userID,idx);
            $.ajax({
                type: "GET",
                url: "rating/",
                data: {
                    user_id: response.authResponse.userID,
                },
                success: function(data) {
                    if(idx==0){
                        myRating1.setRating(data['score1']);
                        myRating2.setRating(data['score2']);
                    }else if(idx==1){
                        myRating0.setRating(data['score0']);
                        myRating2.setRating(data['score2']);
                    }else if(idx==2){
                        myRating1.setRating(data['score1']);
                        myRating0.setRating(data['score0']);
                    }
                },                
                error: function(xhr, status, error) {
                    console.log("get error!!");
                }
            });   
            
            
        }else{
            myRating0.setRating(0,false);
            myRating1.setRating(0,false);
            myRating2.setRating(0,false);
            console.log('rating failed');
        }
    });
}
function createRating(){  
    console.log("create rating");
    els = document.querySelectorAll('.c-rating');
    
    // myRating0 = rating(els[0], currentRating, maxRating, callback0);
    // myRating1 = rating(els[1], currentRating, maxRating, callback1);
    // myRating2 = rating(els[2], currentRating, maxRating, callback2);
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            console.log("call getRating");
            getRating(response.authResponse.userID, els);            
            // myRating0 = rating(els[0], 0, maxRating, callback0);
            // myRating1 = rating(els[1], 0, maxRating, callback1);
            // myRating2 = rating(els[2], 0, maxRating, callback2);
        }else{
            console.log('no login or authorize');
            var newEl0 = document.createElement('div');
            var newEl1 = document.createElement('div');
            var newEl2 = document.createElement('div');
            newEl0.id = 'noRating0';
            newEl1.id = 'noRating1';
            newEl2.id = 'noRating2';
            newEl0.className = 'row';
            newEl1.className = 'row';
            newEl2.className = 'row';
            newEl0.innerText = '你還沒有登入呦~';
            newEl1.innerText = '你還沒有登入呦~';
            newEl2.innerText = '你還沒有登入呦~';
            els[0].parentElement.append(newEl0);
            els[1].parentElement.append(newEl1);
            els[2].parentElement.append(newEl2);
            myRating0 = rating(els[0], 0, maxRating, callback0);
            myRating1 = rating(els[1], 0, maxRating, callback1);
            myRating2 = rating(els[2], 0, maxRating, callback2);
        }
    },true);
}