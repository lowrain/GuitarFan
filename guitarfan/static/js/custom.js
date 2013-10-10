/* add format method to String's prototype */
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
};

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

$(function() {
    $('.gt-landing .input-group').removeClass("hidden");
    $('.gt-landing .input-group').addClass("animated fadeInDown");
});

$(function() {
    $('.link-new-window').tooltip();
});

$(function(){
    if ($('#tagcloud')) {
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
                    $('#tagcloud').html(cloudHTML);
                }

                $("#tagcloud a").tagcloud({
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

    if ($('#stylecloud')) {
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
                    $('#stylecloud').html(cloudHTML);
                }

                $("#stylecloud a").tagcloud({
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

    $('.gt-tabs-header .letters .btn').click(function(){
        updateArtistBox($(this));
    });
});

function updateArtistBox(sender) {
    var letter = sender.text();
    var artistBox = $('.gt-tabs-header .artists');

    $('.gt-tabs-header .letters .btn-info').toggleClass('btn-info btn-default');
    sender.toggleClass('btn-info btn-default');

    if (sender.text() != 'All') {
        artistBox.fadeIn('slow');
    }
    else {
        artistBox.fadeOut('fast');
        return;
    }
    $.ajax({
        url: '/artists.json?letter=' + sender.text(),
        type: 'GET',
        dataType: 'json',
        beforeSend: function() {
            artistBox.html('<img class="ajax-loader" src="static/images/loading-1.gif" width="16px" height="11px" border="0" />');
        },
        success: function(data) {
            if (data && data.artists && data.artists.length > 0) {
                var html = '';
                for (var i=0; i<data.artists.length; i++) {
                    html += '<a href="javascript:void(0);">'+data.artists[i].name+'</a> ';
                }
                artistBox.html(html);
            }
            else {
                artistBox.html('暂时没有以字母 <b class="text-danger"> '+letter+'</b> 开头的艺人');
            }
        }
    });
}

function updateTabsBox() {

}
