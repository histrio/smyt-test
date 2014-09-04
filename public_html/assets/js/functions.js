// Browser detection for when you get desparate. A measure of last resort.
// http://rog.ie/post/9089341529/html5boilerplatejs

// var b = document.documentElement;
// b.setAttribute('data-useragent',  navigator.userAgent);
// b.setAttribute('data-platform', navigator.platform);

// sample CSS: html[data-useragent*='Chrome/13.0'] { ... }



(function(code) {

    code(window.jQuery, window, document);

}(function($, window, document) {

    var meta = {};

    function getTablesList(){
        return $.ajax({
            url: "/smyt_items/",
            type: "get"
        });
    }


    function getData(url) {
        return $.ajax({
            url:url,
            type:"get"
        });
    }

    function getField(fld){
        var field = $("<input>",{
            legend:fld.title,
            name:fld.name,
            type:'text'
        });
        if (fld.type=="DateField"){
            field.datepicker();
        }
        return field
    }


    function updateForm(item){
        getData(item.href).done(function(data){
            var table_meta = meta[item.id],
                table = $("<table>"),
                form = $("<form>",{ action:item.href, method:"post" }),
                head = $("<tr>"),
                table_fields = $.grep(table_meta, function(fld){
                    return fld.type != 'AutoField'
                });

            $.each(table_fields, function(index, value){
                $("<th>").append(value.title).appendTo(head);
            });
            table.append(head);

            $.each(data, function(index, value){
                var row = $("<tr>", {id:value.pk});
                $.each(table_meta, function(index, field_name){
                    var td = $("<td>").append(value.fields[field_name.name]).appendTo(row)
                    td.on(
                        "click", function(e){
                            var fld = getField(field_name).val($(this).html());
                            fld.on('blur', function(e){
                                $(this).replaceWith(td.html($(this).val()));
                            });
                            $(this).replaceWith(fld)
                            fld.focus();
                        });
                });
                table.append(row);
            });

            $.each(table_fields, function(index, value){
                var div = $("<div>"),
                    field = getField(value).appendTo(div);
                $("<label>",{
                    for:value.name
                }).append(value.title).appendTo(form);
                //div.append(field);
                form.append(div);
            });

            $("<input>",{
                type:"submit",
                value:"Save",
            }).appendTo(form);

            $("#form").html(form).submit(
                function (e){
                    $.ajax({ 
                        url   : form.attr('action'),
                        type  : form.attr('method'),
                        data  : form.serialize(), // data to be submitted
                        success: function(response){
                            if (!response.success){
                                alert(response.message);
                            } else {
                                $("#form").empty();
                                $("#table").empty();
                            }
                        }
                    });
                    return false;
                }
            );
            $("#table").html(table);

        });
    }

    $(function() {
        getTablesList().done(function(data){
            var list = $("ol.tables");
            $.each(data, function(index, value){
                var link = $("<a>", {
                        id: value.name,
                        href: value.url,
                        title: value.name
                    }).append(value.title),
                    li = $("<li>").append(link);
                meta[value.name] = value.fields;
                list.append(li);
            });
            list.on("click", "li", function(e){
                e.preventDefault();
                var link = e.target;
                updateForm(link);
            })
        });
    });

}));
