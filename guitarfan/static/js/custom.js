/* add format method to String's prototype */
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
};

$(function() {
    //init animation effect
    $(".gt-index-tabs .hot-box, .gt-index-tabs .new-box").hover(
        function () {
            $(this).find('.icon').addClass("animated active rotateIn");
            $(this).find('h4').addClass("animated active fadeInRight");
        },
        function () {
            $(this).find('.icon').removeClass("animated active rotateIn");
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

    $('.gt-landing .input-group').removeClass("hidden");
    $('.gt-landing .input-group').addClass("animated fadeInDown");

    //init tooltip
    $('.link-new-window').tooltip();

    //init tag and style cloud
    if ($('#tagCloud')) {
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

    if ($('#styleCloud')) {
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
});

function TabsListOperator() {
    this.queryFilter = {
        artistLetter: 'All',
        artistCategoryId: 0,
        artistRegionId: 0,
        styleId: 0,
        artistIds: '',
        tagId: '',
        pageIndex: 1,
        orderBy: 'time'
    },
        this.artistFilterBox = $('.gt-tabs-header');
    this.artistLetters = $('.gt-tabs-header .letters');
    this.artistCategories = $('.gt-tabs-header .categories');
    this.artistRegions = $('.gt-tabs-header .regions');
    this.artistsBox = $('.gt-tabs-header .artists');
    this.tabsListBox = $('.gt-tabs-list');
    this.tabsListHeader = $('.gt-tabs-list .list-header');
    this.tabsListBody = $('.gt-tabs-list .list-body');
    this.tabsListPagination = $('.gt-tabs-list ul.pagination');

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
                    var html = '';
                    var categoryClass = '';
                    var artist = null;
                    for (var i=0; i<data.artists.length; i++) {
                        artist = data.artists[i];
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
                    _this.artistsBox.html(html);
                }
                else {
                    _this.artistsBox.html('暂时没有符合条件的的艺人');
                }
            }
        });
    };

    this.updateTabsListBox = function () {
        var conditionsHTML = '';
        var artistConditions = [];
        if (this.queryFilter.artistLetter == 'All' && this.queryFilter.artistCategoryId == 0 && this.queryFilter.artistRegionId == 0) {
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


        var _this = this;
        $.ajax({
            url: '/tabs.json',
            data: { queryFilter: _this.queryFilter },
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data && data.tabs && data.tabs.length > 0) {
                    var html = '<table width="100%">';
                    for (var i=0; i<data.tabs.length; i++) {
                        tab = data.tabs[i];
                        html += '<tr>';
                        html += '   <td width="45%">';
                        html += '       <i class="icon icon-file-alt"></i>&nbsp;&nbsp;';
                        html += '       <a href="#" class="link-tab-subject">' + tab.title + '</a>';
                        html += '           <a href="#" class="link-new-window" title="在新窗口中查看" data-toggle="在新窗口中查看" data-placement="right"><i class="icon-share-alt"></i></a>';
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
                    _this.tabsListBody.html(html);
                }
                else {
                    _this.tabsListBody.html('<br><center>暂时没有符合条件的的曲谱 >_<</center><br><br>');
                }
            }
        });
    };

    this.initialize = function () {
        if (!this.artistFilterBox || !this.tabsListBox) return;
        var _this = this;
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
            _this.updateArtistBox();
            _this.updateTabsListBox();
        });
        this.artistCategories.find('a').click(function () {
            if ($(this).hasClass('active')) return false;
            _this.artistCategories.find('.active').removeClass('active');
            $(this).addClass('active');
            _this.queryFilter.artistCategoryId = $(this).attr('rel');
            _this.queryFilter.artistIds = '';
            _this.updateArtistBox();
            _this.updateTabsListBox();
        });
        this.artistRegions.find('a').click(function () {
            if ($(this).hasClass('active')) return false;
            _this.artistRegions.find('.active').removeClass('active');
            $(this).addClass('active');
            _this.queryFilter.artistRegionId = $(this).attr('rel');
            _this.queryFilter.artistIds = '';
            _this.updateArtistBox();
            _this.updateTabsListBox();
        });
        this.artistsBox.on("click", 'a', function() {
            $(this).toggleClass('active');
            _this.queryFilter.artistIds = '';
            _this.artistsBox.find('.active').each(function () {
                var artistId = $(this).attr('rel');
                if (_this.queryFilter.artistIds != '') _this.queryFilter.artistIds += '|';
                _this.queryFilter.artistIds += artistId;
            });
            _this.updateTabsListBox();
        });
        this.tabsListHeader.find('button').click(function () {
            _this.tabsListHeader.find('.active').removeClass('active');
            $(this).addClass('active');
            _this.queryFilter.orderBy = $(this).attr('rel');
            _this.updateTabsListBox();
        });
        // TODO style/tag cloud

        this.tabsListPagination.find('a').click(function () {
            alert('pagination');
        });
    };
}
