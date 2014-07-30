/* add format method to String's prototype */
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
};

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function isMobile() {
    return (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))
}

function setFancyboxIframeScrollY(num) {
    var contents = $('.fancybox-iframe').contents();
    contents.scrollTop(contents.scrollTop() + num);
}

$(function() {
    BrowserDetection.init();

    //init landing
    if ($('.gt-landing').length > 0) {
        var landingImgUrl = '../static/images/landing' + parseInt(Math.random()*19+1) + '.jpg';
        $('.gt-landing').css('background-image', 'url(' + landingImgUrl + ')');
    }

    //init animation effect
    $(".gt-index-tabs .hot-box, .gt-index-tabs .new-box").hover(
        function () {
            $(this).find('.fa-circled').addClass("animated active rotateIn");
            $(this).find('h4').addClass("animated active fadeInRight");
        },
        function () {
            $(this).find('.fa-circled').removeClass("animated active rotateIn");
            $(this).find('h4').removeClass("animated active fadeInRight");
        }
    );

    $(".gt-styles, .gt-tags").hover(
        function () {
            $(this).find('h4').addClass("animated active fadeIn");
        },
        function () {
            $(this).find('h4').removeClass("animated active fadeIn");
        }
    );

    //fadein search box
    setTimeout(function() {
        $('.gt-landing .input-group').removeClass("hidden");
        $('.gt-landing .input-group').addClass("animated fadeInDown");
    }, 500);

    if (!isMobile()) {
        setTimeout(function() {
            $('.gt-landing .responsive-devices').removeClass("hidden");
            $('.gt-landing .responsive-devices').addClass("animated fadeInRight");
        }, 1500);
    }

    //init tooltip
    $('.link-new-window').tooltip();

    //search submit validation
    $('.search-form').submit(function() {
        if ($(this).find('input[name=search]').val() == '') {
            return false;
        }
        else {
            $(this).find('input[name=search]').val($(this).find('input[name=search]').val().trim());
            return true;
        }
    });

    //init tag and style cloud
    if ($('#tagCloud').length > 0) {
        $.ajax({
            url: '/tagcloud.json',
            type: 'GET',
            dataType: "json",
            success: function(data) {
                if (data && data.tags) {
                    var cloudHTML = '';
                    for (var i=0; i < data.tags.length; i++) {
                        cloudHTML += '<a href="/tabs?tag={0}" rel="{1}">{2}</a> '.format(data.tags[i]['tagId'], data.tags[i]['count'], data.tags[i]['tagName']);
                    }
                    $('#tagCloud').html(cloudHTML);
                }

                $("#tagCloud a").tagcloud({
                    size: {
                        start: 12,
                        end: 18,
                        unit: 'px'
                    },
                    color: {
                        start: "#CDE",
                        end: "#F52"
                    }
                });
            }
        });
    }

    if ($('#styleCloud').length > 0) {
        $.ajax({
            url: '/stylecloud.json',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                if (data && data.styles) {
                    var cloudHTML = '';
                    for (var i=0; i < data.styles.length; i++) {
                        cloudHTML += '<a href="/tabs?style={0}" rel="{1}">{2}</a> '.format(data.styles[i]['styleId'], data.styles[i]['count'], data.styles[i]['styleName']);
                    }
                    $('#styleCloud').html(cloudHTML);
                }

                $("#styleCloud a").tagcloud({
                    size: {
                        start: 12,
                        end: 18,
                        unit: 'px'
                    },
                    color: {
                        start: "#CDE",
                        end: "#F52"
                    }
                });
            }
        });
    }

    $('.link-tab-subject').fancybox({
        type: 'iframe',
        padding : 0,
        width: 850,
        height: '100%',
        title: 'Tips: 鼠标滚轮或者 ↑ ↓ 键可以浏览完整曲谱',
        helpers: {
            overlay : {
                closeClick: false,
                showEarly  : true
            },
            title: {
                type: 'over'
            }
        },
        iframe: {
            scrolling : 'auto',
            preload: false
        },
        afterLoad: function() {
            if (isMobile()) {
                this.title = '';
            }
            else {
                // mosuse over/out to show/hide tips
                $(".fancybox-title").wrapInner('<div />').show();
                $(".fancybox-wrap").hover(function() {
                    $(".fancybox-title").show();
                }, function() {
                    $(".fancybox-title").hide();
                });

                $(document).keydown(function(e) {
                    // 38-up, 40-down
                    switch(e.keyCode) {
                        case 38:
                            setFancyboxIframeScrollY(-100);
                            break;
                        case 40:
                            setFancyboxIframeScrollY(100);
                            break;
                    }
                });
                var mousewheelevt = (/Firefox/i.test(navigator.userAgent)) ? "DOMMouseScroll" : "mousewheel" //FF doesn't recognize mousewheel as of FF3.x
                $('.fancybox-overlay').bind(mousewheelevt, function(e){
                    var evt = window.event || e //equalize event object
                    evt = evt.originalEvent ? evt.originalEvent : evt; //convert to originalEvent if possible
                    var delta = evt.detail ? evt.detail*(-40) : evt.wheelDelta //check for detail first, because it is used by Opera and FF
                    setFancyboxIframeScrollY(delta * -1);
                });
            }

            // TODO add functional buttons
        },
        afterClose: function() {
            $(document).unbind('keydown');
        }
    });

//    $('.fm_link').fancybox({
//        type: 'iframe',
//        padding : 0,
//        scrollOutside: true,
//        width: 920,
//        height: 370,
//        iframe: {
//            scrolling : 'no'
//        }
//    });
});

