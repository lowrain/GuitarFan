/*
 * Browser Detection
 * � 2010 DevSlide Labs 
 * 
 * Visit us at: www.devslide.com/labs
 */

var notSupportedBrowsers = [{'os': 'Any', 'browser': 'MSIE', 'version': 8}];
var displayPoweredBy = false;
var noticeLang = 'mean';
var noticeLangCustom = null;
var supportedBrowsers = [];

var BrowserDetection = {
	init: function(){
		if(notSupportedBrowsers == null || notSupportedBrowsers.length < 1){
			notSupportedBrowsers = this.defaultNotSupportedBrowsers;
		}
		
		this.detectBrowser();
		this.detectOS();
		
		if(this.browser == '' || this.browser == 'Unknown' || this.os == '' || 
		   this.os == 'Unknown' || this.browserVersion == '' || this.browserVersion == 0)
		{
			return;
		}
		
		// Check if this is old browser
		var oldBrowser = false;
		for(var i = 0; i < notSupportedBrowsers.length; i++){
			if(notSupportedBrowsers[i].os == 'Any' || notSupportedBrowsers[i].os == this.os){
				if(notSupportedBrowsers[i].browser == 'Any' || notSupportedBrowsers[i].browser == this.browser){
					if(notSupportedBrowsers[i].version == "Any" || this.browserVersion <= parseFloat(notSupportedBrowsers[i].version)){
						oldBrowser = true;
						break;
					}
				} 
			}
		}
		
		if(oldBrowser){
			this.displayNotice();
		}
	},
	
	getEl: function(id){ return window.document.getElementById(id); },
	getElSize: function(id){ 
		var el = this.getEl(id); 
		if(el == null){ return null; } 
		return { 'width': parseInt(el.offsetWidth), 'height': parseInt(el.offsetHeight) }; 
	},
	getWindowSize: function(){
		if(typeof window.innerWidth != 'undefined'){
			return {'width': parseInt(window.innerWidth), 'height': parseInt(window.innerHeight)};
		} else {
			if(window.document.documentElement.clientWidth != 0){
				return {'width': parseInt(window.document.documentElement.clientWidth), 'height': parseInt(window.document.documentElement.clientHeight)};
			} else {
				return {'width': parseInt(window.document.body.clientWidth), 'height': parseInt(window.document.body.clientHeight)};
			}
		}
	},
	positionNotice: function(){
		var noticeSize = this.getElSize('browser-detection');
		var windowSize = this.getWindowSize();
		var noticeEl = this.getEl('browser-detection');
		
		if(noticeEl == null || noticeSize == null || windowSize == null || !windowSize.width || !windowSize.height){ return; }
		noticeEl.style.left = (windowSize.width - noticeSize.width) / 2 + "px";
		
		var offset = (this.browser == "MSIE" && this.browserVersion < 7) ? (window.document.documentElement.scrollTop != 0 ? window.document.documentElement.scrollTop : window.document.body.scrollTop) : 0;
		noticeEl.style.top = (windowSize.height - noticeSize.height - 20 + offset) + "px";
		this.noticeHeight = noticeSize.height;
	},
	
	displayNotice: function(){
		if(this.readCookie('bdnotice') == 1){
			return;
		}
		
		this.writeNoticeCode();
		this.positionNotice();
		
		var el = this;
		window.onresize = function(){ el.positionNotice(); };
		if(this.browser == "MSIE" && this.browserVersion < 7){
			window.onscroll = function(){ el.positionNotice(); };
		}
		
		this.getEl('browser-detection-close').onclick = function(){ el.remindMe(false); };
		this.getEl('browser-detection-remind-later').onclick = function(){ el.remindMe(false); };
		this.getEl('browser-detection-never-remind').onclick = function(){ el.remindMe(true); };
	},
	
	remindMe: function(never){
		this.writeCookie('bdnotice', 1, never == true ? 365 : 7);
		this.getEl('browser-detection').style.display = 'none';
		this.getEl('black_overlay').style.display = 'none';
	},
	
	writeCookie: function(name, value, days){
		var expiration = ""; 
		if(parseInt(days) > 0){
			var date = new Date();
			date.setTime(date.getTime() + parseInt(days) * 24 * 60 * 60 * 1000);
			expiration = '; expires=' + date.toGMTString();
		}
		
		document.cookie = name + '=' + value + expiration + '; path=/';
	},
	
	readCookie: function(name){
		if(!document.cookie){ return ''; }
		
		var searchName = name + '='; 
		var data = document.cookie.split(';');
		
		for(var i = 0; i < data.length; i++){
			while(data[i].charAt(0) == ' '){
				data[i] = data[i].substring(1, data[i].length);
			}
			
			if(data[i].indexOf(searchName) == 0){ 
				return data[i].substring(searchName.length, data[i].length);
			}
		}
		
		return '';
	},
	
	writeNoticeCode: function(){
		var title = '';
		var notice = '';
		var selectBrowser = '';
		var remindMeLater = '';
		var neverRemindAgain = '';
		
		var browsersList = null;		
		var code = '<div id="black_overlay"></div><div id="browser-detection"><a href="javascript:;" id="browser-detection-close">Close</a>';
		
		if(noticeLang == 'custom' && noticeLangCustom != null){
			title = noticeLangCustom.title;
			notice = noticeLangCustom.notice;
			selectBrowser = noticeLangCustom.selectBrowser;
			remindMeLater = noticeLangCustom.remindMeLater;
			neverRemindAgain = noticeLangCustom.neverRemindAgain;
		} else {
			var noticeTextObj = null;
			eval('noticeTextObj = this.noticeText.' + noticeLang + ';');
			
			if(!noticeTextObj){
				noticeTextObj = this.noticeText.professional;
			}
			
			title = noticeTextObj.title;
			notice = noticeTextObj.notice;
			selectBrowser = noticeTextObj.selectBrowser;
			remindMeLater = noticeTextObj.remindMeLater;
			neverRemindAgain = noticeTextObj.neverRemindAgain;
		}
		
		notice = notice.replace("\n", '</p><p class="bd-notice">');
		notice = notice.replace("{browser_name}", (this.browser + " " + this.browserVersion));
		
		code += '<p class="bd-title">' + title + '</p><p class="bd-notice">' + notice + '</p><p class="bd-notice"><b>' + selectBrowser + '</b></p>';
		
		if(supportedBrowsers.length > 0){
			browsersList = supportedBrowsers;
		} else {
			browsersList = this.supportedBrowsers;
		}
		
		code += '<ul class="bd-browsers-list">';
		for(var i = 0; i < browsersList.length; i++){
			code += '<li class="' + browsersList[i].cssClass + '"><a href="' + browsersList[i].downloadUrl + '" target="_blank">' + browsersList[i].name + '</a></li>';
		}		
		code += '</ul>';
		
		if(displayPoweredBy){
			code += '<div class="bd-poweredby">Powered by <a href="http://www.devslide.com/labs/browser-detection" target="_blank">DevSlide Labs</a></div>';
		}
		
		code += '<ul class="bd-skip-buttons">';
		code += '<li><button id="browser-detection-remind-later" type="button">' + remindMeLater + '</button></li>';
		code += '<li><button id="browser-detection-never-remind" type="button">' + neverRemindAgain + '</button></li>';
		code += '</ul>';
		code += '</div>';
		window.document.body.innerHTML += code;
	},

	detectBrowser: function(){
		this.browser = '';
		this.browserVersion = 0;
		
		if(/Opera[\/\s](\d+\.\d+)/.test(navigator.userAgent)){
			this.browser = 'Opera';
		} else if(/MSIE (\d+\.\d+);/.test(navigator.userAgent)){
			this.browser = 'MSIE';
		} else if(/Navigator[\/\s](\d+\.\d+)/.test(navigator.userAgent)){
			this.browser = 'Netscape';
		} else if(/Chrome[\/\s](\d+\.\d+)/.test(navigator.userAgent)){
			this.browser = 'Chrome';
		} else if(/Safari[\/\s](\d+\.\d+)/.test(navigator.userAgent)){
			this.browser = 'Safari';
			/Version[\/\s](\d+\.\d+)/.test(navigator.userAgent);
			this.browserVersion = new Number(RegExp.$1);
		} else if(/Firefox[\/\s](\d+\.\d+)/.test(navigator.userAgent)){
			this.browser = 'Firefox';
		}
		
		if(this.browser == ''){
			this.browser = 'Unknown';
		} else if(this.browserVersion == 0) {
			this.browserVersion = parseFloat(new Number(RegExp.$1));
		}		
	},
	
	// Detect operation system
	detectOS: function(){
		for(var i = 0; i < this.operatingSystems.length; i++){
			if(this.operatingSystems[i].searchString.indexOf(this.operatingSystems[i].subStr) != -1){
				this.os = this.operatingSystems[i].name;
				return;
			}
		}
		
		this.os = "Unknown";
	},
	
	//	Variables
	noticeHeight: 0,
	browser: '',
	os: '',
	browserVersion: '',
	supportedBrowsers: [
	       { 'cssClass': 'firefox', 'name': 'Mozilla Firefox', 'downloadUrl': 'http://www.getfirefox.com/' },
	       { 'cssClass': 'chrome', 'name': 'Google Chrome', 'downloadUrl': 'http://www.google.com/chrome/' },
	       { 'cssClass': 'msie', 'name': 'Internet Explorer', 'downloadUrl': 'http://www.getie.com/' },
	       { 'cssClass': 'opera', 'name': 'Opera', 'downloadUrl': 'http://www.opera.com/' },
	       { 'cssClass': 'safari', 'name': 'Apple Safari', 'downloadUrl': 'http://www.apple.com/safari/' }
	],
	operatingSystems: [
           { 'searchString': navigator.platform, 'name': 'Windows', 'subStr': 'Win' },
           { 'searchString': navigator.platform, 'name': 'Mac', 'subStr': 'Mac' },
           { 'searchString': navigator.platform, 'name': 'Linux', 'subStr': 'Linux' },
           { 'searchString': navigator.userAgent, 'name': 'iPhone', 'subStr': 'iPhone/iPod' }
	],
	defaultNotSupportedBrowsers: [{'os': 'Any', 'browser': 'MSIE', 'version': 6}],
	noticeText: {
    	   'professional': { "title": "Outdated Browser Detected", "notice": "Our website has detected that you are using an outdated browser. Using your current browser will prevent you from accessing features on our website. An upgrade is not required, but is strongly recommend to improve your browsing experience on our website.", "selectBrowser": "Use the links below to download a new browser or upgrade your existing browser.", "remindMeLater": "Remind me later", "neverRemindAgain": "No, don't remind me again" },
    	   'informal': { "title": "Whoaaa!", "notice": "It appears you're using an outdated browser which prevents access to some of the features on our website. While it's not required, you really should <b>upgrade or install a new browser</b>!", "selectBrowser": "Visit the official sites for popular browsers below:", "remindMeLater": "Not now, but maybe later", "neverRemindAgain": "No, don't remind me again" },
    	   'technical': { "title": "Old Browser Alert! <span class='bd-highlight'>DEFCON 5</span>", "notice": "Come on! If you are hitting our site, then you must at least be partially tech savvy. So, why the older browser? We're not asking you to brush off your old Fibonacci Heap and share it with the class. Just upgrade!\nI know, I know. You don't like to be told what to do. But, we're only asking you to upgrade so you can access all the latest, greatest features on our site. It's quick and easy. But, if you still want to skip it, that's cool. We will still welcome you &mdash; and your creepy old browser. :P", "selectBrowser": "Visit the official sites for popular browsers below:", "remindMeLater": "Remind me later", "neverRemindAgain": "No, don't remind me. I like my Commodore 64!" },
    	   'goofy': { "title": "Are You Serious?", "notice": "Are you really using <b>{browser_name}</b> as your browser?\nYou're surfing the web on a dinosaur (a dangerous one too &mdash; like a Tyrannosaurus or Pterodactyl or something scary like that). <b>Get with it and upgrade now!</b> If you do, we promise you will enjoy our site a whole lot more. :)", "selectBrowser": "Visit the official sites for popular browsers below:", "remindMeLater": "Maybe Later", "neverRemindAgain": "No, don't remind me again" },
    	   'mean': { "title": "呃，你的浏览器太过时了!", "notice": "快点装一个新的吧.", "selectBrowser": "主流浏览器的官方下载地址:", "remindMeLater": "下次再说，魂淡~", "neverRemindAgain": "滚犊子，放开我的浏览器！" }
	}
};