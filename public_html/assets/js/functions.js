// Browser detection for when you get desparate. A measure of last resort.
// http://rog.ie/post/9089341529/html5boilerplatejs

// var b = document.documentElement;
// b.setAttribute('data-useragent',  navigator.userAgent);
// b.setAttribute('data-platform', navigator.platform);

// sample CSS: html[data-useragent*='Chrome/13.0'] { ... }



(function(code) {

    code(window.jQuery, window, document);

}(function($, window, document) {

    function getTablesList(){
        return $.ajax({
            url: "/smyt_items/",
            type: "get"
        });
    }

    function getTableData(item){
        return $.ajax({
            url:item.href,
            type:"get"
        });
    }

    $(function() {
     
        getTablesList().done(function(data){
            var list = $("ol.tables"),
                listItems = "";
            $.each(data, function(index, value){
                var link = "<a href=" + value.url + ">" + value.title +"</a>"
                listItems += "<li>" + link + "</li>";
            });
            list.append(listItems);
            
            list.on("click", "li", function(e){
                e.preventDefault();
                getTableData(e.target).done(function(data){
                    console.log(data);
                })
            })

        });

    });

}));