function TabsListOperator() {
    this.queryFilter = {
        artistLetter: 'All',
        artistCategoryId: 0,
        artistRegionId: 0,
        artistIds: '',
        styleId: 0,
        tagId: '',
        pageIndex: 1,
        orderBy: 'time',
        search: ''
    };
    this.artistFilterBox = $('.gt-tabs-header');
    this.artistLetters = $('.gt-tabs-header .letters');
    this.artistCategories = $('.gt-tabs-header .categories');
    this.artistRegions = $('.gt-tabs-header .regions');
    this.artistsBox = $('.gt-tabs-header .artists');
    this.tabsListBox = $('.gt-tabs-list');
    this.tabsListHeader = $('.gt-tabs-list .list-header');
    this.tabsListBody = $('.gt-tabs-list .list-body');
    this.pagination = $('.gt-tabs-list ul.pagination');

    this.initialize = function () {
        if (!this.artistFilterBox || !this.tabsListBox) return;
        var _this = this;
        if (this.artistFilterBox.length > 0) {
            this.artistLetters.find('button').click(function () {
                if ($(this).hasClass('btn-info')) return false;
                var letter = $(this).text();
                _this.artistLetters.find('.btn-info').toggleClass('btn-info btn-default');
                $(this).toggleClass('btn-info btn-default');

                if (letter != 'All') {
                    _this.artistsBox.fadeIn('slow');
                }
                else {
                    _this.artistsBox.hide();
                }
                _this.queryFilter.artistLetter = letter;
                _this.queryFilter.artistIds = '';
                _this.queryFilter.pageIndex = 1;
                _this.updateArtistBox();
                _this.updateConditionText();
                _this.updateTabsListBox();

                return false;
            });
            this.artistCategories.find('a').click(function () {
                if ($(this).hasClass('active')) return false;
                _this.artistCategories.find('.active').removeClass('active');
                $(this).addClass('active');
                _this.queryFilter.artistCategoryId = $(this).attr('rel');
                _this.queryFilter.artistIds = '';
                _this.queryFilter.pageIndex = 1;
                _this.updateArtistBox();
                _this.updateConditionText();
                _this.updateTabsListBox();

                return false;
            });
            this.artistRegions.find('a').click(function () {
                if ($(this).hasClass('active')) return false;
                _this.artistRegions.find('.active').removeClass('active');
                $(this).addClass('active');
                _this.queryFilter.artistRegionId = $(this).attr('rel');
                _this.queryFilter.artistIds = '';
                _this.queryFilter.pageIndex = 1;
                _this.updateArtistBox();
                _this.updateConditionText();
                _this.updateTabsListBox();

                return false;
            });
            this.artistsBox.on('click', 'a', function() {
                $(this).toggleClass('active');
                _this.queryFilter.artistIds = '';
                _this.artistsBox.find('.active').each(function () {
                    var artistId = $(this).attr('rel');
                    if (_this.queryFilter.artistIds != '') _this.queryFilter.artistIds += '|';
                    _this.queryFilter.artistIds += artistId;
                });
                _this.queryFilter.pageIndex = 1;
                _this.updateConditionText();
                _this.updateTabsListBox();

                return false;
            });
        }
        this.tabsListHeader.find('button').click(function () {
            if ($(this).hasClass('active')) return false;
            _this.tabsListHeader.find('.active').removeClass('active');
            $(this).addClass('active');
            _this.queryFilter.pageIndex = 1;
            _this.queryFilter.orderBy = $(this).attr('rel');
            _this.updateTabsListBox();

            return false;
        });
        this.pagination.on('click', 'a', function () {
            var pageIndex = $(this).text().trim().replace('...', '');
            if (pageIndex == '前页') {
                _this.queryFilter.pageIndex--;
            }
            else if (pageIndex == '后页') {
                _this.queryFilter.pageIndex++;
            }
            else {
                _this.queryFilter.pageIndex = parseInt(pageIndex);
            }
            _this.updateTabsListBox();

            return false;
        });
    };

    this.updateArtistBox = function () {
        var loadingHTML = '<img class="ajax-loader" src="static/images/loading-1.gif" width="16px" height="11px" border="0" />';
        if (this.queryFilter.artistLetter == 'All') {
            this.artistsBox.html(loadingHTML);
            return;
        }
        var _this = this;
        $.ajax({
            url: '/artists.json',
            data: { queryFilter: _this.queryFilter },
            type: 'POST',
            dataType: 'json',
            beforeSend: function() {
                _this.artistsBox.html(loadingHTML);
            },
            success: function(data) {
                if (data && data.artists && data.artists.length > 0) {
                    _this.artistsBox.html(buildArtistsHTML(data.artists));
                }
                else {
                    _this.artistsBox.html('暂时没有符合条件的的艺人');
                }
            }
        });
    };

    this.updateConditionText = function () {
        var conditionsHTML = '';
        var artistConditions = [];
        if (this.queryFilter.artistIds.length > 0) {
            this.artistsBox.find('a.active').slice(0, 3).each(function () {
                artistConditions.push($(this).text());
            });
            if (this.artistsBox.find('a.active').length > 3) {
                artistConditions.push('···');
            }
        }
        else if (this.queryFilter.artistLetter == 'All' && this.queryFilter.artistCategoryId == 0 && this.queryFilter.artistRegionId == 0) {
            artistConditions.push('所有');
        }
        else {
            if (this.queryFilter.artistLetter != 'All') artistConditions.push('字母' + this.queryFilter.artistLetter);
            if (this.queryFilter.artistCategoryId != 0) artistConditions.push(this.artistCategories.find('a.active').text());
            if (this.queryFilter.artistRegionId != 0) artistConditions.push(this.artistRegions.find('a.active').text());
        }
        if (artistConditions.length > 0) {
            conditionsHTML = '艺人：';
            for (var i = 0; i < artistConditions.length; i++) {
                if (i > 0) conditionsHTML += ' + ';
                conditionsHTML += '<span class="label">' + artistConditions[i] + '</span>';
            }
        }
        this.tabsListHeader.find('.header-text > span').html(conditionsHTML);
    };

    this.updateTabsListBox = function () {
        var _this = this;
        $.ajax({
            url: '/tabs.json',
            data: {
                queryFilter: _this.queryFilter
            },
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data && data.tabs && data.tabs.length > 0) {
                    _this.tabsListBody.html(buildTabsListHTML(data.tabs));
                    _this.pagination.html(buildPaginationHTML(data.pageIndex, data.pageCount));
                }
                else {
                    _this.tabsListBody.html('<br><br><center>暂时没有符合条件的的曲谱 >_<</center>');
                    _this.pagination.html('');
                }

                if (_this.queryFilter.search != '') {
                    _this.colorSearchKeyword();
                }
            }
        });
    };

    this.colorSearchKeyword = function () {
        var keyword = this.queryFilter.search;
        this.tabsListBody.find('a.link-tab-subject, a.link-list-artist').highlight(keyword);
    };


    function buildArtistsHTML(artists) {
        var html = '';
        var categoryClass = '';
        var artist = null;
        for (var i=0; i<artists.length; i++) {
            artist = artists[i];
            switch (artist.category) {
                case 1:
                    categoryClass = 'male';
                    break;
                case 2:
                    categoryClass = 'female';
                    break;
                case 3:
                    categoryClass = 'group';
                    break;
                case 4:
                    categoryClass = 'band';
                    break;
                default:
                    categoryClass = 'other';
                    break;
            }
            html += '<a href="javascript:void(0);" class="{0}" rel="{1}">{2}</a> '.format(categoryClass, artist.id, artist.name);
        }
        return html;
    }

    function buildTabsListHTML(tabs) {
        var html = '<table width="100%">';
        for (var i=0; i<tabs.length; i++) {
            tab = tabs[i];
            html += '<tr>';
            html += '   <td width="45%">';
            html += '       <i class="fa fa-file-alt"></i>&nbsp;&nbsp;';
            html += '       <a href="/tabview/' + tab.id + '?popup" class="link-tab-subject" target="_blank">' + tab.title + '</a>';
            html += '           <a href="/tabview/' + tab.id + '" class="link-new-window" title="在新窗口中查看" data-toggle="在新窗口中查看" data-placement="right" target="_blank"><i class="icon-share-alt"></i></a>';
            html += '   </td>';
            html += '   <td width="8%" class="tab-style">' + tab.style + '</td>';
            html += '   <td width="8%" class="tab-difficulty">' + tab.difficalty + '</td>';
            html += '   <td width="10%" class="tab-hits">' + tab.hits + '次</td>';
            html += '   <td align="right">';
            html += '       <a href="/tabs?artist=' + tab.artistId + '" class="link-list-artist pull-right">' + tab.artistName + '</a>';
            html += '   </td>'
            html += '</tr>'
        }
        html += '</table>'
        return html;
    }

    function buildPaginationHTML(pageIndex, pageCount) {
        var html = '';
        if (pageCount == 1) return html;

        var pageStart = 0, pageEnd = 0;
        if (pageIndex < 9) {
            pageStart = 1;
            if (pageCount > 10)
                pageEnd = 10;
            else
                pageEnd = pageCount;
        }
        else if (pageIndex < pageCount - 8) {
            pageStart = pageIndex - 5;
            pageEnd = pageIndex + 4;
        }
        else {
            pageStart = pageCount - 9;
            pageEnd = pageCount;
        }

        if (pageIndex > 1) {
            html += '<li><a href="javascript:void(0);"><i class="fa fa-chevron-left"></i> 前页</a></li>'
        }

        if (pageStart > 1) {
            html += '<li><a href="javascript:void(0);")>1...</a></li>';
        }

        for (var i=pageStart; i<=pageEnd; i++) {
            if (i == pageIndex) {
                html += '<li class="active"><span>' + i + '</span></li>';
            }
            else {
                html += '<li><a href="javascript:void(0)">' + i + '</a></li>';
            }
        }

        if (pageEnd < pageCount) {
            html += '<li><a href="/tabs/"' + pageCount + '>...' + pageCount + '</a></li>';
        }

        if (pageIndex < pageCount) {
            html += '<li><a href="javascript:void(0);">后页 <i class="fa fa-chevron-right"></i></a></li>';
        }
        return html;
    }
}